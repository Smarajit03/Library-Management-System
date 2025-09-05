import csv
import os
from dataclasses import asdict
from models import Book, Member, Loan

def load_books(data_dir):
    books = []
    file_path = os.path.join(data_dir, 'books.csv')
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                books.append(Book(
                    ISBN=row['ISBN'],
                    Title=row['Title'],
                    Author=row['Author'],
                    CopiesTotal=int(row['CopiesTotal']),
                    CopiesAvailable=int(row['CopiesAvailable'])
                ))
    return books

def save_books(data_dir, books):
    file_path = os.path.join(data_dir, 'books.csv')
    with open(file_path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['ISBN', 'Title', 'Author', 'CopiesTotal', 'CopiesAvailable'])
        writer.writeheader()
        for book in books:
            writer.writerow(asdict(book))

def load_members(data_dir):
    members = []
    file_path = os.path.join(data_dir, 'members.csv')
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                members.append(Member(
                    MemberID=row['MemberID'],
                    Name=row['Name'],
                    PasswordHash=row['PasswordHash'],
                    Email=row['Email'],
                    JoinDate=row['JoinDate']
                ))
    return members

def save_members(data_dir, members):
    file_path = os.path.join(data_dir, 'members.csv')
    with open(file_path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['MemberID', 'Name', 'PasswordHash', 'Email', 'JoinDate'])
        writer.writeheader()
        for member in members:
            writer.writerow(asdict(member))

def load_loans(data_dir):
    loans = []
    file_path = os.path.join(data_dir, 'loans.csv')
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                loans.append(Loan(
                    LoanID=row['LoanID'],
                    MemberID=row['MemberID'],
                    ISBN=row['ISBN'],
                    IssueDate=row['IssueDate'],
                    DueDate=row['DueDate'],
                    ReturnDate=row['ReturnDate']
                ))
    return loans

def save_loans(data_dir, loans):
    file_path = os.path.join(data_dir, 'loans.csv')
    with open(file_path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['LoanID', 'MemberID', 'ISBN', 'IssueDate', 'DueDate', 'ReturnDate'])
        writer.writeheader()
        for loan in loans:
            writer.writerow(asdict(loan))