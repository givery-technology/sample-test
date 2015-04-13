"use strict";
var
  assert = require("chai").assert,
  spec = require("api-first-spec"),
  config = require("./config/config.json"),
  fixtures = new (require("sql-fixtures"))(config.database),
  LoginAPI = require("./login.spec");

var API = spec.define({
  "endpoint": "/api/users/reserve",
  "method": "POST",
  "login": LoginAPI,
  "request": {
    "contentType": spec.ContentType.URLENCODED,
    "params": {
      "token": "string",
      "event_id": "int",
      "reserve": "boolean"
    },
    "rules": {
      "token": {
        "required": true
      },
      "event_id": {
        "required": true
      },
      "reserve": {
        "required": true
      }
   }
  },
  "response": {
    "contentType": spec.ContentType.JSON,
    "data": {
      "code": "int",
      "message": "string"
    },
    "rules": {
      "code": {
        "required": true
      },
      "message": {
        "required": function(data) {
          return data.code != 200;
        }
      }
    }
  }
});

describe("Without token", function() {
  var host = spec.host(config.host);

  it("can not call with out login", function(done) {
    host.api(API).params({
      "token": null,
      "event_id": 1,
      "reserve": true
    }).success(function(data, res) {
      assert.equal(data.code, 401);
      done();
    });
  });
});

describe("With company user", function() {
  var host, token;
  before(function(done) {
    host = spec.host(config.host).api(API).login({
      "email": "givery@test.com",
      "password": "password"
    }).success(function(data, res) {
      token = data.token;
      done();
    });
  });

  it("can not reserve event.", function(done) {
    host.api(API).params({
      "token": token,
      "event_id": 1,
      "reserve": true
    }).success(function(data, res) {
      assert.equal(data.code, 401);
      done();
    });
  });
});

describe("With student user", function() {
  var host, token, userId;
  before(function(done) {
    host = spec.host(config.host).api(API).login({
      "email": "user1@test.com",
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

  it("can reserve an event.", function(done) {
    host.api(API).params({
      "token": token,
      "event_id": 1,
      "reserve": true
    }).success(function(data, res) {
      assert.equal(data.code, 200);
      done();
    });
  });
  it("can not reserve already reaserved event.", function(done) {
    fixtures.create({
      "attends": {
        "user_id": userId,
        "event_id": 1
      }
    }).then(function() {
      host.api(API).params({
        "token": token,
        "event_id": 1,
        "reserve": true
      }).success(function(data, res) {
        assert.equal(data.code, 501);//Already reserved
        done();
      });
    });
  });
  it("can unreserve already reaserved event.", function(done) {
    fixtures.create({
      "attends": {
        "user_id": userId,
        "event_id": 1
      }
    }).then(function() {
      host.api(API).params({
        "token": token,
        "event_id": 1,
        "reserve": false
      }).success(function(data, res) {
        assert.equal(data.code, 200);
        done();
      });

    });
  });
  it("can not unreserve not reaserved event.", function(done) {
    host.api(API).params({
      "token": token,
      "event_id": 1,
      "reserve": false
    }).success(function(data, res) {
      assert.equal(data.code, 502);//Not reserved
      done();
    });
  });
});

module.exports = API;
