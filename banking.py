import csv
import os 
import time

def clear_screen():
    os.system("cls" if os.name=="nt" else "clear")
# 🏦 The Parent Class: Bank

class Bank:
    def __init__(self, bank_name, account_file='bank.csv'):
        self.bank_name = bank_name
        self.account_file = account_file

    

    def create_account(self):
        account_number = input("Enter account number: ")
        first_name = input("Enter your first name: ")
        last_name = input("Enter your last name: ")
        password = input("Enter your Password: ")
        checking_balance = float(input("Enter initial checking account balance: "))
        savings_balance = float(input("Enter initial savings account balance: "))        

        new_account = [account_number, first_name, last_name, password, checking_balance, savings_balance]

        with open(self.account_file, "a", newline="") as file:
            writer = csv.writer(file, delimiter=";")
            writer.writerow(new_account)

        print("Account created!")    




bank = Bank("ACME Bank")
print(f"Welcome in {bank.bank_name}")

if input("do you want to compelete? (y/n): ") == "y":
   clear_screen()
   bank.create_account()
else:
    print("ok, se you later")
