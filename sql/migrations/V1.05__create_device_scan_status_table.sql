CREATE TABLE scan_status (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    completed BOOLEAN NOT NULL
);