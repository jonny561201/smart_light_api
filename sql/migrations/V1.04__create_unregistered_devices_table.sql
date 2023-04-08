CREATE TABLE unregistered_devices (
    id VARCHAR(40) PRIMARY KEY,
    name VARCHAR(40) NOT NULL,
    ip_address INET NOT NULL,
    local_key VARCHAR(40) NOT NULL
--     type_id UUID REFERENCES device_types(id) NOT NULL
);