CREATE TABLE switch_types (
    id UUID PRIMARY KEY,
    name VARCHAR(40) NOT NULL
);

INSERT INTO switch_types (id, name)
    VALUES ('b195b325-767a-4ecb-b54f-9aafe756f70b', 'light'),
           ('199a8196-0dd1-461e-adca-823da8e0b804', 'fan');

ALTER TABLE devices ADD COLUMN switch_type_id UUID;

ALTER TABLE devices ADD CONSTRAINT fk_switch_type FOREIGN KEY (switch_type_id)
          REFERENCES switch_types (id);