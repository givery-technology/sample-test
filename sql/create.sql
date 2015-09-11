CREATE TABLE users (
  id integer PRIMARY KEY AUTOINCREMENT,
  name varchar(100) NOT NULL,
  password varchar(100) NOT NULL,
  email varchar(100) NOT NULL,
  group_id int NOT NULL
);

CREATE TABLE events (
  id integer PRIMARY KEY AUTOINCREMENT,
  user_id int NOT NULL,
  name varchar(100) NOT NULL,
  start_date datetime NOT NULL
);

CREATE TABLE attends (
  user_id int NOT NULL,
  event_id int NOT NULL,
  reserved_at timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (user_id, event_id)
);
