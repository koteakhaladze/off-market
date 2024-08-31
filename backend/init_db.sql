CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(80) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(512) NOT NULL,
    role VARCHAR(20) NOT NULL DEFAULT 'user'
);


CREATE TABLE IF NOT EXISTS properties (
    id SERIAL PRIMARY KEY,
    address VARCHAR(200) NOT NULL,
    price NUMERIC(10, 2) NOT NULL,
    bedrooms INTEGER,
    bathrooms INTEGER,
    square_footage NUMERIC(8, 2),
    latitude NUMERIC(10, 6),
    longitude NUMERIC(10, 6),
    image_urls JSON NULL
);


CREATE TABLE IF NOT EXISTS posts (
    id SERIAL PRIMARY KEY,
    user_name VARCHAR(1000) NULL,
    user_url VARCHAR(1000) NULL,
    text TEXT NOT NULL,
    timestamp INTEGER NULL,
    image_urls JSON NULL,
    base_url VARCHAR(1000) NOT NULL,
    comments JSON NULL,
    text_hash BYTEA NOT NULL,
    UNIQUE (text_hash, base_url)
);

CREATE INDEX idx_text_hash_base_url ON posts (text_hash, base_url);

CREATE TABLE IF NOT EXISTS offers (
    id SERIAL PRIMARY KEY,
    property_id INTEGER REFERENCES properties(id) ON DELETE CASCADE,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    amount NUMERIC(10, 2) NOT NULL,
    name VARCHAR(100) NOT NULL,
    phone VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'pending',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS saved_properties (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    property_id INTEGER REFERENCES properties(id) ON DELETE CASCADE,
    saved_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (user_id, property_id)
);


INSERT INTO properties (address, price, bedrooms, bathrooms, square_footage, latitude, longitude, image_urls)
VALUES 
('1234 Oak Avenue, Metropolis', 450000, 3, 2.5, 2000, 40.7128, -74.0060, '["https://scontent.ftbs5-3.fna.fbcdn.net/v/t39.30808-6/456787875_10233963435928621_1978816451833269547_n.jpg?stp=dst-jpg_s1080x2048&_nc_cat=102&ccb=1-7&_nc_sid=aa7b47&_nc_ohc=Ik-VdWc7uWMQ7kNvgEC26ln&_nc_ht=scontent.ftbs5-3.fna&oh=00_AYA_CmkNi9BTqV7jGC65v-QHp95WtaaKE9jFEoQAmFQURw&oe=66D60C28"]'),
('567 Maple Street, Metropolis', 380000, 2, 2, 1500, 40.7150, -74.0070, '["https://scontent.ftbs5-3.fna.fbcdn.net/v/t39.30808-6/456787875_10233963435928621_1978816451833269547_n.jpg?stp=dst-jpg_s1080x2048&_nc_cat=102&ccb=1-7&_nc_sid=aa7b47&_nc_ohc=Ik-VdWc7uWMQ7kNvgEC26ln&_nc_ht=scontent.ftbs5-3.fna&oh=00_AYA_CmkNi9BTqV7jGC65v-QHp95WtaaKE9jFEoQAmFQURw&oe=66D60C28"]'),
('789 Pine Road, Metropolis', 520000, 4, 3, 2500, 40.7170, -74.0080, '["https://scontent.ftbs5-3.fna.fbcdn.net/v/t39.30808-6/456787875_10233963435928621_1978816451833269547_n.jpg?stp=dst-jpg_s1080x2048&_nc_cat=102&ccb=1-7&_nc_sid=aa7b47&_nc_ohc=Ik-VdWc7uWMQ7kNvgEC26ln&_nc_ht=scontent.ftbs5-3.fna&oh=00_AYA_CmkNi9BTqV7jGC65v-QHp95WtaaKE9jFEoQAmFQURw&oe=66D60C28"]'),
('101 Cedar Lane, Metropolis', 600000, 4, 3.5, 3000, 40.7190, -74.0090, '["https://scontent.ftbs5-3.fna.fbcdn.net/v/t39.30808-6/456787875_10233963435928621_1978816451833269547_n.jpg?stp=dst-jpg_s1080x2048&_nc_cat=102&ccb=1-7&_nc_sid=aa7b47&_nc_ohc=Ik-VdWc7uWMQ7kNvgEC26ln&_nc_ht=scontent.ftbs5-3.fna&oh=00_AYA_CmkNi9BTqV7jGC65v-QHp95WtaaKE9jFEoQAmFQURw&oe=66D60C28"]'),
('2468 Birch Boulevard, Metropolis', 350000, 2, 1.5, 1200, 40.7210, -74.0100, '["https://scontent.ftbs5-3.fna.fbcdn.net/v/t39.30808-6/456787875_10233963435928621_1978816451833269547_n.jpg?stp=dst-jpg_s1080x2048&_nc_cat=102&ccb=1-7&_nc_sid=aa7b47&_nc_ohc=Ik-VdWc7uWMQ7kNvgEC26ln&_nc_ht=scontent.ftbs5-3.fna&oh=00_AYA_CmkNi9BTqV7jGC65v-QHp95WtaaKE9jFEoQAmFQURw&oe=66D60C28"]'),
('1357 Spruce Street, Metropolis', 420000, 3, 2, 1800, 40.7230, -74.0110, '["https://scontent.ftbs5-3.fna.fbcdn.net/v/t39.30808-6/456787875_10233963435928621_1978816451833269547_n.jpg?stp=dst-jpg_s1080x2048&_nc_cat=102&ccb=1-7&_nc_sid=aa7b47&_nc_ohc=Ik-VdWc7uWMQ7kNvgEC26ln&_nc_ht=scontent.ftbs5-3.fna&oh=00_AYA_CmkNi9BTqV7jGC65v-QHp95WtaaKE9jFEoQAmFQURw&oe=66D60C28"]')
;
