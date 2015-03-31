"use strict";
var 
  assert = require("chai").assert,
  spec = require("api-first-spec"),
  moment = require("moment"),
  config = require("./config/config.json");

var API = spec.define({
  "endpoint": "/api/users/events",
  "method": "GET",
  "request": {
    "contentType": spec.ContentType.URLENCODED,
    "params": {
      "from": "date",
      "offset": "int",
      "limit": "int"
    },
    "rules": {
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
        "company": {
          "id": "int",
          "name": "string"
        }
      }]
    },
    "rules": {
      "code": {
        "required": true
      },
      "events": {
        "required": true
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
      "events.company.id": {
        "required": true
      },
      "events.company.name": {
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
describe("users_events", function() {
  var host = spec.host(config.host);

  it("Without from parameter", function(done) {
    host.api(API).params({
    }).badRequest(done);
  });
  it("Wrong limit", function(done) {
    host.api(API).params({
      "from": "2015-04-01",
      "offset": 0,
      "limit": 0
    }).badRequest(done);
  });
  it("From 2015-04-01", function(done) {
    host.api(API).params({
      "from": "2015-04-01"
    }).success(function(data, res) {
      assert.equal(data.code, 200);
      assert.equal(data.events.length, 2);
      assert.equal(data.events[0].name == "Givery Event1");
      checkSorted(data.events);
      done();
    });
  });
  it("From 2015-04-18", function(done) {
    host.api(API).params({
      "from": "2015-04-18"
    }).success(function(data, res) {
      assert.equal(data.code, 200);
      assert.equal(data.events.length, 1);
      assert.equal(data.events[0].name == "Givery Event2");
      checkSorted(data.events);
      done();
    });
  });
  it("Specify offset", function(done) {
    host.api(API).params({
      "from": "2015-04-01",
      "offset": 2
    }).success(function(data, res) {
      assert.equal(data.code, 200);
      assert.equal(data.events.length, 0);
      checkSorted(data.events);
      done();
    });
  });
  it("Specify limit", function(done) {
    host.api(API).params({
      "from": "2015-04-01",
      "limit": 1
    }).success(function(data, res) {
      assert.equal(data.code, 200);
      assert.equal(data.events.length, 1)
      assert.equal(data.events[0].name == "Givery Event1");
      checkSorted(data.events);
      done();
    });
  });
});

module.exports = API;
