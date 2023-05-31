CREATE TABLE switch_type (
    id UUID PRIMARY KEY,
    name VARCHAR(40) NOT NULL
);

INSERT INTO switch_type (id, name)
    VALUES ('b195b325-767a-4ecb-b54f-9aafe756f70b', 'light'),
           ('199a8196-0dd1-461e-adca-823da8e0b804', 'fan');