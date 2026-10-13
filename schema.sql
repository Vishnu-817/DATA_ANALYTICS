CREATE DATABASE IF NOT EXISTS restaurant_db
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE restaurant_db;

CREATE TABLE IF NOT EXISTS menu_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(120) NOT NULL,
    description VARCHAR(500) NOT NULL,
    price DECIMAL(8, 2) NOT NULL,
    category VARCHAR(60) NOT NULL,
    image_url VARCHAR(500) NOT NULL,
    available BOOLEAN NOT NULL DEFAULT TRUE,
    UNIQUE KEY uq_menu_item_name (name)
);

CREATE TABLE IF NOT EXISTS reservations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    customer_name VARCHAR(100) NOT NULL,
    email VARCHAR(254) NOT NULL,
    phone VARCHAR(30),
    reservation_date DATE NOT NULL,
    reservation_time TIME NOT NULL,
    guests TINYINT UNSIGNED NOT NULL,
    notes VARCHAR(1000),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_reservation_datetime (reservation_date, reservation_time)
);

INSERT INTO menu_items (name, description, price, category, image_url) VALUES
    ('Burrata & Heirloom Tomato', 'Creamy burrata, ripe summer tomatoes, basil oil, and toasted sourdough.', 14.00, 'Starters', 'https://images.unsplash.com/photo-1608039829572-78524f79c4c7?auto=format&fit=crop&w=900&q=85'),
    ('Wild Mushroom Arancini', 'Crisp risotto bites with wild mushrooms, parmesan, and truffle aioli.', 12.00, 'Starters', 'https://images.unsplash.com/photo-1604908176997-125f25cc6f3d?auto=format&fit=crop&w=900&q=85'),
    ('Rosemary Roast Chicken', 'Herb-roasted chicken, silky potato purée, seasonal greens, and pan jus.', 27.00, 'Mains', 'https://images.unsplash.com/photo-1532550907401-a500c9a57435?auto=format&fit=crop&w=900&q=85'),
    ('Wild Mushroom Tagliatelle', 'Fresh pasta, forest mushrooms, parmesan, and a touch of cream.', 24.00, 'Mains', 'https://images.unsplash.com/photo-1473093295043-cdd812d0e601?auto=format&fit=crop&w=900&q=85'),
    ('Pan-Seared Salmon', 'Crisp-skinned salmon with lemon, crushed peas, and brown butter.', 29.00, 'Mains', 'https://images.unsplash.com/photo-1467003909585-2f8a72700288?auto=format&fit=crop&w=900&q=85'),
    ('Vanilla Bean Panna Cotta', 'Silky vanilla panna cotta with roasted berries and almond crumble.', 10.00, 'Desserts', 'https://images.unsplash.com/photo-1488477181946-6428a0291777?auto=format&fit=crop&w=900&q=85')
ON DUPLICATE KEY UPDATE name = VALUES(name);
