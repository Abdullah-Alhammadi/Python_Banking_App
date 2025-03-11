import csv
import os 
import random
import time

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

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

    def create_account(self, first_name, last_name, phone, password, checking_balance=0.0, savings_balance=0.0, account_status="Inactive"):
        account_id = self.generate_unique_id()
        new_account = [account_id, first_name, last_name, password, phone, checking_balance, savings_balance, account_status]

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

class Customer:
    def __init__(self, bank: Bank):
        self.bank = bank  
        self.accounts = {}

    def add_customer(self, first_name, last_name, phone, password):
        """Create a new customer and add to the bank."""
        account_id = self.bank.create_account(first_name, last_name, phone, password)  # نستخدم كائن Bank هنا
        print(f"Customer {first_name} {last_name} added successfully!")
        return account_id

    def show_customer_details(self, account_id):
        """Display the customer's details based on their account ID."""
        with open(self.bank.account_file, 'r') as file:
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

class Account:
    def __init__(self, account_id, bank, checking_balance=0.0, savings_balance=0.0, account_status="Inactive"):
        self.account_id = account_id
        self.bank = bank
        self.checking_balance = checking_balance
        self.savings_balance = savings_balance
        self.account_status = account_status
        self.overdraft_count = 0  

    def activate_account(self):
        if self.checking_balance > 0 or self.savings_balance > 0:
            self.account_status = "Active"
        else:
            self.account_status = "Inactive"

    def open_checking_account(self, initial_balance=0.0):
        self.checking_balance = initial_balance
        self.activate_account()

    def open_savings_account(self, initial_balance=0.0):
        self.savings_balance = initial_balance
        self.activate_account()

    def withdraw(self, amount, account_type="checking"):
        if account_type == "checking":
            if self.checking_balance - amount < -100:
                print("Insufficient funds or overdraft limit reached.")
                return False
            self.checking_balance -= amount
        elif account_type == "savings":
            if self.savings_balance - amount < -100:
                print("Insufficient funds or overdraft limit reached.")
                return False
            self.savings_balance -= amount
        self.activate_account()
        self.update_account_file()  
        return True

    def deposit(self, amount, account_type="checking"):
        if account_type == "checking":
            self.checking_balance += amount
        elif account_type == "savings":
            self.savings_balance += amount
        self.activate_account()
        self.update_account_file()  

    def transfer(self, amount, from_account="checking", to_account="savings"):
        if from_account == "checking" and self.checking_balance >= amount:
            self.checking_balance -= amount
            if to_account == "savings":
                self.savings_balance += amount
            self.update_account_file() 
            return True
        elif from_account == "savings" and self.savings_balance >= amount:
            self.savings_balance -= amount
            if to_account == "checking":
                self.checking_balance += amount
            self.update_account_file()   
            return True
        return False

    def update_account_file(self):
        with open(self.bank.account_file, 'r') as file:
            lines = file.readlines()

        with open(self.bank.account_file, 'w', newline="") as file:
            writer = csv.writer(file, delimiter=";")
            for line in lines:
                account_data = line.strip().split(';')
                if account_data[0] == self.account_id:
                    account_data[5] = str(self.checking_balance)
                    account_data[6] = str(self.savings_balance)
                    account_data[7] = self.account_status
                writer.writerow(account_data)

    def get_account_details(self):
        return {
            "Account ID": self.account_id,
            "Checking Balance": self.checking_balance,
            "Savings Balance": self.savings_balance,
            "Status": self.account_status,
        }

def test_bank_and_customer_and_account():
    bank = Bank("ACME Bank")
    customer1 = Customer(bank) 
    time.sleep(1)

    print("\n-- Adding a new customer --")
    customer_id = customer1.add_customer(input("Enter your first name: "), input("Enter your last name: "), input("Enter your phone: "), input("Enter your password: "))
    time.sleep(2)

    # 2. Attempting to log in
    print("\n-- Attempting to log in --")
    account_id = input("Enter your account ID: ")
    phone = input("Enter your phone: ")
    password = input("Enter your password: ")
    is_logged_in = bank.log_in(account_id, phone, password)
    if is_logged_in:
        clear_screen()
        print("please wait")
        time.sleep(2)
        print("Login successful!")
        # 3. Show customer details
        print("\n-- Showing customer details --")
        customer1.show_customer_details(customer_id)
       
        # 4. Adding funds to checking or savings account
        account_type = input("\nChoose account type to deposit (checking/savings): ").lower()
        amount = float(input("Enter amount to deposit: "))
        if account_type == "checking":
            print(f"Depositing {amount} into checking account.")
        elif account_type == "savings":
            print(f"Depositing {amount} into savings account.")
        else:
            print("Invalid account type.")
            return
       
        # Deposit money
        account = Account(customer_id, bank)
        account.deposit(amount, account_type)
       
        # Show account details after deposit
        print("\n-- Showing account details after deposit --")
        print(account.get_account_details())
    else:
        print("Failed to log in.")

# Test the bank and customer system
test_bank_and_customer_and_account()
