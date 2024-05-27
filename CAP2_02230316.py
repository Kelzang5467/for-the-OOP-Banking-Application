import random
import string

class BankAccount:
    """
    Represents a bank account with an account type and balance.
    
    Attributes:
        account_type (str): The type of the account (e.g., "Personal" or "Business").
        balance (float): The current balance of the account.
        account_number (str): The unique account number generated for the account.
        password (str): The password generated for the account.
    """
    
    def __init__(self, account_type, balance=0):
        self.account_type = account_type
        self.balance = balance
        self.account_number = self.generate_account_number()
        self.password = self.generate_password()

    def generate_account_number(self):
        """
        Generates a unique 10-digit account number.
        
        Returns:
            str: The generated account number.
        """
        return ''.join(str(random.randint(0, 9)) for _ in range(10))

    def generate_password(self):
        """
        Generates an 8-character password consisting of letters and digits.
        
        Returns:
            str: The generated password.
        """
        characters = string.ascii_letters + string.digits
        return ''.join(random.choice(characters) for _ in range(8))

    def deposit(self, amount):
        """
        Deposits the specified amount into the account.
        
        Args:
            amount (float): The amount to be deposited.
        """
        self.balance += amount

    def withdraw(self, amount):
        """
        Withdraws the specified amount from the account if there are sufficient funds.
        
        Args:
            amount (float): The amount to be withdrawn.
        """
        if self.balance >= amount:
            self.balance -= amount
        else:
            print("Insufficient funds.")

    def check_balance(self):
        """
        Returns the current balance of the account.
        
        Returns:
            float: The current balance of the account.
        """
        return self.balance

class PersonalAccount(BankAccount):
    """
    Represents a personal bank account.
    """
    
    def __init__(self, balance=0):
        super().__init__("Personal", balance)

class BusinessAccount(BankAccount):
    """
    Represents a business bank account.
    """
    
    def __init__(self, balance=0):
        super().__init__("Business", balance)

def save_account(account):
    """
    Saves the account information to a file named "accounts.txt".
    
    Args:
        account (BankAccount): The account to be saved.
    """
    with open("accounts.txt", "a") as file:
        file.write(f"{account.account_number},{account.password},{account.account_type},{account.balance}\n")

def load_accounts():
    """
    Loads account information from the "accounts.txt" file.
    
    Returns:
        dict: A dictionary containing the loaded accounts, with account numbers as keys and BankAccount objects as values.
    """
    accounts = {}
    try:
        with open("accounts.txt", "r") as file:
            for line in file:
                account_number, password, account_type, balance = line.strip().split(",")
                if account_type == "Personal":
                    account = PersonalAccount(int(balance))
                else:
                    account = BusinessAccount(int(balance))
                account.account_number = account_number
                account.password = password
                accounts[account_number] = account
    except FileNotFoundError:
        pass
    return accounts

def login():
    """
    Prompts the user to enter their account number and password, and attempts to log in.
    
    Returns:
        BankAccount or None: The logged-in account if the login is successful, otherwise None.
    """
    account_number = input("Enter your account number: ")
    password = input("Enter your password: ")
    accounts = load_accounts()
    if account_number in accounts and accounts[account_number].password == password:
        return accounts[account_number]
    else:
        print("Invalid account number or password.")
        return None

def logout():
    """
    Logs out the user and displays a message.
    """
    print("Logged out successfully.")

def main():
    """
    The main function that runs the banking application.
    """
    accounts = load_accounts()   
    """
    Load accounts at the beginning of the main function
    """
    
    while True:
        print("Welcome to the Banking Application!")
        print("1. Open a new account")
        print("2. Login to an existing account")
        print("3. Exit")

        choice = input("Enter your choice (1-3): ")

        if choice == "1":
            account_type = input("Enter account type (Personal/Business): ")
            if account_type.lower() == "personal":
                account = PersonalAccount()
            elif account_type.lower() == "business":
                account = BusinessAccount()
            else:
                print("Invalid account type.")
                continue
            print(f"Your account number is: {account.account_number}")
            print(f"Your password is: {account.password}")
            save_account(account)
            print("Account created successfully.")

        elif choice == "2":
            account = login()
            if account:
                while True:
                    print(f"Welcome, {account.account_type} account holder!")
                    print("1. Check balance")
                    print("2. Deposit")
                    print("3. Withdraw")
                    print("4. Transfer to another account")
                    print("5. Logout")

                    choice = input("Enter your choice (1-5): ")

                    if choice == "1":
                        print(f"Your balance is: {account.check_balance()}")
                    elif choice == "2":
                        amount = float(input("Enter the amount to deposit: "))
                        account.deposit(amount)
                        print("Deposit successful.")
                    elif choice == "3":
                        amount = float(input("Enter the amount to withdraw: "))
                        account.withdraw(amount)
                        print("Withdrawal successful.")
                    elif choice == "4":
                        recipient_account_number = input("Enter recipient's account number: ")
                        recipient_account = accounts.get(recipient_account_number)
                        if recipient_account:
                            amount = float(input("Enter the amount to transfer: "))
                            if account != recipient_account:
                                account.withdraw(amount)
                                recipient_account.deposit(amount)
                                print("Transfer successful.")
                            else:
                                print("Cannot transfer to the same account.")
                        else:
                            print("Recipient account not found.")
                    elif choice == "5":
                        logout()
                        break

def validate_brackets(s):
    """
    Validates if the given string of brackets is balanced.
    
    Args:
        s (str): The string of brackets to be validated.
    
    Returns:
        bool: True if the brackets are balanced, False otherwise.
    """
    stack = []
    brackets = {')': '(', '}': '{', ']': '['}

    for char in s:
        if char in brackets.values():
            stack.append(char)
        elif char in brackets.keys():
            if not stack or stack.pop() != brackets[char]:
                return False

    return not stack

if __name__ == "__main__":
    main()
    input_string = input("Enter a string of brackets: ")