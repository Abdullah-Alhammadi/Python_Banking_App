import csv
import os 
import random
import time

def clear_screen():
    os.system("cls" if os.name=="nt" else "clear")




#The Parent Class: Bank
class Bank:
    def __init__(self, bank_name, account_file='bank.csv'):
        self.bank_name = bank_name
        self.account_file = account_file

    def generate_unique_id(self):
        try:
            with open(self.account_file, "r") as file:
                used_ids = {line.split(";")[0].strip() for line in file}
        except FileNotFoundError:
            used_ids = set()

        while True:
            new_id = f"{random.randint(1, 9999):04d}"  
            if new_id not in used_ids:
                return new_id

    def create_account(self, first_name, last_name, phone, password, checking_balance=0.0, savings_balance=0.0):
        account_id = self.generate_unique_id()
        new_account = [account_id, first_name, last_name, password, phone, checking_balance, savings_balance]

        with open(self.account_file, "a", newline="") as file:
            writer = csv.writer(file, delimiter=";")
            writer.writerow(new_account)

        print(f"Account for {first_name} {last_name} created successfully!")
        return account_id  


    def log_in(self, account_id, phone, password):
        with open(self.account_file, 'r') as file:
            for line in file:
                account_data = line.strip().split(';')
                stored_id = account_data[0]
                stored_phone = account_data[4]
                stored_password = account_data[3]

                if account_id == stored_id and phone == stored_phone and password == stored_password:
                    return True
        return False

    

 

# The Customer Class
class Customer(Bank):
    def __init__(self, bank_name, account_file='bank.csv'):
        super().__init__(bank_name, account_file)
        self.accounts = {}  



    def add_customer(self, first_name, last_name, phone, password):
        """Create a new customer and add to the bank."""
        account_id = self.create_account(first_name, last_name, phone, password)
        print(f"Customer {first_name} {last_name} added successfully!")
        return account_id


    def show_customer_details(self, account_id):
        """Display the customer's details based on their account ID."""
        with open(self.account_file, 'r') as file:
            for line in file:
                account_data = line.strip().split(';')
                stored_id = account_data[0]
                if stored_id == account_id:
                    print(f"Customer Details for Account ID {account_id}:")
                    print(f"First Name: {account_data[1]}")
                    print(f"Last Name: {account_data[2]}")
                    print(f"Phone: {account_data[4]}")
                    return
        print(f"No details found for Account ID {account_id}.")

   




def test_bank_and_customer():
    bank = Bank("ACME Bank")
    customer1 = Customer("ACME Bank")

    print("\n-- Adding a new customer --")
    customer_id = customer1.add_customer(input("Enter your fname: "), input("Enter you lname: "), input("Enter your phone: "), input("Enter your pass: "))
    clear_screen()
    time.sleep(2)
    print("\n-- Attempting to log in --")
    is_logged_in = bank.log_in(input("Enter your Id: "), input("Enter your phone: "), input("Enter your pass: "))
    if is_logged_in:
        print("Login successful!")
    else:
        print("Login failed!")

    print("\n-- Showing customer details --")
    customer1.show_customer_details(customer_id)

test_bank_and_customer()





class Account(Bank):
    pass






class Transactions(Bank):
    pass






# bank = Bank("ACME Bank")
# print(f"Welcome in {bank.bank_name}\n")

# menu = """
# 1. create an account
# 2. log in

# """

# print(menu)
# user_choice = input("Press 1 to create an account or 2 to log in: ")

# if user_choice == "1":
#     clear_screen()
#     bank.create_account()
# elif user_choice == "2":
#     account_id = input("Enter your ID: ")
#     phone = input("Enter your phone: ")
#     password = input("Enter your password: ")
    
#     if bank.log_in(account_id = account_id, phone = phone ,password = password) == True:  
#         clear_screen()
#         print("Welcome to your account!")
#     else:
#         print("Invalid credentials. Please try again.")

      
