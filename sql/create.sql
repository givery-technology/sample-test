CREATE TABLE IF NOT EXISTS users (
  id serial PRIMARY KEY,
  name varchar(100) NOT NULL,
  password varchar(100) NOT NULL,
  email varchar(100) NOT NULL,
  group_id int NOT NULL
);

CREATE TABLE IF NOT EXISTS events (
  id serial PRIMARY KEY,
  user_id int NOT NULL,
  name varchar(100) NOT NULL,
  start_date datetime NOT NULL
);

CREATE TABLE IF NOT EXISTS attends (
  user_id int NOT NULL,
  event_id int NOT NULL,
  reserved_at timestamp NOT NULL DEFAULT now(),
  PRIMARY KEY (user_id, event_id)
);

TRUNCATE TABLE users;
TRUNCATE TABLE events;
TRUNCATE TABLE attends;

ALTER TABLE users AUTO_INCREMENT = 1;
ALTER TABLE events AUTO_INCREMENT = 1;

INSERT INTO users (name, password, email, group_id) VALUES ('givery Inc.', sha1('password'), 'givery@test.com', 2);
INSERT INTO users (name, password, email, group_id) VALUES ('Google Inc.', sha1('password'), 'google@test.com', 2);
INSERT INTO users (name, password, email, group_id) VALUES ('Apple Inc.', sha1('password'), 'apple@test.com', 2);

INSERT INTO users (name, password, email, group_id) VALUES ('John Smith', sha1('password'), 'user1@test.com', 1);
INSERT INTO users (name, password, email, group_id) VALUES ('Taro Yamada', sha1('password'), 'user2@test.com', 1);
INSERT INTO users (name, password, email, group_id) VALUES ('Ichiro Suzuki', sha1('password'), 'user3@test.com', 1);

INSERT INTO events (user_id, name, start_date) VALUES (1, 'Givery Event1', '2015-04-17 19:00:00');
INSERT INTO events (user_id, name, start_date) VALUES (1, 'Givery Event2', '2015-04-19 19:00:00');
INSERT INTO events (user_id, name, start_date) VALUES (2, 'Google Event1', '2015-04-19 14:00:00');
INSERT INTO events (user_id, name, start_date) VALUES (2, 'Google Event2', '2015-05-19 14:00:00');
INSERT INTO events (user_id, name, start_date) VALUES (3, 'Apple Event1', '2015-05-02 14:00:00');
INSERT INTO events (user_id, name, start_date) VALUES (3, 'Apple Event2', '2015-05-19 14:00:00');
