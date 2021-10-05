DROP TABLE IF EXISTS room_time;
DROP TABLE IF EXISTS room;
DROP TABLE IF EXISTS user;


CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,  /* obs, her er user/session id sequential */
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);
/*
CREATE TABLE post (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  title TEXT NOT NULL,
  body TEXT NOT NULL,
  FOREIGN KEY (author_id) REFERENCES user (id)
);
*/
CREATE TABLE room (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  room_number INTEGER NOT NULL
);

INSERT INTO room (room_number) VALUES (101);
INSERT INTO room (room_number) VALUES (102);
INSERT INTO room (room_number) VALUES (103);
INSERT INTO room (room_number) VALUES (104);
INSERT INTO room (room_number) VALUES (105);


/* konverter input til dato type for å kunne sammenligne med from/to i tabell under */

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