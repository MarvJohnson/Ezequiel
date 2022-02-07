DROP DATABASE ezequiel;
CREATE DATABASE ezequiel;
CREATE USER ezequieluser WITH PASSWORD 'ezequiel';
GRANT ALL PRIVILEGES ON DATABASE ezequiel TO ezequieluser;
ALTER USER ezequieluser CREATEDB;