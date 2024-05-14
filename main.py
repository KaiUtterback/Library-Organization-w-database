import re
import json
import mysql.connector
from mysql.connector import Error

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

def add_book():
    title = input("Enter book title: ")
    author = input("Enter book author ID: ")  # Assuming author IDs are known
    isbn = input("Enter book ISBN: ")
    genre = input("Enter book genre ID: ")  # Assuming genre IDs are known
    publication_date = input("Enter publication date (YYYY-MM-DD): ")
    new_book = Book(title, author, isbn, genre, publication_date)
    new_book.save_to_db()
    print("Book added successfully!")

def fetch_books():
    conn = get_connection()
    cursor = conn.cursor()
    query = "SELECT title, author_id, isbn, genre_id, publication_date, availability FROM books;"
    cursor.execute(query)
    books = cursor.fetchall()
    for book in books:
        print(book)
    conn.close()




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

def add_user():
    name = input("Enter user name: ")
    library_id = input("Enter library ID: ")
    new_user = User(name, library_id)
    new_user.save_to_db()

def view_user_borrowed_books(library_id):
    user = User(name='', library_id=library_id)  # Placeholder user to access methods
    borrowed_books = user.fetch_borrowed_books()
    if borrowed_books:
        print("Borrowed Books:")
        for book in borrowed_books:
            print(book)
    else:
        print("No books currently borrowed.")


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

def add_author():
    name = input("Enter author's name: ")
    biography = input("Enter author's biography: ")
    new_author = Author(name, biography)
    new_author.save_to_db()

def view_author_details(name):
    author = Author(name, '')  # Biography not needed for fetching details
    author.fetch_details()




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

def add_genre():
    name = input("Enter genre name: ")
    description = input("Enter genre description: ")
    new_genre = Genre(name, description)
    new_genre.save_to_db()

def view_genre_details(name):
    genre = Genre(name, '') 
    genre.fetch_details()



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

# Function to handle adding books with specialized types
def add_specialized_book():
    book_type = input("Enter book type (Fiction, Non-Fiction, Mystery): ")
    title = input("Enter book title: ")
    author = input("Enter book author ID: ")
    isbn = input("Enter book ISBN: ")
    genre = input("Enter book genre ID: ")
    publication_date = input("Enter publication date (YYYY-MM-DD): ")

    if book_type.lower() == "fiction":
        fiction_type = input("Enter fiction type: ")
        book = FictionBook(title, author, isbn, genre, publication_date, fiction_type)
    elif book_type.lower() == "non-fiction":
        subject = input("Enter the subject: ")
        book = NonFictionBook(title, author, isbn, genre, publication_date, subject)
    elif book_type.lower() == "mystery":
        mystery_elements = input("Enter mystery elements: ")
        book = MysteryBook(title, author, isbn, genre, publication_date, mystery_elements)
    else:
        print("Invalid book type provided.")
        return

    book.save_to_db()
    print(f"{book_type} book added successfully.")






def add_book():
    print("Adding a new book. Please specify the type of book:")
    book_type = input("Enter book type (Fiction, Non-Fiction, Mystery): ")
    title = input("Enter book title: ")
    author_id = input("Enter author ID (please ensure the author exists in the database): ")
    isbn = input("Enter book ISBN: ")
    genre_id = input("Enter genre ID (please ensure the genre exists in the database): ")
    publication_date = input("Enter publication date (YYYY-MM-DD): ")


    conn = get_connection()
    cursor = conn.cursor()

    fiction_type = subject = mystery_elements = None

    if book_type.lower() == 'fiction':
        fiction_type = input("Enter fiction type (e.g., Fantasy, Sci-Fi, etc.): ")
    elif book_type.lower() == 'non-fiction':
        subject = input("Enter the subject of the non-fiction book: ")
    elif book_type.lower() == 'mystery':
        mystery_elements = input("Enter key elements of the mystery (e.g., Crime, Detective, etc.): ")

    sql = """
    INSERT INTO books (title, author_id, genre_id, isbn, publication_date, availability, fiction_type, subject, mystery_elements)
    VALUES (%s, %s, %s, %s, %s, 'Available', %s, %s, %s)
    """
    try:
        cursor.execute(sql, (title, author_id, genre_id, isbn, publication_date, fiction_type, subject, mystery_elements))
        conn.commit()
        print("Book added successfully.")
    except mysql.connector.Error as err:
        print("Failed to add book:", err)
        conn.rollback()
    finally:
        conn.close()





def display_all_books():
    conn = get_connection()
    cursor = conn.cursor()
    # This query should be updated to join with other tables if those tables contain necessary additional information
    query = """
    SELECT b.id, b.title, a.name as author_name, g.name as genre_name, b.isbn, b.publication_date, b.availability,
           b.fiction_type, b.subject, b.mystery_elements
    FROM books b
    LEFT JOIN authors a ON b.author_id = a.id
    LEFT JOIN genres g ON b.genre_id = g.id;
    """
    cursor.execute(query)
    books = cursor.fetchall()
    if not books:
        print("No books available.")
        return
    
    print("Displaying all books:")
    for book in books:
        print(f"\nBook ID: {book[0]}")
        print(f"Title: {book[1]}")
        print(f"Author: {book[2]}")
        print(f"Genre: {book[3]}")
        print(f"ISBN: {book[4]}")
        print(f"Publication Date: {book[5]}")
        print(f"Availability: {book[6]}")
        if book[7]:  # Fiction type
            print(f"Fiction Type: {book[7]}")
        if book[8]:  # Non-Fiction subject
            print(f"Subject: {book[8]}")
        if book[9]:  # Mystery elements
            print(f"Mystery Elements: {book[9]}")
    conn.close()


def add_user():
    name = input("Enter user name: ")
    library_id = input("Enter library ID: ")

    conn = get_connection()
    cursor = conn.cursor()
    try:
        query = "INSERT INTO users (name, library_id) VALUES (%s, %s);"
        cursor.execute(query, (name, library_id))
        conn.commit()
        print(f"User {name} added successfully.")
    except mysql.connector.Error as err:
        print("Failed to insert user:", err)
    finally:
        if conn.is_connected():
            conn.close()


def display_all_users():
    conn = get_connection()
    cursor = conn.cursor()
    query = "SELECT id, name, library_id FROM users;"
    cursor.execute(query)
    users = cursor.fetchall()
    
    if not users:
        print("No users available.")
        return
    
    print("Displaying all users:")
    for user in users:
        print(f"\nUser ID: {user[0]}")
        print(f"Name: {user[1]}")
        print(f"Library ID: {user[2]}")
    
    conn.close()



def add_author():
    name = input("Enter author's name: ")
    biography = input("Enter author's biography: ")

    conn = get_connection()
    cursor = conn.cursor()
    try:
        query = "INSERT INTO authors (name, biography) VALUES (%s, %s);"
        cursor.execute(query, (name, biography))
        conn.commit()
        print(f"Author {name} added successfully.")
    except mysql.connector.Error as err:
        print("Failed to insert author:", err)
    finally:
        if conn.is_connected():
            conn.close()



def display_all_authors():
    conn = get_connection()
    cursor = conn.cursor()
    query = "SELECT id, name, biography FROM authors;"
    cursor.execute(query)
    authors = cursor.fetchall()
    
    if not authors:
        print("No authors available.")
        return
    
    print("Displaying all authors:")
    for author in authors:
        print(f"\nAuthor ID: {author[0]}")
        print(f"Name: {author[1]}")
        print(f"Biography: {author[2]}")
    
    conn.close()


def add_genre():
    name = input("Enter genre name: ")
    description = input("Enter genre description: ")

    # Establish a connection and insert the new genre into the database
    conn = get_connection()
    cursor = conn.cursor()
    try:
        query = "INSERT INTO genres (name, description) VALUES (%s, %s);"
        cursor.execute(query, (name, description))
        conn.commit()
        print(f"Genre '{name}' added successfully.")
    except mysql.connector.Error as err:
        print("Failed to insert genre:", err)
    finally:
        if conn.is_connected():
            conn.close()

def display_all_genres():
    conn = get_connection()
    cursor = conn.cursor()
    query = "SELECT id, name, description FROM genres;"
    cursor.execute(query)
    genres = cursor.fetchall()
    
    if not genres:
        print("No genres available.")
        return
    
    print("Displaying all genres:")
    for genre in genres:
        print(f"\nGenre ID: {genre[0]}")
        print(f"Name: {genre[1]}")
        print(f"Description: {genre[2]}")
    
    conn.close()


# Implementing borrow, return, and search functionalities for books, and viewing details for users, authors, and genres


def borrow_book():
    isbn = input("Enter the ISBN of the book you wish to borrow: ")
    user_id = input("Enter your User ID: ")
    
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT id FROM books WHERE isbn = %s", (isbn,))
        result = cursor.fetchone()
        if result:
            book_id = result[0]

            cursor.execute("SELECT availability FROM books WHERE id = %s", (book_id,))
            availability = cursor.fetchone()[0]
            if availability == 'Available':
                cursor.execute("INSERT INTO borrowed_books (user_id, book_id, borrow_date) VALUES (%s, %s, CURDATE())", (user_id, book_id))
                cursor.execute("UPDATE books SET availability = 'Borrowed' WHERE id = %s", (book_id,))
                conn.commit()
                print("Book successfully borrowed.")
            else:
                print("This book is currently unavailable for borrowing.")
        else:
            print("No book found with the given ISBN.")

    except mysql.connector.Error as err:
        print("Failed to borrow book:", err)
        conn.rollback()

    finally:
        if conn.is_connected():
            conn.close()



def return_book():
    isbn = input("Enter the ISBN of the book you wish to return: ")
    
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT id FROM books WHERE isbn = %s", (isbn,))
        result = cursor.fetchone()
        if result:
            book_id = result[0]
            cursor.execute("SELECT * FROM borrowed_books WHERE book_id = %s AND return_date IS NULL", (book_id,))
            borrowed_book = cursor.fetchone()
            if borrowed_book:
                cursor.execute("UPDATE borrowed_books SET return_date = CURDATE() WHERE book_id = %s AND return_date IS NULL", (book_id,))
                cursor.execute("UPDATE books SET availability = 'Available' WHERE id = %s", (book_id,))
                conn.commit()
                print("Book successfully returned.")
            else:
                print("This book was not borrowed or already returned.")
        else:
            print("No book found with the given ISBN.")
    except mysql.connector.Error as err:
        print("Failed to return book:", err)
        conn.rollback()
    finally:
        if conn.is_connected():
            conn.close()


def search_book():
    search_query = input("Enter the ISBN or title of the book to search for: ")
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT title, author_id, isbn, publication_date, availability FROM books WHERE isbn = %s OR title LIKE %s", (search_query, '%' + search_query + '%'))
    books = cursor.fetchall()

    if books:
        print("Found books:")
        for book in books:
            print(f"Title: {book[0]}, ISBN: {book[2]}, Publication Date: {book[3]}, Availability: {book[4]}")
    else:
        print("No books found matching your criteria.")

    conn.close()


def view_author_details():
    author_name = input("Enter the author's name: ")
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id, name, biography FROM authors WHERE name = %s", (author_name,))
    author = cursor.fetchone()

    if author:
        print(f"Author ID: {author[0]}, Name: {author[1]}, Biography: {author[2]}")
    else:
        print("Author not found.")
    
    conn.close()



def view_author_details():
    author_name = input("Enter the author's name: ")
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id, name, biography FROM authors WHERE name = %s", (author_name,))
    author = cursor.fetchone()

    if author:
        print(f"Author ID: {author[0]}, Name: {author[1]}, Biography: {author[2]}")
    else:
        print("Author not found.")
    
    conn.close()


def view_genre_details():
    genre_name = input("Enter the genre name: ")
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id, name, description FROM genres WHERE name = %s", (genre_name,))
    genre = cursor.fetchone()

    if genre:
        print(f"Genre ID: {genre[0]}, Name: {genre[1]}, Description: {genre[2]}")
    else:
        print("Genre not found.")
    
    conn.close()



# Expanding the system to include update and delete functionalities for books, users, authors, and genres

def update_book():
    isbn = input("Enter the ISBN of the book to update: ")
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT title, author_id, genre_id, publication_date FROM books WHERE isbn = %s", (isbn,))
    book = cursor.fetchone()

    if not book:
        print("No book found with the provided ISBN.")
        conn.close()
        return

    new_title = input(f"Enter new title (Current: {book[0]}): ")
    new_author_id = input(f"Enter new author ID (Current: {book[1]}): ")
    new_genre_id = input(f"Enter new genre ID (Current: {book[2]}): ")
    new_publication_date = input(f"Enter new publication date (YYYY-MM-DD) (Current: {book[3]}): ")

    cursor.execute("""
        UPDATE books SET title = %s, author_id = %s, genre_id = %s, publication_date = %s 
        WHERE isbn = %s
    """, (new_title, new_author_id, new_genre_id, new_publication_date, isbn))
    conn.commit()
    print("Book details updated successfully.")
    
    conn.close()

def delete_book():
    isbn = input("Enter the ISBN of the book to delete: ")
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM books WHERE isbn = %s", (isbn,))
    if cursor.rowcount:
        conn.commit()
        print("Book deleted successfully.")
    else:
        print("No book found with the provided ISBN or unable to delete.")

    conn.close()



def update_user():
    library_id = input("Enter the library ID of the user to update: ")
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM users WHERE library_id = %s", (library_id,))
    user = cursor.fetchone()

    if not user:
        print("No user found with the provided library ID.")
        conn.close()
        return

    new_name = input(f"Enter new name (Current: {user[0]}): ")

    cursor.execute("UPDATE users SET name = %s WHERE library_id = %s", (new_name, library_id))
    conn.commit()
    print("User details updated successfully.")
    
    conn.close()


def delete_user():
    library_id = input("Enter the library ID of the user to delete: ")
    conn = get_connection()
    cursor = conn.cursor()


    cursor.execute("DELETE FROM users WHERE library_id = %s", (library_id,))
    if cursor.rowcount:
        conn.commit()
        print("User deleted successfully.")
    else:
        print("No user found with the provided library ID or unable to delete.")

    conn.close()

def view_user_details():
    """
    Retrieves and displays the details of a user from the library system based on their library ID.
    """
    library_id = input("Enter the library ID of the user: ")
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT id, name, library_id FROM users WHERE library_id = %s", (library_id,))
        user = cursor.fetchone()

        if user:
            print("\nUser Details:")
            print(f"User ID: {user[0]}")
            print(f"Name: {user[1]}")
            print(f"Library ID: {user[2]}")
        else:
            print("No user found with the library ID:", library_id)

    except mysql.connector.Error as err:
        print("Error retrieving user details:", str(err))

    finally:
        if conn.is_connected():
            conn.close()



def update_author():
    author_name = input("Enter the author's name to update: ")
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT biography FROM authors WHERE name = %s", (author_name,))
    author = cursor.fetchone()

    if not author:
        print("No author found with that name.")
        conn.close()
        return

    new_biography = input(f"Enter new biography (Current: {author[0]}): ")

    cursor.execute("UPDATE authors SET biography = %s WHERE name = %s", (new_biography, author_name))
    conn.commit()
    print("Author details updated successfully.")
    
    conn.close()

def delete_author():
    author_name = input("Enter the author's name to delete: ")
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM authors WHERE name = %s", (author_name,))
    if cursor.rowcount:
        conn.commit()
        print("Author deleted successfully.")
    else:
        print("No author found with that name or unable to delete.")

    conn.close()


def update_genre():
    genre_name = input("Enter the genre name to update: ")
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT description FROM genres WHERE name = %s", (genre_name,))
    genre = cursor.fetchone()

    if not genre:
        print("No genre found with that name.")
        conn.close()
        return

    new_description = input(f"Enter new description (Current: {genre[0]}): ")

    cursor.execute("UPDATE genres SET description = %s WHERE name = %s", (new_description, genre_name))
    conn.commit()
    print("Genre details updated successfully.")
    
    conn.close()


def delete_genre():
    genre_name = input("Enter the genre name to delete: ")
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM genres WHERE name = %s", (genre_name,))
    if cursor.rowcount:
        conn.commit()
        print("Genre deleted successfully.")
    else:
        print("No genre found with that name or unable to delete.")

    conn.close()



# Validation functions

def valid_isbn(isbn):
    """ Validate ISBN with either 10 or 13 digits. """
    return bool(re.match(r'^\d{10}(\d{3})?$', isbn))

def valid_library_id(library_id):
    """ Validate that the library ID is numeric. """
    return bool(re.match(r'^\d+$', library_id))

def valid_name(name):
    """ Validate that the name contains only letters and spaces, and starts with a letter. """
    return bool(re.match(r'^[A-Za-z][A-Za-z\s]*$', name))

from datetime import datetime

def valid_publication_date(date):
    """ Validate that the date is in the format YYYY-MM-DD and is a valid date. """
    try:
        datetime.strptime(date, '%Y-%m-%d')
        return True
    except ValueError:
        return False

def valid_book_type(book_type):
    """ Validate that the book type is one of 'Fiction', 'Non-Fiction', or 'Mystery'. """
    return book_type.lower() in ['fiction', 'non-fiction', 'mystery']

def valid_description(description):
    """ Validate that the description is not empty and meets a minimum length requirement. """
    return len(description.strip()) > 0 and len(description.strip()) >= 20



# UI

def return_to_main_menu():
    """
    Offers the user the option to return to the main menu or exit the system.
    This function provides a prompt and handles the user's choice.
    """
    while True:
        user_choice = input("Press 'M' to return to the Main Menu or 'Q' to quit: ").upper()
        if user_choice == 'M':
            print("Returning to the Main Menu...\n")
            break  
        elif user_choice == 'Q':
            print("Exiting the system. Thank you for using the Library Management System.")
            exit(0)  
        else:
            print("Invalid input. Please enter 'M' to go to the Main Menu or 'Q' to quit.")


# Menu and start functions

def main_menu():
    print("""
Welcome to the Library Management System!
Main Menu:
1. Book Operations
2. User Operations
3. Author Operations
4. Genre Operations
5. Quit
""")
    choice = input("Enter your choice (1-5): ")
    return choice

def book_menu():
    print("""
Book Operations:
1. Add a new book
2. Borrow a book
3. Return a book
4. Search for a book
5. Display all books
6. Update a book
7. Delete a book
""")
    choice = input("Enter your choice (1-7): ")
    return choice

def user_menu():
    print("""
User Operations:
1. Add a new user
2. View user details
3. Display all users
4. Update user details
5. Delete a user
""")
    choice = input("Enter your choice (1-5): ")
    return choice

def author_menu():
    print("""
Author Operations:
1. Add a new author
2. View author details
3. Display all authors
4. Update author details
5. Delete an author
""")
    choice = input("Enter your choice (1-5): ")
    return choice

def genre_menu():
    print("""
Genre Operations:
1. Add a new genre
2. View genre details
3. Display all genres
4. Update genre details
5. Delete a genre
""")
    choice = input("Enter your choice (1-5): ")
    return choice

# 'Handle' Functions to  navegate the UI

def handle_book_operations():
    while True:
        print("\nBook Operations:")
        print("1. Add a new book")
        print("2. Borrow a book")
        print("3. Return a book")
        print("4. Search for a book")
        print("5. Display all books")
        print("6. Update a book")
        print("7. Delete a book")
        print("8. Return to Main Menu")
        choice = input("Enter your choice: ")

        if choice == '1':
            add_book()
        elif choice == '2':
            borrow_book()
        elif choice == '3':
            return_book()
        elif choice == '4':
            search_book()
        elif choice == '5':
            display_all_books()
        elif choice == '6':
            update_book()
        elif choice == '7':
            delete_book()
        elif choice == '8':
            break
        else:
            print("Invalid choice. Please try again.")
        return_to_main_menu()

def handle_user_operations():
    while True:
        print("\nUser Operations:")
        print("1. Add a new user")
        print("2. View user details")
        print("3. Display all users")
        print("4. Update user details")
        print("5. Delete a user")
        print("6. Return to Main Menu")
        choice = input("Enter your choice: ")

        if choice == '1':
            add_user()
        elif choice == '2':
            view_user_details()
        elif choice == '3':
            display_all_users()
        elif choice == '4':
            update_user()
        elif choice == '5':
            delete_user()
        elif choice == '6':
            break
        else:
            print("Invalid choice. Please try again.")
        return_to_main_menu()

def handle_author_operations():
    while True:
        print("\nAuthor Operations:")
        print("1. Add a new author")
        print("2. View author details")
        print("3. Display all authors")
        print("4. Update author details")
        print("5. Delete an author")
        print("6. Return to Main Menu")
        choice = input("Enter your choice: ")

        if choice == '1':
            add_author()
        elif choice == '2':
            view_author_details()
        elif choice == '3':
            display_all_authors()
        elif choice == '4':
            update_author()
        elif choice == '5':
            delete_author()
        elif choice == '6':
            break
        else:
            print("Invalid choice. Please try again.")
        return_to_main_menu()




def handle_genre_operations():
    while True:
        print("\nGenre Operations:")
        print("1. Add a new genre")
        print("2. View genre details")
        print("3. Display all genres")
        print("4. Update genre details")
        print("5. Delete a genre")
        print("6. Return to Main Menu")
        choice = input("Enter your choice: ")

        if choice == '1':
            add_genre()
        elif choice == '2':
            view_genre_details()
        elif choice == '3':
            display_all_genres()
        elif choice == '4':
            update_genre()
        elif choice == '5':
            delete_genre()
        elif choice == '6':
            break
        else:
            print("Invalid choice. Please try again.")
        return_to_main_menu()



# Startup testing

def test_database_connection():
    try:
        conn = get_connection()
        if conn.is_connected():
            print("Database connection test passed.")
            conn.close()
        else:
            print("Database connection test failed.")
    except Exception as e:
        print("Database connection test failed with an error:", str(e))

def test_initial_data_fetch():
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM books LIMIT 1;")
        if cursor.fetchone():
            print("Initial data fetch test for books passed.")
        else:
            print("No data found in books table.")

        cursor.execute("SELECT * FROM users LIMIT 1;")
        if cursor.fetchone():
            print("Initial data fetch test for users passed.")
        else:
            print("No data found in users table.")

        cursor.execute("SELECT * FROM authors LIMIT 1;")
        if cursor.fetchone():
            print("Initial data fetch test for authors passed.")
        else:
            print("No data found in authors table.")

        cursor.execute("SELECT * FROM genres LIMIT 1;")
        if cursor.fetchone():
            print("Initial data fetch test for genres passed.")
        else:
            print("No data found in genres table.")
    except mysql.connector.Error as err:
        print("Initial data fetch test failed:", err)
    finally:
        conn.close()

def test_operational_readiness():
    print("Testing add and display functionalities...")
    try:
        add_book()  # Assume add_book asks for inputs directly and doesn't require parameters here
        display_all_books()
        add_user()
        display_all_users()
        print("Operational readiness tests passed. All add and display functions are operational.")
    except Exception as e:
        print("Operational readiness tests failed:", str(e))






# Integrating load operations to initialize the system with data from JSON files at startup



def start_system():
    while True:
        print("\nWelcome to the Library Management System!")
        print("Main Menu:")
        print("1. Book Operations")
        print("2. User Operations")
        print("3. Author Operations")
        print("4. Genre Operations")
        print("5. Quit")

        choice = input("Enter your choice (1-5): ")

        if choice == '1':
            handle_book_operations()
        elif choice == '2':
            handle_user_operations()
        elif choice == '3':
            handle_author_operations()
        elif choice == '4':
            handle_genre_operations()
        elif choice == '5':
            print("Thank you for using the Library Management System.")
            break
        else:
            print("Invalid choice. Please try again.")

        if input("Return to Main Menu? (yes/no): ").lower() != 'yes':
            print("Exiting system...")
            break

def run_startup_tests():
    print("Running startup tests...")
    test_database_connection()
    test_initial_data_fetch()
    test_operational_readiness()
    print("All startup tests passed successfully.")

def main():
    try:
        # run_startup_tests()  # Ensuring all systems are go before starting
        start_system()
    except Exception as e:
        print(f"An error occurred during system startup: {e}")
    finally:
        print("System shutdown.")

if __name__ == "__main__":
    main()



