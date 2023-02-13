# Sets formating values
RED = '\033[91m'
COLRESET = '\033[0m'
BOLD = '\033[1m'
GREEN = '\033[92m'
BLUE = '\033[94m'
ITALIC = '\033[3m'

#=========== Database & table setup section ============#
# This imports sqlite and creates ebookstore database
import sqlite3
db = sqlite3.connect('ebookstore')

# Get a coursor object
cursor = db.cursor()

# This creates table books
# Assigns primary key, sets data types
cursor.execute("""CREATE TABLE books(
                  id INTEGER PRIMARY KEY,
                  Title TEXT,
                  Author TEXT,
                  Qty INTEGER)
                  """)
db.commit()

# This creates list of books to be added to the database
books_list = [(3001, "A Tale of Two Cities", "Charles Dickens", 30),
              (3002, "Harry Potter and the Philosopher's Stone", "J.K. Rowling", 40),
              (3003, 'The Lion, the Witch and the Wardrobe', 'C. S. Lewis', 25),
              (3004, "The Lord of the Rings", "J.R.R Tolkien", 37),
              (3005, "Alice in Wonderland", "Lewis Carroll", 12),
              ]

# Adds data from the books_list to the books table
cursor.executemany('''INSERT INTO books(id, Title, Author, Qty)
                      VALUES(?,?,?,?)''', 
                      books_list)
db.commit()


#=========== Functions section ============#

# Function to add new book to the books table
def add_book():

    # Asks user for id, Title, Author & Qty
    try:
        print("Please enter the following details: ")
        book_id = int(input("id: \t"))
        book_title = str(input("Title:  "))
        book_author = str(input("Author: "))
        book_qty = int(input("Qty: \t"))

        # This checks if id is unique, prints error message if not
        cursor.execute("""SELECT Title FROM books
                    WHERE id=?""", 
                    [(book_id)])
        book = cursor.fetchall()
        if book != []:
            print(f"{RED}Book id already exists{COLRESET} \n")
        
        # If id is unique, adds book to the book table
        else:
            cursor.execute('''INSERT INTO books(id, Title, Author, Qty)
                            VALUES(?,?,?,?)''', 
                            (book_id,book_title,book_author,book_qty))
            db.commit()
            print(f"{BLUE}Book has been added{COLRESET} \n")

    # This errors if values aren't correct type
    except ValueError:
        print(f"{RED}Please enter correct details {COLRESET}")


# Function to update book details by searching for id
def update_by_id():  
    try:
        # Requests all new details for book
        print("Please enter the following details: ")
        book_id = int(input(f"{BLUE}Id: \t{COLRESET}"))
        book_title = str(input("Title:  "))
        book_author = str(input("Author: "))
        book_qty = int(input("Qty: \t"))

        # Checks if book exists, if it doesn't prints error message
        cursor.execute("""SELECT Title FROM books
                        WHERE id=?""", 
                        [(book_id)])
        book = cursor.fetchall()
        if book == []:
            print(f"{RED}Book not found{COLRESET} \n")

        # If book exists updates details and prints confirmation message
        else:
            cursor.execute("""UPDATE books
                        SET Title=?, Author=?, Qty=?
                        WHERE id=?""", 
                        ([book_title,book_author,book_qty,book_id]))
            db.commit()
            print(f"{BLUE}Details has been updated{COLRESET} \n")

    # This errors if values aren't correct type
    except ValueError:
        print(f"{RED}Please enter correct details {COLRESET}")


# Function to update book details by searching for title
def update_by_title():

    try:

        # Requests new book details from user
        # Keeps id the same
        print("Please enter the following details: ")
        book_title = str(input(f"{BLUE}Title:  {COLRESET}"))
        book_author = str(input("Author: "))
        book_qty = int(input("Qty: \t"))

        # Checks if book exists, prints error message if it doesn't
        cursor.execute("""SELECT id FROM books
                        WHERE Title=?""", 
                        [(book_title)])
        book = cursor.fetchall()
        if book == []:
            print(f"{RED}Book not found{COLRESET} \n")

        # If it exists then updates book details and prints message
        else:
            cursor.execute("""UPDATE books
                            SET Author=?, Qty=?
                            WHERE Title=?""", 
                            ([book_author,book_qty,book_title]))
            db.commit()
            print(f"{BLUE}Details has been updated{COLRESET} \n")

    # This errors if values aren't correct type
    except ValueError:
        print(f"{RED}Please enter correct details {COLRESET}")


# Function to delete book from the books table by using id
def delete_by_id():

    # Requests details of book to delete & checks if it exists
    book_id = [int(input(f"{BLUE}Please enter a book id: \t{COLRESET}"))]
    cursor.execute("""SELECT Title FROM books
                    WHERE id=?""", 
                    book_id)
    book = cursor.fetchall()

    # If book doesn't exist displays error message
    if book == []:
        print(f"{RED}Book not found{COLRESET} \n")
    
    # If it does exist deletes from the file and prints message
    else:
        cursor.execute("""DELETE FROM books
                        WHERE id= ?""", 
                        book_id)
        db.commit()
        print(f"{BLUE}Deleted{COLRESET} \n")


# Function to delete book from the books table by using title
def delete_by_title():

    # Requests details of book to delete & checks if it exists
    book_title = [str(input(f"{BLUE}Please enter a book title: \t{COLRESET}"))]
    cursor.execute("""SELECT id FROM books
                    WHERE Title=?""", 
                    book_title)
    book = cursor.fetchall()

    # If book doesn't exist displays error message
    if book == []:
        print(f"{RED}Book not found{COLRESET} \n")
    
    # If it does exist deletes from the file and prints message
    else:
        cursor.execute("""DELETE FROM books
                        WHERE title= ?""", 
                        book_title)
        db.commit()
        print(f"{BLUE}Deleted{COLRESET} \n")
    
    
# Function to search for a book by id
def search_by_id():

    # Requests book id and checks if it exists
    book_id = [int(input(f"{BLUE}Please enter a book id: \t{COLRESET}"))]
    cursor.execute("""SELECT Title, Author, Qty FROM books
                      WHERE id=?""", 
                      book_id)
    book = cursor.fetchall()

    # Prints error message if book doesn't exists
    if book == []:
        print(f"{RED}Book not found{COLRESET} \n")
    
    # If it does exist prints book details
    else:
        for i in book:
            print(f"Title:  {i[0]} \n"
                  f"Author: {i[1]} \n"
                  f"Qty: \t{i[2]} \n")


# Function to search for a book by title
def search_by_title():

    # Requests book title and checks if it exists
    book_title = [str(input(f"{BLUE}Please enter a book title: \t{COLRESET}"))]
    cursor.execute("""SELECT id, Author, Qty FROM books
                      WHERE title=?""", 
                      book_title)
    book = cursor.fetchall()
    
    # Prints error message if book doesn't exists
    if book == []:
        print(f"{RED}Book not found{COLRESET} \n")
    
    # If it does exist prints book details
    else:
        for i in book:
            print(f"id: \t{i[0]} \n"
                  f"Author: {i[1]} \n"
                  f"Qty: \t{i[2]} \n")





#=========== Main menu section ============#
while True:

    # Asks user to select menu option
    menu = int(input(f"""\n *** Menu ***
{ITALIC}Please choose from following options{COLRESET}
1 - Enter book
2 - Update book
3 - Delete book
4 - Search books
0 - Exit \n"""))

    # 1 - Add book, adds book details to the table
    if menu == 1:
        add_book()

    # 2 - Update book details
    # Asks if user wants to make an update based on id or title
    # Runs relevant function, errors if incorrect option selected
    elif menu == 2:
        search_option = input("What do you want to search by: (id/title) \n")
        if search_option == "id":
            update_by_id()
        elif search_option == "title":
            update_by_title()
        else:
            print("Please select correct option")
    
    # 3 - Delete book details
    # Asks if user wants to delete based on id or title
    # Runs relevant function, errors if incorrect option selected
    elif menu == 3:
        search_option = input("What do you want to search by: (id/title) \n")
        if search_option == "id":
            delete_by_id()
        elif search_option == "title":
            delete_by_title()
        else:
            print("Please select correct option")

    # 4 - Search book details
    # Asks if user wants to search based on id or title
    # Runs relevant function, errors if incorrect option selected
    elif menu == 4:
        search_option = input("What do you want to search by: (id/title) \n")
        if search_option == "id":
            search_by_id()
        elif search_option == "title":
            search_by_title()
        else:
            print("Please select correct option")
        
    # 0 - Closes database & exits file
    elif menu == 0:
        db.close()
        exit()

    # Displays error message if user selects incorrect option
    else:
        print("Please select correct option")



