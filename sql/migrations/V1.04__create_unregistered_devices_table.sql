CREATE TABLE unregistered_devices (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(40) NOT NULL,
    ip_address INET NOT NULL,
    local_key VARCHAR(40) NOT NULL,
    device_id VARCHAR(40) NOT NULL
--     type_id UUID REFERENCES device_types(id) NOT NULL
);