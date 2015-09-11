"use strict";
var
  _ = require("lodash"),
  fs = require("fs"),
  Promise = require("bluebird"),
  Fixtures = require("sql-fixtures");

function DBUtilsImpl(config) {
  var fixtures = new Fixtures(config);
  var tables = [
    "users",
    "events",
    "attends"
  ];

  function deleteAll() {
    return del(tables);
  }
  function truncateAll() {
    return truncate(tables);
  }

  function del(tableNames) {
    if (!_.isArray(tableNames)) {
      tableNames = [tableNames];
    }
    var knex = fixtures.knex;
    var promises = _.map(tableNames, function(name) {
      return knex(name).del();
    });
    return Promise.all(promises);
  }
  function truncate(tableNames) {
    if (!_.isArray(tableNames)) {
      tableNames = [tableNames];
    }
    var knex = fixtures.knex;
    var promises = _.map(tableNames, function(name) {
      return knex(name).truncate();
    });
    return Promise.all(promises);
  }
  function create(data) {
    return fixtures.create(data);
  }
  function verifySingle(data, sql) {
    var params = [sql];
    if (arguments.length > 2) {
      params.push(Array.prototype.slice.call(arguments, 2));
    }
    var promise = new Promise(function (resolve, reject) {
      var knex = fixtures.knex;
      knex.raw.apply(knex, params).then(function(resp) {
        var rows = resp.rows;
        if (resp.rowCount !== 1) {
          reject(new Error("sql[" + sql + "] returns " + resp.rowCount + "rows"));
          return;
        }
        var row = rows[0];
        var error = null;
        _.keys(data).forEach(function(key) {
          if (data[key] !== row[key]) {
            error = new Error("sql[" + sql + "] returns " + JSON.stringify(row));
          }
        });
        if (error) {
          reject(error);
        } else {
          resolve(row);
        }
      });
    });
    return promise;
  }
  _.extend(this, {
    knex: fixtures.knex,
    deleteAll: deleteAll,
    del: del,
    truncateAll: truncateAll,
    truncate: truncate,
    create: create,
    verifySingle: verifySingle
  });
}

module.exports = DBUtilsImpl;
