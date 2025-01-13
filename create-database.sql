CREATE DATABASE moviecollector;

CREATE USER movie_admin WITH PASSWORD 'password';

GRANT ALL PRIVILEGES ON DATABASE moviecollector TO movie_admin;

