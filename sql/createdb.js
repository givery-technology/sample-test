var sqlite3 = require('sqlite3').verbose();
var fs      = require("fs");

var dbname = "mydb.db";

if (fs.existsSync(dbname)) {
  fs.unlinkSync(dbname);
}
var db = new sqlite3.Database(dbname);
try {
  db.serialize(function() {
    var statements = fs.readFileSync("sql/create.sql", "utf-8").split(";");
    statements.pop();//Remove last empty string
    statements.forEach(function(sql) {
      db.run(sql.trim());
    });
  });
} finally {
  db.close();  
}
