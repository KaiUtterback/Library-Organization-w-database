from utils import *

# Database connection
def get_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='Gretschwhitefalcon1',
            database='library_manager'  
        )
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None



class Book:
    def __init__(self, title, author, isbn, genre, publication_date, availability='Available'):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.genre = genre
        self.publication_date = publication_date
        self.availability = availability

    def save_to_db(self):
        conn = get_connection()
        cursor = conn.cursor()
        query = """
        INSERT INTO books (title, author_id, genre_id, isbn, publication_date, availability) 
        VALUES (%s, %s, %s, %s, %s, %s);
        """
        cursor.execute(query, (self.title, self.author, self.genre, self.isbn, self.publication_date, self.availability))
        conn.commit()
        conn.close()

    def borrow(self):
        if self.availability == 'Available':
            self.availability = 'Borrowed'
            conn = get_connection()
            cursor = conn.cursor()
            query = "UPDATE books SET availability = %s WHERE isbn = %s;"
            cursor.execute(query, (self.availability, self.isbn))
            conn.commit()
            conn.close()
            return True
        else:
            print("This book is not available for borrowing.")
            return False

    def return_book(self):
        if self.availability == 'Borrowed':
            self.availability = 'Available'
            conn = get_connection()
            cursor = conn.cursor()
            query = "UPDATE books SET availability = %s WHERE isbn = %s;"
            cursor.execute(query, (self.availability, self.isbn))
            conn.commit()
            conn.close()
            return True
        else:
            print("This book is not currently borrowed.")
            return False



class User:
    def __init__(self, name, library_id, borrowed_books=None):
        self.name = name
        self.library_id = library_id
        self.borrowed_books = borrowed_books if borrowed_books else []

    def save_to_db(self):
        conn = get_connection()
        cursor = conn.cursor()
        query = "INSERT INTO users (name, library_id) VALUES (%s, %s);"
        cursor.execute(query, (self.name, self.library_id))
        conn.commit()
        conn.close()
        print(f"User {self.name} added successfully.")

    def borrow_book(self, book):
        if book.availability == 'Available':
            book.borrow()  # Update the book's availability
            conn = get_connection()
            cursor = conn.cursor()
            query = "INSERT INTO borrowed_books (user_id, book_id, borrow_date) VALUES (%s, %s, CURDATE());"
            cursor.execute(query, (self.library_id, book.isbn))
            conn.commit()
            conn.close()
            print(f"Book '{book.title}' successfully borrowed by {self.name}.")
        else:
            print("This book is not available for borrowing.")

    def return_book(self, book):
        if book.availability == 'Borrowed':
            book.return_book()  # Update the book's availability
            conn = get_connection()
            cursor = conn.cursor()
            query = "UPDATE borrowed_books SET return_date = CURDATE() WHERE user_id = %s AND book_id = %s;"
            cursor.execute(query, (self.library_id, book.isbn))
            conn.commit()
            conn.close()
            print(f"Book '{book.title}' returned successfully.")
        else:
            print("This book is not currently borrowed by this user.")

    def fetch_borrowed_books(self):
        conn = get_connection()
        cursor = conn.cursor()
        query = """
        SELECT b.title 
        FROM books b
        JOIN borrowed_books bb ON b.isbn = bb.book_id
        WHERE bb.user_id = %s AND bb.return_date IS NULL;
        """
        cursor.execute(query, (self.library_id,))
        books = cursor.fetchall()
        self.borrowed_books = [b[0] for b in books]  # Update borrowed_books list
        conn.close()
        return self.borrowed_books




class Author:
    def __init__(self, name, biography):
        self.name = name
        self.biography = biography

    def save_to_db(self):
        conn = get_connection()
        cursor = conn.cursor()
        query = "INSERT INTO authors (name, biography) VALUES (%s, %s);"
        cursor.execute(query, (self.name, self.biography))
        conn.commit()
        conn.close()
        print(f"Author {self.name} added successfully.")

    def fetch_details(self):
        conn = get_connection()
        cursor = conn.cursor()
        query = "SELECT name, biography FROM authors WHERE name = %s;"
        cursor.execute(query, (self.name,))
        details = cursor.fetchone()
        conn.close()
        if details:
            print(f"Name: {details[0]}, Biography: {details[1]}")
        else:
            print("Author not found.")

class Genre:
    def __init__(self, name, description):
        self.name = name
        self.description = description

    def save_to_db(self):
        conn = get_connection()
        cursor = conn.cursor()
        query = "INSERT INTO genres (name, description) VALUES (%s, %s);"
        cursor.execute(query, (self.name, self.description))
        conn.commit()
        conn.close()
        print(f"Genre '{self.name}' added successfully.")

    def fetch_details(self):
        conn = get_connection()
        cursor = conn.cursor()
        query = "SELECT name, description FROM genres WHERE name = %s;"
        cursor.execute(query, (self.name,))
        details = cursor.fetchone()
        conn.close()
        if details:
            print(f"Name: {details[0]}, Description: {details[1]}")
        else:
            print("Genre not found.")


class FictionBook(Book):
    def __init__(self, title, author, isbn, genre, publication_date, fiction_type, availability='Available'):
        super().__init__(title, author, isbn, genre, publication_date, availability)
        self.fiction_type = fiction_type

    def save_to_db(self):
        super().save_to_db()  
        conn = get_connection()
        cursor = conn.cursor()
        query = "UPDATE books SET fiction_type = %s WHERE isbn = %s;"
        cursor.execute(query, (self.fiction_type, self.isbn))
        conn.commit()
        conn.close()

class NonFictionBook(Book):
    def __init__(self, title, author, isbn, genre, publication_date, subject, availability='Available'):
        super().__init__(title, author, isbn, genre, publication_date, availability)
        self.subject = subject

    def save_to_db(self):
        super().save_to_db()  
        conn = get_connection()
        cursor = conn.cursor()
        query = "UPDATE books SET subject = %s WHERE isbn = %s;"
        cursor.execute(query, (self.subject, self.isbn))
        conn.commit()
        conn.close()

class MysteryBook(Book):
    def __init__(self, title, author, isbn, genre, publication_date, mystery_elements, availability='Available'):
        super().__init__(title, author, isbn, genre, publication_date, availability)
        self.mystery_elements = mystery_elements

    def save_to_db(self):
        super().save_to_db()  
        conn = get_connection()
        cursor = conn.cursor()
        query = "UPDATE books SET mystery_elements = %s WHERE isbn = %s;"
        cursor.execute(query, (self.mystery_elements, self.isbn))
        conn.commit()
        conn.close()
