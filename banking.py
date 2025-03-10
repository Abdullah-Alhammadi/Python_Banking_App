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

    def create_account(self):
        account_id = self.generate_unique_id()
        first_name = input("Enter your first name: ")
        last_name = input("Enter your last name: ")
        password = input("Enter your Password: ")
        checking_balance = float(input("Enter initial checking account balance: "))
        savings_balance = float(input("Enter initial savings account balance: "))        

        new_account = [account_id, first_name, last_name, password, checking_balance, savings_balance]

        with open(self.account_file, "a", newline="") as file:
            writer = csv.writer(file, delimiter=";")
            writer.writerow(new_account)

        print("Account created!") 
        

    def log_in(self, account_id, password):
        with open(self.account_file, 'r') as file:
            for line in file:
             account_data = line.strip().split(';')   
             stored_id = account_data[0]  
             stored_password = account_data[3]   

            if account_id == stored_id and password == stored_password:
                return True  
        return False  
 


        





bank = Bank("ACME Bank")
print(f"Welcome in {bank.bank_name}\n")

menu = """
1. create an account
2. log in

"""

print(menu)
user_choice = input("Press 1 to create an account or 2 to log in: ")

if user_choice == "1":
    clear_screen()
    bank.create_account()
elif user_choice == "2":
    account_id = input("Enter your ID: ")
    password = input("Enter your password: ")
    
    if bank.log_in(account_id=account_id, password=password):  
        clear_screen()
        print("Welcome to your account!")
    else:
        print("Invalid credentials. Please try again.")

      





class Account(Bank):
    pass



class Customer(Bank):
    pass


class Transactions(Bank):
    pass