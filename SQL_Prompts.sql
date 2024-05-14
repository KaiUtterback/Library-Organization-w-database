create database library_manager;

CREATE TABLE IF NOT EXISTS books (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    author_id INT,
    genre_id INT,
    isbn VARCHAR(13) UNIQUE NOT NULL,
    publication_date DATE,
    availability ENUM('Available', 'Borrowed') DEFAULT 'Available',
    FOREIGN KEY (author_id) REFERENCES authors(id) ON DELETE SET NULL,
    FOREIGN KEY (genre_id) REFERENCES genres(id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    library_id VARCHAR(10) UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS authors (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) UNIQUE NOT NULL,
    biography TEXT
);

CREATE TABLE IF NOT EXISTS genres (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) UNIQUE NOT NULL,
    description TEXT
);

CREATE TABLE IF NOT EXISTS borrowed_books (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    book_id INT,
    borrow_date DATE NOT NULL,
    return_date DATE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (book_id) REFERENCES books(id) ON DELETE CASCADE
);


CREATE INDEX idx_isbn ON books(isbn);
CREATE INDEX idx_library_id ON users(library_id);


-- Insert borrowed books (make sure user and book IDs exist)
INSERT INTO borrowed_books (user_id, book_id, borrow_date) VALUES (1, 1, CURDATE());

ALTER TABLE books
ADD COLUMN fiction_type VARCHAR(255) DEFAULT NULL,
ADD COLUMN subject VARCHAR(255) DEFAULT NULL,
ADD COLUMN mystery_elements VARCHAR(255) DEFAULT NULL;


DESCRIBE books;
DESCRIBE borrowed_books;


SELECT * FROM authors;
SELECT * FROM genres;
select * from books;
select * from borrowed_books;
