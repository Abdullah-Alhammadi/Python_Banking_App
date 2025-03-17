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
                    return account_id
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

        updated_lines = []
        found = False

        with open(self.bank.account_file, 'r') as file:
            lines = file.readlines()

        for line in lines:
            account_data = line.strip().split(';')
            if account_data[0] == self.account_id:
                found = True
                checking_balance = float(account_data[5])
                savings_balance = float(account_data[6])

                if account_type == "checking":
                     checking_balance += amount
                     self.checking_balance = checking_balance  
                elif account_type == "savings":
                     savings_balance += amount
                     self.savings_balance = savings_balance    
                else:
                    print("Invalid account type.")
                    return

                account_data[5] = str(checking_balance)
                account_data[6] = str(savings_balance)

            updated_lines.append(';'.join(account_data) + '\n')

        if not found:
            print(f"Account {self.account_id} not found!")
            return

        with open(self.bank.account_file, 'w') as file:
             file.writelines(updated_lines)

        self.activate_account()




    def withdraw(self, amount, account_type="checking"):
        if amount <= 0:
            print("Invalid withdrawal amount.")
            return
       
        updated_lines = []
        found = False
       
        with open(self.bank.account_file, 'r') as file:
            lines = file.readlines()
       
        for line in lines:
            account_data = line.strip().split(';')
            if account_data[0] == self.account_id:
                found = True
                checking_balance = float(account_data[5])
                savings_balance = float(account_data[6])
       
                if account_type == "checking":
                    balance = checking_balance
                else:
                    balance = savings_balance
       
                if balance < amount:
                    print("Insufficient funds.")
                    return
       
                if not self.handle_overdraft(amount, account_type):
                    return
       
                if account_type == "checking":
                    checking_balance -= amount
                else:
                    savings_balance -= amount
       
                account_data[5] = str(checking_balance)
                account_data[6] = str(savings_balance)
       
            updated_lines.append(';'.join(account_data) + '\n')
       
        if not found:
            print(f"Account {self.account_id} not found!")
            return
       
        with open(self.bank.account_file, 'w') as file:
            file.writelines(updated_lines)
       
        self.activate_account()


    def transfer(self, amount, from_account="checking", to_account="savings"):
     if amount <= 0:
         print("Invalid transfer amount.")
         return

     if from_account == to_account:
         print("Cannot transfer to the same account.")
         return

     updated_lines = []
     found = False

     with open(self.bank.account_file, 'r') as file:
         lines = file.readlines()

     for line in lines:
         account_data = line.strip().split(';')
         if account_data[0] == self.account_id:
             found = True
             checking_balance = float(account_data[5])
             savings_balance = float(account_data[6])

             if from_account == "checking" and checking_balance >= amount:
                 checking_balance -= amount
                 savings_balance += amount
             elif from_account == "savings" and savings_balance >= amount:
                 savings_balance -= amount
                 checking_balance += amount
             else:
                 print("Insufficient funds for transfer.")
                 return

             account_data[5] = str(checking_balance)
             account_data[6] = str(savings_balance)
             self.checking_balance = checking_balance
             self.savings_balance = savings_balance

         updated_lines.append(';'.join(account_data) + '\n')

     if not found:
         print(f"Account {self.account_id} not found!")
         return

     with open(self.bank.account_file, 'w') as file:
         file.writelines(updated_lines)
    

     self.activate_account()



    def handle_overdraft(self, amount, account_type):
        updated_lines = []
        found = False
       
        with open(self.bank.account_file, 'r') as file:
            lines = file.readlines()
       
        for line in lines:
            account_data = line.strip().split(';')
            if account_data[0] == self.account_id:
                found = True
                checking_balance = float(account_data[5])
                savings_balance = float(account_data[6])
       
                balance = checking_balance if account_type == "checking" else savings_balance
       
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
                            checking_balance -= 35
                        else:
                            savings_balance -= 35
                    else:
                        print("Transaction denied: Cannot apply overdraft fee without exceeding -$100.")
                        return False
       
                account_data[5] = str(checking_balance)
                account_data[6] = str(savings_balance)
                account_data[7] = self.account_status  
       
            updated_lines.append(';'.join(account_data) + '\n')
       
        if not found:
            print(f"Account {self.account_id} not found!")
            return False
       
        with open(self.bank.account_file, 'w') as file:
            file.writelines(updated_lines)
       
        return True




    def activate_account(self):
        with open(self.bank.account_file, 'r') as file:
            lines = file.readlines()
     
        for i, line in enumerate(lines):
            account_data = line.strip().split(';')
            if account_data[0] == self.account_id:
                checking_balance = float(account_data[5])
                savings_balance = float(account_data[6])
     
                if checking_balance > 0 or savings_balance > 0:
                    self.account_status = "Active"
                else:
                    self.account_status = "Inactive"
     
                account_data[7] = self.account_status
     
                lines[i] = ';'.join(account_data) + '\n'
                break       
             
        with open(self.bank.account_file, 'w') as file:
            file.writelines(lines)
     

       

  
    







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

    class Customer:
        def __init__(self, bank: Bank):
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
    
        if sender_data[7] == "Inactive":
            print("Sender's account is inactive. Cannot transfer money.")
            return False
    
        sender_balance = float(sender_data[5])
        receiver_balance = float(receiver_data[5])
    
        if sender_balance < amount:
            print("Insufficient funds.")
            return False
    
        if sender_balance - amount < -100:
            print("Transaction denied: Account balance cannot go below -$100.")
            return False
    
        sender_data[5] = str(sender_balance - amount)
        receiver_data[5] = str(receiver_balance + amount)
    
        with open(self.bank.account_file, 'w', newline="") as file:
            writer = csv.writer(file, delimiter=";")
            for account in accounts:
                writer.writerow(account)
    
        print(f"Transferred ${amount} from {sender_id} to {receiver_id}.")
        return True








def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")





def start_app():
  while True:  
    clear_screen()
    bank = Bank(bank_name=r"""
 ________  ________  _____ ______   _______           ________  ________  ________   ___  __       
|\   __  \|\   ____\|\   _ \  _   \|\  ___ \         |\   __  \|\   __  \|\   ___  \|\  \|\  \     
\ \  \|\  \ \  \___|\ \  \\\__\ \  \ \   __/|        \ \  \|\ /\ \  \|\  \ \  \\ \  \ \  \/  /|_   
 \ \   __  \ \  \    \ \  \\|__| \  \ \  \_|/__       \ \   __  \ \   __  \ \  \\ \  \ \   ___  \  
  \ \  \ \  \ \  \____\ \  \    \ \  \ \  \_|\ \       \ \  \|\  \ \  \ \  \ \  \\ \  \ \  \\ \  \ 
   \ \__\ \__\ \_______\ \__\    \ \__\ \_______\       \ \_______\ \__\ \__\ \__\\ \__\ \__\\ \__\
    \|__|\|__|\|_______|\|__|     \|__|\|_______|        \|_______|\|__|\|__|\|__| \|__|\|__| \|__|                                                                                                                                                                                                                                                                                      
""")
    print(bank.bank_name)
    print("""
          1. create an account
          2. log-in
          
          """)
    response = input("please choose (1/2) to continue: ")

    if response == "1":
        clear_screen()

        customer = Customer(bank)
        account_id = customer.add_customer(
            input("Enter your first name: "), 
            input("Enter your last name: "), 
            input("Enter phone: "), 
            input("Enter password: ")
            )
        clear_screen()
        print("please wait.........")
        time.sleep(3)

        print(f"Account created successfully! Account ID: {account_id}\n")
        customer.show_customer_details(account_id)
        if input("Do you want to back to 1.home or 2.exit: ") == "2":
            break



    elif response == "2":
        clear_screen()
        print("please wait.......")
        time.sleep(2)
        clear_screen()
        customer_log = Customer(bank)
        account_id = customer_log.log_in_customer(
            input("Enter your ID: "),
            input("Enter your phone: "),
            input("Enter your password: ")
        )
        clear_screen()
        print(f"---Welcome---\n\n")
        time.sleep(2)
        while True:
            print("""
              1. Deposit Money
              2. Withdraw Money
              3. Transfer Money
              4. Show Account Details
              5. transfer from your checking and savings   
              6. Delete Account
              7. Logout 
              """)    
            choice = input("Please choose a number to continue: ")
            account = Account(account_id, bank) 

            if choice == "1":
               clear_screen()
               print("please wait.......")
               time.sleep(2)
               clear_screen()
               amount = float(input("Enter amount to deposit: "))
               account_type = input("Enter account type (checking/savings): ").strip().lower()
               if account_type in ["checking", "savings"]:
                  account.deposit(amount, account_type)
                  clear_screen()
                  print("successful")
                  time.sleep(3)


               else:
                  print("Invalid account type. Please enter 'checking' or 'savings'.")
                


            elif choice == "2":
                 clear_screen()
                 print("please wait.......")
                 time.sleep(2)
                 clear_screen()

                 amount = float(input("Enter amount to withdraw: "))
                 account_type = input("Enter account type (checking/savings): ").strip().lower()
                 if account_type in ["checking", "savings"]:
                    account.withdraw(amount, account_type)
                    clear_screen()
                    print("successful")
                    time.sleep(3)
                 else:
                    print("Invalid account type. Please enter 'checking' or 'savings'.")
    
     
            elif choice == "3":
                 clear_screen()
                 print("please wait.......")
                 time.sleep(2)
                 clear_screen()

                 receiver_id = input("Enter receiver's account ID: ")
                 amount = float(input("Enter amount to transfer: "))
                 transactions = Transactions(bank)
                 transactions.transfer_money(account_id, receiver_id, amount)
                 clear_screen()
                 print("successful")
                 time.sleep(3)

     
            elif choice == "4":
                 clear_screen()
                 print("please wait.......")
                 time.sleep(2)
                 clear_screen()
                 customer = Customer(bank)
                 customer.show_customer_details(account_id)
     
            
            
            elif choice == "5":
                 clear_screen()
                 print("please wait.......")
                 time.sleep(2)
                 clear_screen()
                 amount = float(input("Enter amount to transfer between checking and savings: "))
                 direction = input("Transfer from (1. checking to savings /2. savings to checking): ").strip().lower()
                 if direction == "1":
                     account.transfer(amount, "checking", "savings")
                 elif direction == "2":
                     account.transfer(amount, "savings", "checking")
                 else:
                     print("Invalid transfer direction.")


            elif choice == "6":
                 clear_screen()
                 print("please wait.......")
                 time.sleep(2)
                 clear_screen()
                 confirm = input("Are you sure you want to delete your account? (yes/no): ").strip().lower()
                 if confirm == "yes":
                     if Customer(bank).delete_customer_account(account_id):
                         print("Account deleted successfully. Logging out...")
                         break         

      
            elif choice == "7":
                 time.sleep(2)
                 print("Logging out...")
                 print("\n\n\nsee you soon")
                 break
     
            else:
                clear_screen()
                print("please wait.......")
                time.sleep(2)
                print("Invalid choice, please try again.")

    else:
        clear_screen()
        print("please wait.......")
        time.sleep(2)
        print("Invalid typed")             
     



start_app()