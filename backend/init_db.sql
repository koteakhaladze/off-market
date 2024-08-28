CREATE TABLE IF NOT EXISTS properties (
    id SERIAL PRIMARY KEY,
    address VARCHAR(200) NOT NULL,
    price NUMERIC(10, 2) NOT NULL,
    bedrooms INTEGER,
    bathrooms INTEGER,
    square_footage NUMERIC(8, 2),
    latitude NUMERIC(10, 6),
    longitude NUMERIC(10, 6)
);


CREATE TABLE IF NOT EXISTS posts (
    id SERIAL PRIMARY KEY,
    user_name VARCHAR(1000) NULL,
    user_url VARCHAR(1000) NULL,
    text TEXT NOT NULL,
    timestamp INTEGER NULL,
    image_urls JSON NULL,
    base_url VARCHAR(1000) NOT NULL
);

-- CREATE TABLE IF NOT EXISTS offers (
--     id SERIAL PRIMARY KEY,
--     property_id INTEGER FOREIGN KEY REFERENCES properties(id) NOT NULL,
--     amount NUMERIC(10, 2) NOT NULL,
--     name VARCHAR(100) NOT NULL,
--     phone VARCHAR(20) NOT NULL,
--     email VARCHAR(100) NOT NULL
-- );

INSERT INTO properties (address, price, bedrooms, bathrooms, square_footage, latitude, longitude)
VALUES 
('1234 Oak Avenue, Metropolis', 450000, 3, 2.5, 2000, 40.7128, -74.0060),
('567 Maple Street, Metropolis', 380000, 2, 2, 1500, 40.7150, -74.0070),
('789 Pine Road, Metropolis', 520000, 4, 3, 2500, 40.7170, -74.0080),
('101 Cedar Lane, Metropolis', 600000, 4, 3.5, 3000, 40.7190, -74.0090),
('2468 Birch Boulevard, Metropolis', 350000, 2, 1.5, 1200, 40.7210, -74.0100),
('1357 Spruce Street, Metropolis', 420000, 3, 2, 1800, 40.7230, -74.0110)
