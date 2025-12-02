CREATE TABLE dates
(
    date_id INTEGER IDENTITY(1,1) PRIMARY KEY,
    record_date DATE NOT NULL,
    month INTEGER NOT NULL,
    year INTEGER NOT NULL
);

CREATE TABLE routes
(
    route_id INTEGER IDENTITY(1,1) PRIMARY KEY,
    origin VARCHAR(100) NOT NULL,
    destination VARCHAR(100) NOT NULL,
    distance_km INTEGER NOT NULL
);

CREATE TABLE vehicles
(
    vehicle_id INTEGER IDENTITY(1,1) PRIMARY KEY,
    plate_number VARCHAR(20) NOT NULL,
    vehicle_type VARCHAR(50) NOT NULL,
    capacity INTEGER NOT NULL
);

CREATE TABLE fact_freights
(
    freight_id INTEGER IDENTITY(1,1) PRIMARY KEY,
    date_id INTEGER NOT NULL,
    route_id INTEGER NOT NULL,
    vehicle_id INTEGER NOT NULL,
    freight_value DECIMAL(10, 2) NOT NULL,
    diesel_price DECIMAL(10, 2) NOT NULL,
    weight_ton DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (date_id) REFERENCES dates(date_id),
    FOREIGN KEY (route_id) REFERENCES routes(route_id),
    FOREIGN KEY (vehicle_id) REFERENCES vehicles(vehicle_id)
);