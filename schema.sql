CREATE DATABASE medicinedb;

CREATE TABLE medicines (
    id BIGINT PRIMARY KEY,
    sku_id TEXT,
    name TEXT,
    manufacturer_name TEXT,
    marketer_name TEXT,
    type TEXT,
    price NUMERIC,
    pack_size_label TEXT,
    short_composition TEXT,
    is_discontinued BOOLEAN,
    available BOOLEAN
);

CREATE EXTENSION IF NOT EXISTS pg_trgm;
CREATE EXTENSION IF NOT EXISTS unaccent;

ALTER TABLE medicines
medicinedb-# ADD COLUMN search_vector tsvector;

UPDATE medicines
SET search_vector =
    to_tsvector(
        'english',
        coalesce(name,'') || ' ' ||
        coalesce(short_composition,'') || ' ' ||
        coalesce(manufacturer_name,'')
    );


CREATE INDEX idx_medicines_search_vector
ON medicines USING GIN(search_vector);

CREATE INDEX idx_medicines_name_trgm
ON medicines USING GIN (name gin_trgm_ops);