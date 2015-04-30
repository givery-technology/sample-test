"use strict";
var
  assert = require("chai").assert,
  spec = require("api-first-spec"),
  config = require("./config/config.json"),
  fixtures = new (require("sql-fixtures"))(config.database),
  moment = require("moment"),
  LoginAPI = require("./login.spec");

var API = spec.define({
  "endpoint": "/api/companies/events",
  "method": "POST",
  "login": LoginAPI,
  "request": {
    "contentType": spec.ContentType.URLENCODED,
    "params": {
      "token": "string",
      "from": "date",
      "offset": "int",
      "limit": "int"
    },
    "rules": {
      "token": {
        "required": true
      },
      "from": {
        "required": true,
        "format": "YYYY-MM-DD"
      },
      "offset": {
        "min": 0
      },
      "limit": {
        "min": 1
      }
   }
  },
  "response": {
    "contentType": spec.ContentType.JSON,
    "data": {
      "code": "int",
      "events": [{
        "id": "int",
        "name": "string",
        "start_date": "datetime",
        "number_of_attendees": "int"
      }]
    },
    "rules": {
      "code": {
        "required": true
      },
      "events": {
        "required": function(data) {
          data.code == 200;
        }
      },
      "events.id": {
        "required": true
      },
      "events.name": {
        "required": true
      },
      "events.start_date": {
        "required": true,
        "format": "YYYY-MM-DD HH:mm:ss"
      },
      "events.number_of_attendees": {
        "required": true
      }
    }
  }
});

function checkSorted(events) {
  if (events.length == 0) {
    return;
  }
  var prev = moment(events[0].start_date).toDate().getTime();
  for (var i=0; i<events.length; i++) {
    var current = moment(events[i].start_date).toDate().getTime();
    assert.ok(prev <= current);
    prev = current;
  }
}

describe("Without token", function() {
  var host = spec.host(config.host);

  it("can not call with out login", function(done) {
    host.api(API).params({
      "token": null,
      "from": "2015-04-01"
    }).success(function(data, res) {
      assert.equal(data.code, 401);
      done();
    });
  });
});

describe("With student user", function() {
  var host = spec.host(config.host), token;
  before(function(done) {
    host.api(API).login({
      "email": "user1@test.com",
      "password": "password"
    }).success(function(data, res) {
      token = data.token;
      done();
    });
  });

  it("can not call.", function(done) {
    host.api(API).params({
      "token": token,
      "from": "2015-04-01"
    }).success(function(data, res) {
      assert.equal(data.code, 401);
      done();
    });
  });
});

describe("With company user", function() {
  var host = spec.host(config.host), token, userId;
  before(function(done) {
    host.api(API).login({
      "email": "givery@test.com",
      "password": "password"
    }).success(function(data, res) {
      token = data.token;
      userId = data.user.id;
      done();
    });
  });
  beforeEach(function(done) {
    fixtures.knex("attends").del().then(function() {
      done();
    });
  });

  it("Without from parameter", function(done) {
    host.api(API).params({
      "token": token
    }).badRequest(done);
  });
  it("Wrong limit", function(done) {
    host.api(API).params({
      "token": token,
      "from": "2015-04-01",
      "offset": 0,
      "limit": 0
    }).badRequest(done);
  });
  it("From 2015-04-01", function(done) {
    fixtures.create({
      "attends": [{
        "user_id": 1,
        "event_id": 1
      }, {
        "user_id": 2,
        "event_id": 1
      }]
    }).then(function() {
      host.api(API).params({
        "token": token,
        "from": "2015-04-01"
      }).success(function(data, res) {
        assert.equal(data.code, 200);
        assert.equal(data.events.length, 2);
        assert.equal(data.events[0].name, "Givery Event1");
        assert.equal(data.events[0].number_of_attendees, 2);
        assert.equal(data.events[1].number_of_attendees, 0);
        checkSorted(data.events);
        done();
      });
    });
  });
  it("From 2015-05-01", function(done) {
    host.api(API).params({
      "token": token,
      "from": "2015-05-01"
    }).success(function(data, res) {
      assert.equal(data.code, 200);
      assert.equal(data.events.length, 0)
      checkSorted(data.events);
      done();
    });
  });
  it("Specify offset", function(done) {
    host.api(API).params({
      "token": token,
      "from": "2015-04-01",
      "offset": 3
    }).success(function(data, res) {
      assert.equal(data.code, 200);
      assert.equal(data.events.length, 0)
      checkSorted(data.events);
      done();
    });
  });
  it("Specify offset and limit", function(done) {
    host.api(API).params({
      "token": token,
      "from": "2015-04-01",
      "offset": 1,
      "limit": 3
    }).success(function(data, res) {
      assert.equal(data.code, 200);
      assert.equal(data.events.length, 1)
      assert.equal(data.events[0].name, "Givery Event2");
      checkSorted(data.events);
      done();
    });
  });

});

module.exports = API;
