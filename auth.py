import bcrypt
import getpass
from datetime import datetime
from storage import load_members, save_members
from models import Member  # Added import for Member class

session = {}  # Global session dict to store logged-in user

def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def check_password(stored_hash, password):
    return bcrypt.checkpw(password.encode('utf-8'), stored_hash.encode('utf-8'))

def generate_member_id(members):
    if not members:
        return '1001'
    return str(max(int(m.MemberID) for m in members) + 1)

def register_member(data_dir):
    members = load_members(data_dir)
    name = input("Enter name: ")
    email = input("Enter email: ")
    password = getpass.getpass("Enter password: ")
    confirm_password = getpass.getpass("Confirm password: ")
    if password != confirm_password:
        print("Passwords do not match.")
        return
    member_id = generate_member_id(members)
    join_date = datetime.today().strftime('%Y-%m-%d')
    password_hash = hash_password(password)
    new_member = Member(member_id, name, password_hash, email, join_date)  # Now Member is recognized
    members.append(new_member)
    save_members(data_dir, members)
    print(f"Member registered with ID: {member_id}")

def login(data_dir, role):
    global session
    if role == 'librarian':
        # Fixed credentials for simplicity (secure in production)
        username = input("Librarian username: ")
        password = getpass.getpass("Librarian password: ")
        if username == 'admin' and password == 'adminpass':
            session = {'role': 'librarian', 'id': 'admin'}
            return session
        else:
            print("Invalid credentials.")
            return None
    elif role == 'member':
        member_id = input("Member ID: ")
        password = getpass.getpass("Password: ")
        members = load_members(data_dir)
        for member in members:
            if member.MemberID == member_id and check_password(member.PasswordHash, password):
                session = {'role': 'member', 'id': member_id}
                return session
        print("Invalid credentials.")
        return None