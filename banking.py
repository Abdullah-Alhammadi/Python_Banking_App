import csv
import os 
import random
import time


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

        new_id = f"{random.randint(1, 9999):04d}"
        while new_id in used_ids:
            new_id = f"{random.randint(1, 9999):04d}"
        return new_id



    def create_account(self, first_name, last_name, phone, password):
        account_id = self.generate_unique_id()
        new_account = [account_id, first_name, last_name, password, phone, 0.0, 0.0, "Inactive"]

        with open(self.account_file, "a", newline="") as file:
            writer = csv.writer(file, delimiter=";")
            writer.writerow(new_account)

        print(f"Account for {first_name} {last_name} created successfully!")
        return account_id




    def log_in(self, account_id, phone, password):
        with open(self.account_file, 'r') as file:
            for line in file:
                account_data = line.strip().split(';')
                if account_data[0] == account_id and account_data[4] == phone and account_data[3] == password:
                    return True
        return False
    



    def delete_account(self, account_id):
        accounts = []
        account_found = False

        with open(self.account_file, "r") as file:
            for line in file:
               account_data = line.strip().split(";")
               if account_data[0] == account_id:
                  account_found = True 
                  continue  
               accounts.append(account_data)   

        if account_found:
           with open(self.account_file, "w", newline="") as file:
            writer = csv.writer(file, delimiter=";")
            writer.writerows(accounts)     
            print(f"Account {account_id} has been deleted successfully.")
            return True
        else:
            print(f"Account {account_id} not found.")
            return False    




class Account:
    def __init__(self, account_id, bank: Bank):
        self.account_id = account_id
        self.bank = bank
        self.checking_balance = 0.0
        self.savings_balance = 0.0
        self.account_status = "Inactive"
        self.overdraft_count = 0  

    def deposit(self, amount, account_type="checking"):
        if amount <= 0:
            print("Invalid deposit amount.")
            return

        if account_type == "checking":
            self.checking_balance += amount
        elif account_type == "savings":
            self.savings_balance += amount
        else:
            print("Invalid account type.")
            return

        self.activate_account()
        self.update_account_file()



    def withdraw(self, amount, account_type="checking"):
        if amount <= 0:
            print("Invalid withdrawal amount.")
            return

        balance = self.get_balance(account_type)
        if balance < amount:
            print("Insufficient funds.")
            return

        if not self.handle_overdraft(amount, account_type, balance):
            return

        if account_type == "checking":
            self.checking_balance -= amount
        else:
            self.savings_balance -= amount

        self.activate_account()
        self.update_account_file()



    def transfer(self, amount, from_account="checking", to_account="savings"):
        if amount <= 0:
            print("Invalid transfer amount.")
            return

        if from_account == to_account:
            print("Cannot transfer to the same account.")
            return

        if self.get_balance(from_account) < amount:
            print("Insufficient funds for transfer.")
            return


        if from_account == "checking":
            self.checking_balance -= amount
            self.savings_balance += amount
        else:
            self.savings_balance -= amount
            self.checking_balance += amount

        self.update_account_file()

    def handle_overdraft(self, amount, account_type, balance):
        if balance - amount < -100:
            print("Transaction denied: Account balance cannot go below -$100.")
            return False

        if balance < 0 and amount > 100:
            print("Transaction denied: Cannot withdraw more than $100 when account is negative.")
            return False

        if balance - amount < 0:
            print("Overdraft alert: Charging $35 fee.")
            self.overdraft_count += 1

            if self.overdraft_count >= 2:
                self.account_status = "Inactive"
                print("Account deactivated due to multiple overdrafts.")
                return False

            if balance - amount >= -65:
                if account_type == "checking":
                    self.checking_balance -= 35  
                else:
                    self.savings_balance -= 35   
            else:
                print("Transaction denied: Cannot apply overdraft fee without exceeding -$100.")
                return False

        return True

    def get_balance(self, account_type):
        return self.checking_balance if account_type == "checking" else self.savings_balance

    def activate_account(self):
        if self.checking_balance > 0 or self.savings_balance > 0:
            self.account_status = "Active"
        else:
            self.account_status = "Inactive"

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





class Customer:
    def __init__(self, bank : Bank):
        self.bank = bank

    def add_customer(self, first_name, last_name, phone, password):
        return self.bank.create_account(first_name, last_name, phone, password)

    def show_customer_details(self, account_id):
        found = False  
        with open(self.bank.account_file, 'r') as file:
            for line in file:
                account_data = line.strip().split(';')
                if account_data[0] == account_id:
                    found = True  
                    print(f"Customer Details for Account ID {account_id}:")
                    print(f"First Name: {account_data[1]}")
                    print(f"Last Name: {account_data[2]}")
                    print(f"Phone: {account_data[4]}")
                    break   

        if not found:
            print(f"No details found for Account ID {account_id}.")
    
    def log_in_customer(self, account_id, phone, password):
        return self.bank.log_in(account_id, phone, password)
         

    def delete_customer_account(self, account_id):
        return self.bank.delete_account(account_id)            




class Transactions:
    def __init__(self, bank : Bank):
        self.bank = bank

    def transfer_money(self, sender_id, receiver_id, amount):
        sender_data = None
        receiver_data = None
        accounts = []

        with open(self.bank.account_file, 'r') as file:
            for line in file:
                account_data = line.strip().split(';')
                if account_data[0] == sender_id:
                    sender_data = account_data
                if account_data[0] == receiver_id:
                    receiver_data = account_data
                accounts.append(account_data)

        if not sender_data or not receiver_data:
            print("Account not found.")
            return False

        sender_balance = float(sender_data[5])
        receiver_balance = float(receiver_data[5])

        if sender_balance < amount:
            print("Insufficient funds.")
            return False

        sender_data[5] = str(sender_balance - amount)
        receiver_data[5] = str(receiver_balance + amount)

        with open(self.bank.account_file, 'w', newline="") as file:
            writer = csv.writer(file, delimiter=";")
            for account in accounts:
                writer.writerow(account)

        print(f"Transferred {amount} from {sender_id} to {receiver_id}.")
        return True



def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")





def start_app():
    pass











# def test_classes():
#     bank = Bank(bank_name="ASME")
#     print(f"Welcome to {bank.bank_name}")
#     while True:
#         print("""
#            1. Create an account
#            2. Log in
#            3. Exit
#         """)
    
#         response = input("Choose 1, 2: ")

#         if response == "1":
#             customer = Customer(bank)
#             account_id = customer.add_customer(
#                 input("Enter your first name: "), 
#                 input("Enter your last name: "), 
#                 input("Enter phone: "), 
#                 input("Enter password: ")
#             )
#             clear_screen()
#             print(f"Account created successfully! Account ID: {account_id}")
#             customer.show_customer_details(account_id)
#         elif response == "2":
#             customer_log = Customer(bank)
#             account_id = customer_log.log_in_customer(
#                 input("Enter your ID: "),
#                 input("Enter your phone: "),
#                 input("Enter your password: ")
#             )
            
        
#         else:
#             print("Invlaid")    


#         if input("Do you want to continue: ") == "n":
#             break

# test_classes()

