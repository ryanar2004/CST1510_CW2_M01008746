import pandas as pd

from app_model.db import get_connection
from app_model.users import add_user, get_user
from hashing import generate_hash, is_valid_hash

#user registration
def register_user(conn):
    name = input("Enter your name: ")
    password = input("Enter your password: ")
    role = input("Enter your role (admin/user): ")
    hash_password = generate_hash(password)
    add_user(conn, name, hash_password, role)
  


#user login
def login_user(conn):
    name = input("Enter your name: ")
    password = input("Enter your password: ")
    id, user_name, user_hash, role = get_user(conn, name)
    print(f'Welcome {user_name}')
    if name == user_name and is_valid_hash(password, user_hash):
            return True
    return False


def main():
    conn = get_connection()
    while True:
        print("Welcome to the User Authentication System")
        choice = input("Choose an option: \n1. Register\n2. Login\n3. Exit\n")
        if choice == '1':
            register_user(conn)
        elif choice == '2':
            if login_user(conn):
                print("Log in successful.")
            else:
                print("Log in failed.")
        elif choice == '3':
            print("Exiting the system. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")
            
   


if __name__ == "__main__":
    main()
