CREATE TABLE device_types (
    id UUID PRIMARY KEY,
    name VARCHAR(30) NOT NULL
);

INSERT INTO device_types (id, name)
VALUES ('26cf7b35-8366-4c16-be9a-e0009bda62b6', 'outlet'),
       ('58927435-1afd-41b2-be1c-0ee21a8294b8', 'cover'),
       ('8a1e98ae-63c7-444e-971f-1781cc6f9352', 'bulb'),
       ('e60ae72e-4f16-40ff-a3cc-323effa73810', 'cloud');