import random
import json

# References:
# 1. Python OOP - Object-Oriented Programming for Beginners: 
#    https://www.youtube.com/watch?v=Ej_02ICOIgs
# 2. JSON in Python: 
#    https://www.youtube.com/watch?v=pTT5An0cpKw
# 3. Python Official Documentation on JSON:
#    https://docs.python.org/3/library/json.html
# 4. Real Python's Guide to File Handling in Python:
#    https://realpython.com/read-write-files-python/

class Account:
    def __init__(self, account_number, account_type, initial_balance=0):
        self.account_number = account_number
        self.account_type = account_type
        self.balance = initial_balance
        self.password = self.generate_password()

    def generate_password(self):
        # It will generate a 4-digit random password
        return str(random.randint(1000, 9999))

    def deposit(self, amount):
        # Deposit amount to the account balance
        if amount > 0:
            self.balance += amount
            return True
        return False

    def withdraw(self, amount):
        # Withdraw amount from the account balance
        if 0 < amount <= self.balance:
            self.balance -= amount
            return True
        return False

class SavingsAccount(Account):
    def __init__(self, account_number, initial_balance=0):
        # Initialize a savings account
        super().__init__(account_number, 'savings', initial_balance)

class CurrentAccount(Account):
    def __init__(self, account_number, initial_balance=0):
        # Initialize a current account
        super().__init__(account_number, 'current', initial_balance)

class BusinessAccount(Account):
    def __init__(self, account_number, initial_balance=0):
        # Initialize a business account
        super().__init__(account_number, 'business', initial_balance)

class PersonalAccount(Account):
    def __init__(self, account_number, initial_balance=0):
        # Initialize a personal account
        super().__init__(account_number, 'personal', initial_balance)

def save_account(account):
    # Save a single account to the file
    account_data = {
        'account_number': account.account_number,
        'password': account.password,
        'account_type': account.account_type,
        'balance': account.balance
    }
    with open('accounts.txt', 'a') as f:
        f.write(json.dumps(account_data) + '\n')

def save_all_accounts(accounts):
    # Save all accounts to the file
    with open('accounts.txt', 'w') as f:
        for account in accounts:
            account_data = {
                'account_number': account.account_number,
                'password': account.password,
                'account_type': account.account_type,
                'balance': account.balance
            }
            f.write(json.dumps(account_data) + '\n')

def load_accounts():
    # Load all accounts from the file
    accounts = []
    try:
        with open('accounts.txt', 'r') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    account_data = json.loads(line)
                    if account_data['account_type'] == 'savings':
                        account = SavingsAccount(account_data['account_number'], account_data['balance'])
                    elif account_data['account_type'] == 'current':
                        account = CurrentAccount(account_data['account_number'], account_data['balance'])
                    elif account_data['account_type'] == 'business':
                        account = BusinessAccount(account_data['account_number'], account_data['balance'])
                    elif account_data['account_type'] == 'personal':
                        account = PersonalAccount(account_data['account_number'], account_data['balance'])
                    account.password = account_data['password']
                    accounts.append(account)
                except json.JSONDecodeError:
                    # Skip invalid JSON lines
                    print(f"Skipping invalid JSON line: {line}")
    except FileNotFoundError:
        # Handle the case where the file does not exist
        pass
    return accounts

def get_account_by_number(account_number):
    # Get account by account number
    accounts = load_accounts()
    for account in accounts:
        if account.account_number == account_number:
            return account
    return None

def login(account_number, password):
    # Login to an account
    account = get_account_by_number(account_number)
    if account and account.password == password:
        return account
    return None

def delete_account(account_number, password):
    # Delete an account
    accounts = load_accounts()
    account_to_delete = None
    for account in accounts:
        if account.account_number == account_number and account.password == password:
            account_to_delete = account
            break
    if account_to_delete:
        accounts.remove(account_to_delete)
        save_all_accounts(accounts)
        return True
    return False

def transfer_funds(from_account_number, to_account_number, amount):
    # Transfer funds from one account to another
    from_account = get_account_by_number(from_account_number)
    to_account = get_account_by_number(to_account_number)
    if from_account and to_account:
        if from_account.withdraw(amount):
            to_account.deposit(amount)
            accounts = load_accounts()
            for i, account in enumerate(accounts):
                if account.account_number == from_account_number:
                    accounts[i] = from_account
                elif account.account_number == to_account_number:
                    accounts[i] = to_account
            save_all_accounts(accounts)
            return True
        else:
            print("You have insufficient balance to complete the transfer.")
            return False
    print("The recipient account does not exist.")
    return False

def main():
    while True:
        # Main menu
        print("\nWelcome to the Banking Application")
        print("1. Open a new account")
        print("2. Login to an existing account")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            # Open a new account
            account_type = input("Enter account type (savings/current/business/personal): ").lower()
            initial_deposit = float(input("Enter initial deposit amount: "))
            account_number = random.randint(100000000, 999999999)  # 9-digit account number
            if account_type == 'savings':
                account = SavingsAccount(account_number, initial_deposit)
            elif account_type == 'current':
                account = CurrentAccount(account_number, initial_deposit)
            elif account_type == 'business':
                account = BusinessAccount(account_number, initial_deposit)
            elif account_type == 'personal':
                account = PersonalAccount(account_number, initial_deposit)
            else:
                print("Invalid account type!")
                continue
            save_account(account)
            print(f"Account created! Your account number is {account.account_number} and your password is {account.password}")

        elif choice == '2':
            # Login to an existing account
            account_number = int(input("Enter your account number: "))
            password = input("Enter your password: ")
            account = login(account_number, password)
            if account:
                print(f"Login successful! Welcome, Account Number: {account.account_number}")
                while True:
                    # Account menu
                    print("\n1. Check Balance")
                    print("2. Deposit Funds")
                    print("3. Withdraw Funds")
                    print("4. Transfer Funds")
                    print("5. Delete Account")
                    print("6. Logout")
                    sub_choice = input("Enter your choice: ")

                    if sub_choice == '1':
                        # Check balance
                        print(f"Your current balance is: {account.balance}")

                    elif sub_choice == '2':
                        # To deposit funds
                        amount = float(input("Enter amount to deposit: "))
                        if account.deposit(amount):
                            accounts = load_accounts()
                            for i, acc in enumerate(accounts):
                                if acc.account_number == account.account_number:
                                    accounts[i] = account
                            save_all_accounts(accounts)
                            print(f"Deposit successful! New balance: {account.balance}")
                        else:
                            print("Invalid deposit amount!")

                    elif sub_choice == '3':
                        # To withdraw funds
                        amount = float(input("Enter amount to withdraw: "))
                        if account.withdraw(amount):
                            accounts = load_accounts()
                            for i, acc in enumerate(accounts):
                                if acc.account_number == account.account_number:
                                    accounts[i] = account
                            save_all_accounts(accounts)
                            print(f"Withdrawal successful! New balance: {account.balance}")
                        else:
                            print("Insufficient funds or invalid amount!")

                    elif sub_choice == '4':
                        # To transfer funds
                        to_account_number = int(input("Enter recipient's account number: "))
                        amount = float(input("Enter amount to transfer: "))
                        if transfer_funds(account.account_number, to_account_number, amount):
                            print(f"Transfer successful! Your new balance is: {account.balance}")
                        else:
                            print("Transfer failed! You have insufficient balance.")

                    elif sub_choice == '5':
                        # To delete account
                        if delete_account(account.account_number, password):
                            print("Account deleted successfully!")
                            break
                        else:
                            print("Failed to delete account! Incorrect credentials.")

                    elif sub_choice == '6':
                        #To Logout
                        print("Logged out successfully!")
                        break

                    else:
                        print("Invalid choice! Please try again.")
            else:
                print("Login failed! Check your account number and password.")

        elif choice == '3':
            # To exit the application
            print("Exiting the application. Goodbye!")
            break

        else:
            print("Invalid choice! Please try again.")

if __name__ == "__main__":
    main()
