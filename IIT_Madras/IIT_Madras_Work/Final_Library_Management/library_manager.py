## Rajendra Bichu. 
## Date : 8.11.2025  Version 1.0 , Purpose a simple library management system.

##========================================================================================

#Import the packages needed

import datetime
from collections import defaultdict

# -----------------------------
# Data Structures
# -----------------------------
books = []      # List of dictionaries for book records
members = []    # List of dictionaries for member records
borrow_history = []  # List of (member_name, book_title, genre) for analytics

# -----------------------------
# Log books transaction
# -----------------------------
def log_book_trx(action, details):
    """Logs every transaction into a text file with timestamp and append it to a simple log file"""
    with open("library_record.txt", "a") as f:
        time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"[{time}] {action}: {details}\n")

# -----------------------------
# various functions for books management 
# -----------------------------

def add_book(book_id, book_title, book_author, genre, number_copies):
    """Adds a new book with genre."""
    for book in books:
        if book["id"] == book_id:
            print("Book with this ID already exists!")
            return
    books.append({
	"id": book_id,
        "book_title": book_title,
        "book_author": book_author,
        "number_copies": number_copies,
        "genre": genre,
        "issued_count": 0  
    })
    print(f"Book '{book_title}' added successfully!")
    log_book_trx("Add Book", f"{book_title} by {book_author} (number_copies: {number_copies})")


def display_book_records():
    """Displays all books in the library."""
    if not books:
        print(" No books in the library yet.")
        return
    print("\nAvailable Books:")
    print("-" * 60)
    print(f"{'ID':<5} {'book_title':<25} {'book_author':<20} {'number_copies':<8}")
    print("-" * 60)
    for book in books:
        print(f"{book['id']:<5} {book['book_title']:<25} {book['book_author']:<20} {book['number_copies']:<8}")
    print("-" * 60)

# -----------------------------
# Member Functions
# -----------------------------
def add_member(member_id, name, age, mobile):
    """Adds a new member to the library."""
    for member in members:
        if member["member_id"] == member_id:
            print("   Member with this ID already exists!")
            return
    members.append({
        "member_id": member_id,
        "member_name": name,
        "member_age": age,
        "member_mobile": mobile,
        "has_borrowed": False,
        "borrowed_book": None
    })
    print(f" Member '{name}' added successfully!")
    log_book_trx("Add Member", f"{name} (ID: {member_id})")

def display_members():
    """Displays all members and their book borrowed status."""
    if not members:
        print(" No members registered yet.")
        return
    print("\nLibrary Members:")
    print("-" * 75)
    print(f"{'ID':<10} {'Name':<20} {'Age':<5} {'Mobile':<15} {'Borrowed':<10} {'Book':<20}")
    print("-" * 75)
    for m in members:
        status = "Yes" if m["has_borrowed"] else "No"
        book_book_title = m["borrowed_book"] if m["borrowed_book"] else "-"
        print(f"{m['member_id']:<10} {m['member_name']:<20} {m['member_age']:<5} {m['member_mobile']:<15} {status:<10} {book_book_title:<20}")
    print("-" * 75)

# -----------------------------
# Borrow / Return Functions
# -----------------------------
def borrow_book(book_id, member_id):
    """Borrow a single book by member ID."""
    # Check member validity
    for member in members:
        if member["member_id"] == member_id:
            if member["has_borrowed"]:
                print(f"   Member '{member['member_name']}' has already borrowed a book!")
                return
            # Find book
            for book in books:
                if book["id"] == book_id:
                    if book["number_copies"] > 0:
                        book["number_copies"] -= 1
                        member["has_borrowed"] = True
                        member["borrowed_book"] = book["book_title"]
                        borrow_history.append((member["member_name"], book["book_title"], book["genre"]))
                        print(f"   '{book['book_title']}' borrowed by {member['member_name']}.")
                        log_book_trx("Borrow Book", f"{member['member_name']} borrowed '{book['book_title']}'")
                        return
                    else:
                        print(f"   '{book['book_title']}' is not available right now.")
                        return
            print("   Book not found.")
            return
    print("   Member not found.")

def return_book(member_id):
    """Return a borrowed book."""
    for member in members:
        if member["member_id"] == member_id:
            if not member["has_borrowed"]:
                print(f"   Member '{member['member_name']}' has no borrowed books.")
                return
            # Find the borrowed book
            borrowed_book_title = member["borrowed_book"]
            for book in books:
                if book["book_title"] == borrowed_book_title:
                    book["number_copies"] += 1
                    member["has_borrowed"] = False
                    member["borrowed_book"] = None
                    print(f" '{book['book_title']}' returned by {member['member_name']}.")
                    log_book_trx("Return Book", f"{member['member_name']} returned '{book['book_title']}'")
                    return
            print("⚠️ Book record missing for return!")
            return
    print("   Member not found.")

def show_borrowed_books():
    """Shows all members who have borrowed books."""
    borrowed = [m for m in members if m["has_borrowed"]]
    if not borrowed:
        print(" No books currently borrowed.")
        return
    print("\nBorrowed Books List:")
    print("-" * 70)
    print(f"{'Member ID':<10} {'Member Name':<20} {'Book book_title':<30}")
    print("-" * 70)
    for m in borrowed:
        print(f"{m['member_id']:<10} {m['member_name']:<20} {m['borrowed_book']:<30}")
    print("-" * 70)


def show_books_by_genre(genre):
    """Show all books in a given genre."""
    genre_books = [b for b in books if b["genre"].lower() == genre.lower()]
    if not genre_books:
        print(f"  No books found in genre '{genre}'.")
        return
    print(f"\n Books in Genre: {genre}")
    print("-" * 60)
    print(f"{'Title':<25} {'Author':<20} {'Copies':<8}")
    print("-" * 60)
    for b in genre_books:
        print(f"{b['book_title']:<25} {b['book_author']:<20} {b['number_copies']:<8}")
    print("-" * 60)

def search_book_by_author(author):
    """Search for books by a specific author."""
    found = [b for b in books if author.lower() in b["book_author"].lower()]
    if not found:
        print(f"  No books found by author '{author}'.")
        return
    print(f"\n   Books by '{author}':")
    for b in found:
        print(f"- {b['book_title']} ({b['genre']}) - Copies: {b['number_copies']}")

def search_book_by_title(title):
    """Search for books by title or partial title."""
    found = [b for b in books if title.lower() in b["book_title"].lower()]
    if not found:
        print(f"  No books found with title containing '{title}'.")
        return
    print(f"\n  Books matching '{title}':")
    for b in found:
        print(f"- {b['book_title']} by {b['book_author']} ({b['genre']}) - Copies: {b['number_copies']}")


def list_members_by_book(title):
    """Show which members have borrowed a particular book."""
    borrowers = [
        m.get("member_name", "<unknown>")
        for m in members
        if m.get("borrowed_book") and title.casefold() in m["borrowed_book"].casefold()
    ]
    if not borrowers:
        print(f"  No members have borrowed '{title}'.")
        return []
    print(f"\n  Members who borrowed '{title}':")
    for b in borrowers:
        print(f"- {b}")
    return borrowers

def display_most_popular_genre():
    """Display the most popular genre based on borrowed books."""
    if not borrow_history:
        print("   No borrowing history yet.")
        return
    genre_count = defaultdict(int)
    for _, _, genre in borrow_history:
        genre_count[genre] += 1
    most_popular = max(genre_count, key=genre_count.get)
    print(f"  Most Popular Genre: {most_popular} ({genre_count[most_popular]} issues)")
    log_book_trx("Popular Genre", f"{most_popular} ({genre_count[most_popular]} issues)")



# -----------------------------
# Main Menu
# -----------------------------

def main():
    while True:
        print("\n===Library Management System ===")
        print("1. Add Book")
        print("2. Display All Books")
        print("3. Add Member")
        print("4. Display Members")
        print("5. Borrow Book")
        print("6. Return Book")
        print("7. Show Books by Genre")
        print("8. Search Book by Author")
        print("9. Search Book by Title")
        print("10. List Members by Book")
        print("11. Display Most Popular Genre")
        print("12. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            book_id = input("Enter Book ID: ")
            title = input("Enter Book Title: ")
            author = input("Enter Author Name: ")
            genre = input("Enter Genre: ")
            copies = int(input("Enter Number of Copies: "))
            add_book(book_id, title, author, genre, copies)

        elif choice == "2":
            display_book_records()

        elif choice == "3":
            member_id = input("Enter Member ID: ")
            name = input("Enter Member Name: ")
            age = input("Enter Member Age: ")
            mobile = input("Enter Member Mobile Number: ")
            add_member(member_id, name, age, mobile)

        elif choice == "4":
            display_members()

        elif choice == "5":
            member_id = input("Enter Member ID: ")
            book_id = input("Enter Book ID: ")
            borrow_book(book_id, member_id)

        elif choice == "6":
            member_id = input("Enter Member ID: ")
            return_book(member_id)

        elif choice == "7":
            genre = input("Enter Genre to Search: ")
            show_books_by_genre(genre)

        elif choice == "8":
            author = input("Enter Author Name: ")
            search_book_by_author(author)

        elif choice == "9":
            title = input("Enter Title or Part of Title: ")
            search_book_by_title(title)

        elif choice == "10":
            title = input("Enter Book Title: ")
            list_members_by_book(title)

        elif choice == "11":
            display_most_popular_genre()

        elif choice == "12":
            print("Exiting Library System. Goodbye!")
            break
        else:
            print("Invalid choice, please enter a proper choice.")

# Run
if __name__ == "__main__":
    main()
