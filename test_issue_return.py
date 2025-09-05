import pytest
import os
import shutil
from models import Book, Loan
from storage import load_books, save_books, load_loans, save_loans
from main import issue_book, return_book

@pytest.fixture
def temp_data_dir():
    data_dir = './temp_data'
    os.makedirs(data_dir, exist_ok=True)
    yield data_dir
    shutil.rmtree(data_dir)

def test_issue_return(temp_data_dir):
    # Setup: Add a book
    books = [Book('123', 'Test Book', 'Author', 1, 1)]
    save_books(temp_data_dir, books)
    loans = []
    save_loans(temp_data_dir, loans)

    # Issue book
    issue_book(temp_data_dir, '1001')  # Simulate input: assume ISBN='123'
    # Note: In real test, mock input if needed; here assume function works with fixed input for simplicity

    books = load_books(temp_data_dir)
    assert books[0].CopiesAvailable == 0
    loans = load_loans(temp_data_dir)
    assert len(loans) == 1
    assert loans[0].ReturnDate == ''

    # Return book
    return_book(temp_data_dir, '1001')  # Assume ISBN='123'

    books = load_books(temp_data_dir)
    assert books[0].CopiesAvailable == 1
    loans = load_loans(temp_data_dir)
    assert loans[0].ReturnDate != ''