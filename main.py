import argparse
import os
import uuid
from datetime import datetime, timedelta
from storage import load_books, save_books, load_loans, save_loans, load_members
from auth import register_member, login, session
from models import Book, Member, Loan

# Business logic functions
def add_book(data_dir):
    books = load_books(data_dir)
    isbn = input("ISBN: ")
    if any(b.ISBN == isbn for b in books):
        print("Book with this ISBN already exists.")
        return
    title = input("Title: ")
    author = input("Author: ")
    try:
        copies_total = int(input("Total copies: "))
        if copies_total < 1:
            raise ValueError
    except ValueError:
        print("Invalid copies number.")
        return
    new_book = Book(isbn, title, author, copies_total, copies_total)
    books.append(new_book)
    save_books(data_dir, books)
    print("Book added.")

def remove_book(data_dir):
    books = load_books(data_dir)
    loans = load_loans(data_dir)
    isbn = input("ISBN to remove: ")
    if any(l.ISBN == isbn and l.ReturnDate == '' for l in loans):
        print("Cannot remove book with active loans.")
        return
    books = [b for b in books if b.ISBN != isbn]
    save_books(data_dir, books)
    print("Book removed.")

def issue_book(data_dir, member_id):
    books = load_books(data_dir)
    loans = load_loans(data_dir)
    isbn = input("ISBN to issue: ")
    book = next((b for b in books if b.ISBN == isbn), None)
    if not book:
        print("Book not found.")
        return
    if book.CopiesAvailable < 1:
        print("No copies available.")
        return
    issue_date = datetime.today().strftime('%Y-%m-%d')
    due_date = (datetime.today() + timedelta(days=14)).strftime('%Y-%m-%d')
    loan_id = str(uuid.uuid4())[:8]
    new_loan = Loan(loan_id, member_id, isbn, issue_date, due_date, '')
    loans.append(new_loan)
    book.CopiesAvailable -= 1
    save_books(data_dir, books)
    save_loans(data_dir, loans)
    print(f"Book issued. Due on {due_date}.")

def return_book(data_dir, member_id):
    books = load_books(data_dir)
    loans = load_loans(data_dir)
    isbn = input("ISBN to return: ")
    loan = next((l for l in loans if l.MemberID == member_id and l.ISBN == isbn and l.ReturnDate == ''), None)
    if not loan:
        print("No active loan for this book.")
        return
    return_date = datetime.today().strftime('%Y-%m-%d')
    loan.ReturnDate = return_date
    book = next(b for b in books if b.ISBN == isbn)
    book.CopiesAvailable += 1
    save_books(data_dir, books)
    save_loans(data_dir, loans)
    print("Book returned.")

def view_overdue(data_dir):
    loans = load_loans(data_dir)
    today = datetime.today().date()
    overdue = [l for l in loans if l.ReturnDate == '' and datetime.strptime(l.DueDate, '%Y-%m-%d').date() < today]
    if not overdue:
        print("No overdue loans.")
        return
    print("Overdue Loans:")
    for loan in overdue:
        print(f"LoanID: {loan.LoanID}, MemberID: {loan.MemberID}, ISBN: {loan.ISBN}, Due: {loan.DueDate}")

def search_catalogue(data_dir, keyword):
    books = load_books(data_dir)
    results = [b for b in books if keyword.lower() in b.Title.lower() or keyword.lower() in b.Author.lower()]
    if not results:
        print("No results found.")
        return
    for book in results:
        print(f"ISBN: {book.ISBN}, Title: {book.Title}, Author: {book.Author}, Available: {book.CopiesAvailable}/{book.CopiesTotal}")

def view_my_loans(data_dir, member_id):
    loans = load_loans(data_dir)
    my_loans = [l for l in loans if l.MemberID == member_id]
    if not my_loans:
        print("No loans.")
        return
    for loan in my_loans:
        status = "Returned" if loan.ReturnDate else f"Due: {loan.DueDate}"
        print(f"LoanID: {loan.LoanID}, ISBN: {loan.ISBN}, Issue: {loan.IssueDate}, {status}")

# Menus
def librarian_menu(data_dir):
    while True:
        print("\n=== Librarian Dashboard ===")
        print("1. Add Book")
        print("2. Remove Book")
        print("3. Register Member")
        print("4. Issue Book")
        print("5. Return Book")
        print("6. Overdue List")
        print("7. Logout")
        choice = input("> ")
        if choice == '1':
            add_book(data_dir)
        elif choice == '2':
            remove_book(data_dir)
        elif choice == '3':
            register_member(data_dir)
        elif choice == '4':
            member_id = input("Member ID: ")
            issue_book(data_dir, member_id)
        elif choice == '5':
            member_id = input("Member ID: ")
            return_book(data_dir, member_id)
        elif choice == '6':
            view_overdue(data_dir)
        elif choice == '7':
            break
        else:
            print("Invalid choice.")

def member_menu(data_dir):
    while True:
        print("\n=== Member Dashboard ===")
        print("1. Search Catalogue")
        print("2. Borrow Book")
        print("3. My Loans")
        print("4. Logout")
        choice = input("> ")
        if choice == '1':
            keyword = input("Keyword (title/author): ")
            search_catalogue(data_dir, keyword)
        elif choice == '2':
            issue_book(data_dir, session['id'])
        elif choice == '3':
            view_my_loans(data_dir, session['id'])
        elif choice == '4':
            break
        else:
            print("Invalid choice.")

# Main entry point
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Library Management System")
    parser.add_argument('--data-dir', default='./data', help='Directory for data files')
    args = parser.parse_args()
    data_dir = args.data_dir
    os.makedirs(data_dir, exist_ok=True)

    while True:
        print("\n=== Library Management System ===")
        print("1. Login as Librarian")
        print("2. Login as Member")
        print("3. Exit")
        choice = input("> ")
        if choice == '1':
            if login(data_dir, 'librarian'):
                librarian_menu(data_dir)
        elif choice == '2':
            if login(data_dir, 'member'):
                member_menu(data_dir)
        elif choice == '3':
            break
        else:
            print("Invalid choice.")