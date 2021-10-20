DROP TABLE IF EXISTS room_time;
DROP TABLE IF EXISTS room;
DROP TABLE IF EXISTS user;


CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT, 
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);


CREATE TABLE room (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  room_number INTEGER NOT NULL
);


INSERT INTO room (room_number) VALUES (101);
INSERT INTO room (room_number) VALUES (102);
INSERT INTO room (room_number) VALUES (103);
INSERT INTO room (room_number) VALUES (104);
INSERT INTO room (room_number) VALUES (105);


CREATE TABLE room_time (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  room_id INTEGER NOT NULL,
  user_id INTEGER NOT NULL,
  room_name TEXT,
  from_time DATE NOT NULL,
  to_time DATE NOT NULL,
  FOREIGN KEY (room_id) REFERENCES room (id)
  FOREIGN KEY (user_id) REFERENCES user (id)
);