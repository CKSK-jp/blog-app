-- from the terminal run:
-- psql < music.sql

DROP DATABASE IF EXISTS blogly;

CREATE DATABASE blogly;

\c blogly

CREATE TABLE artists
(
  id SERIAL PRIMARY KEY,
  name TEXT NOT NULL
);

CREATE TABLE producers
(
  id SERIAL PRIMARY KEY,
  name TEXT NOT NULL
);

CREATE TABLE albums
(
  id SERIAL PRIMARY KEY,
  title TEXT NOT NULL
);

CREATE TABLE songs
(
  id SERIAL PRIMARY KEY,
  title TEXT NOT NULL,
  duration_in_seconds INTEGER NOT NULL,
  release_date DATE NOT NULL,
  album_id INT REFERENCES albums(id),
  artist_id INT REFERENCES artists(id),
  producer_id INT REFERENCES producers(id)
);

INSERT INTO artists (name) VALUES
  ('Hanson'),
  ('Queen'),
  ('Mariah Carey'),
  ('Boyz II Men'),
  ('Lady Gaga'),
  ('Bradley Cooper'),
  ('Nickelback'),
  ('Jay Z'),
  ('Alicia Keys'),
  ('Katy Perry'),
  ('Juicy J'),
  ('Maroon 5'),
  ('Christina Aguilera'),
  ('Avril Lavigne'),
  ('Destiny''s Child');

INSERT INTO producers (name) VALUES
  ('Dust Brothers'),
  ('Stephen Lironi'),
  ('Roy Thomas Baker'),
  ('Walter Afanasieff'),
  ('Benjamin Rice'),
  ('Rick Parashar'),
  ('Al Shux'),
  ('Max Martin'),
  ('Cirkut'),
  ('Shellback'),
  ('Benny Blanco'),
  ('The Matrix'),
  ('Darkchild');

INSERT INTO albums (title) VALUES
  ('Middle of Nowhere'),
  ('A Night at the Opera'),
  ('Daydream'),
  ('A Star Is Born'),
  ('Silver Side Up'),
  ('The Blueprint 3'),
  ('Prism'),
  ('Hands All Over'),
  ('Let Go'),
  ('The Writing''s on the Wall');

INSERT INTO songs
  (title, duration_in_seconds, release_date, album_id, artist_id, producer_id)
VALUES
  ('MMMBop', 238, '1997-04-15', 1, 1, 1),
  ('Bohemian Rhapsody', 355, '1975-10-31', 2, 2, 2),
  ('One Sweet Day', 282, '1995-11-14', 3, 3, 3),
  ('Shallow', 216, '2018-09-27', 4, 4, 4),
  ('How You Remind Me', 223, '2001-08-21', 5, 5, 5),
  ('New York State of Mind', 276, '2009-10-20', 6, 6, 6),
  ('Dark Horse', 215, '2013-12-17', 7, 7, 7),
  ('Moves Like Jagger', 201, '2011-06-21', 8, 8, 8),
  ('Complicated', 244, '2002-05-14', 9, 9, 9),
  ('Say My Name', 240, '1999-11-07', 10, 10, 10);