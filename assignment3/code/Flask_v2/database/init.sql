-- init.sql

CREATE TABLE entity (
    id SERIAL PRIMARY KEY,
    text VARCHAR(100)
);

CREATE TABLE relation (
    id SERIAL PRIMARY KEY,
    relation_text VARCHAR(100),
    entity_id INTEGER REFERENCES entity(id)
);
