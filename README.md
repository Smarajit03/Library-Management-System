📚 Library Management System (Python + CSV)

A console-based Library Management System built in Python that uses CSV files as a mini-database.
The system models a many-to-many relationship between members and loans, supports secure password handling with bcrypt, implements CRUD operations, due-date logic, and includes automated tests with pytest.

🚀 Features
👩‍🏫 Librarian Role

Add / Remove books

Register new members

Issue books (due date = 14 days from issue)

Return books (updates ReturnDate, restores copy)

View overdue list

👤 Member Role

Search catalogue by title/author keywords

Borrow books (if available)

View personal loan history

🗂 Data Storage (CSV Mini-Database)

books.csv → ISBN, Title, Author, CopiesTotal, CopiesAvailable

members.csv → MemberID, Name, PasswordHash, Email, JoinDate

loans.csv → LoanID, MemberID, ISBN, IssueDate, DueDate, ReturnDate

Passwords are securely stored using bcrypt hashing (never plain-text).

🔒 Authentication

Librarian login with bcrypt-hashed password (default: admin123)

Members register with email + password → stored as bcrypt hash

🧪 Testing

Automated tests are written with pytest.
The core test scenario:

Issue a book → copies decrease

Return the book → copies restore, ReturnDate filled

Run tests:

pytest -q

🧩 Project Structure
library_mgmt_project/
│── main.py        # Entry point (role menus)
│── models.py      # Dataclasses (Book, Member, Loan)
│── storage.py     # CSV read/write helpers
│── auth.py        # bcrypt login & registration
│── logic.py       # Business rules (issue, return, overdue)
│── ui.py          # Console printing helpers
│── data/          # Sample CSV files
│── tests/         # pytest tests
│── requirements.txt
│── README.md
