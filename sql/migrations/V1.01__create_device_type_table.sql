CREATE TABLE device_types (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(30) NOT NULL
);

INSERT INTO device_types (name) VALUES ('outlet'), ('cover'), ('bulb'), ('cloud');