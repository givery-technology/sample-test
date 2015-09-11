"use strict";
var assert = require("chai").assert;
var spec = require("api-first-spec");
var config = require("../config/config.json");
var db = new (require("./db.util"))(config.database);

var API = spec.define({
  "endpoint": "/api/auth/login",
  "method": "POST",
  "request": {
    "contentType": spec.ContentType.URLENCODED,
    "params": {
      "email": "string",
      "password": "string"
    },
    "rules": {
      "email": {
        "required": true
      },
      "password": {
        "required": true
      }
   }
  },
  "response": {
    "contentType": spec.ContentType.JSON,
    "data": {
      "code": "int",
      "token": "string",
      "user": {
        "id": "int",
        "name": "string",
        "group_id": "int"
      }
    },
    "rules": {
      "code": {
        "required": true
      },
      "token": {
        "required": function(data) {
          return data.code == 200;
        }
      },
      "user": {
        "required": function(data) {
          return data.code == 200;
        }
      },
      "user.*": {
        "required": true
      },
      "user.group_id": {
        "min": 1,
        "max": 2
      }
    }
  }
});

describe("login", function() {
  var host = spec.host(config.host);

  beforeEach(function(done) {
    initData(done);
  });

  host.api(API).params({
    "token": "test2",
    "password": "password"
  }).badRequestAll({
    "password": ["abc def", "あいうえおかきくけこ"],
  });
  
  it("Wrong password", function(done) {
    host.api(API).params({
      "email": "user1@test.com",
      "password": "wrong"
    }).success(function(data, res) {
      assert.equal(data.code, 500);
      done();
    });
  });
  it("Wrong username", function(done) {
    host.api(API).params({
      "email": "unknown@test.com",
      "password": "password"
    }).success(function(data, res) {
      assert.equal(data.code, 500);
      done();
    });
  });
  it("Success", function(done) {
    host.api(API).params({
      "email": "user1@test.com",
      "password": "password"
    }).success(function(data, res) {
      assert.equal(data.code, 200);
      assert.ok(data.token.length > 0);
      assert.equal(data.user.name, "John Smith");
      assert.equal(data.user.group_id, 1);
      done();
    });
  });
});

function initData(done) {
  db.deleteAll().then(function() {
    db.create(require("../sql/testdata.json")).then(function() {
      done();
    });
  });
}
module.exports = API;
