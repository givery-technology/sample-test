"use strict";
var assert = require("chai").assert;
var spec = require("api-first-spec");
var config = require("../config/config.json");
var db = new (require("./db.util"))(config.database);
var LoginAPI = require("./login.spec");

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
  var e1;

  beforeEach(function(done) {
    initData(function(data) {
      e1 = data.events[0].id;

      db.del("attends").then(function() {
        host = spec.host(config.host).api(API).login({
          "email": "user1@test.com",
          "password": "password"
        }).success(function(data, res) {
          token = data.token;
          userId = data.user.id;
          done();
        });
      });
    });
  });

  it("can reserve an event.", function(done) {
    host.api(API).params({
      "token": token,
      "event_id": e1,
      "reserve": true
    }).success(function(data, res) {
      assert.equal(data.code, 200);
      done();
    });
  });
  it("can not reserve already reaserved event.", function(done) {
    db.create({
      "attends": {
        "user_id": userId,
        "event_id": e1
      }
    }).then(function() {
      host.api(API).params({
        "token": token,
        "event_id": e1,
        "reserve": true
      }).success(function(data, res) {
        assert.equal(data.code, 501);//Already reserved
        done();
      });
    });
  });
  it("can unreserve already reaserved event.", function(done) {
    db.create({
      "attends": {
        "user_id": userId,
        "event_id": e1
      }
    }).then(function() {
      host.api(API).params({
        "token": token,
        "event_id": e1,
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
      "event_id": e1,
      "reserve": false
    }).success(function(data, res) {
      assert.equal(data.code, 502);//Not reserved
      done();
    });
  });
});

function initData(done) {
  db.deleteAll().then(function() {
    db.create(require("../sql/testdata.json")).then(function(data) {
      done(data);
    });
  });
}

module.exports = API;
