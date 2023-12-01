
from abc import ABC, abstractmethod

class Account(ABC):
    latest_accNum = 1000
    accounts=[]
    def __init__(self,name,email,address,type):
        self.name=name
        self.email = email
        self.address= address
        self.balance = 0
        self.loan_amount =0 
        self.type=type
        Account.latest_accNum += 1
        self.accountNo = Account.latest_accNum
        self.transactions = []
        self.loan_count =0
        Account.accounts.append(self)
    
    
    def deposit(self, amount):
        if amount >= 0:
            self.balance += amount
            Bank.total_balance += amount 
            self.transactions.append(f'Deposited ${amount}')
            print(f"\n--> Deposited ${amount}. New balance: ${self.balance}")
        else:
            print("\n--> Invalid deposit amount")

    def recipent_deposit(self, amount, from_acc):
        if amount >= 0:
            self.balance += amount
            self.transactions.append(f'Deposited ${amount} from {from_acc}')
        else:
            print("\n--> Invalid deposit amount")
    def withdraw(self, amount):
        if Bank.total_balance >= amount:
            if amount >= 0 :
                if amount <= self.balance:
                    self.balance -= amount
                    Bank.total_balance -= amount 
                    self.transactions.append(f'Withdrew ${amount}')
                    print(f"\n--> Withdrew ${amount}. New balance: ${self.balance}")
                else:
                    print("\n--> Insufficient Balance.")
            else:
                print("\n--> Withdrawal amount exceeded")
        else:
            print("\n--> Bank is Bankrupt! Unable to withdraw money.")

    def show_balance(self):
        print(f"\n--> Available balance: ${self.balance}")

    def show_transactions(self):
        print("\n--> Transaction History: \n")
        for transaction in self.transactions:
            print(transaction)

    def take_loan(self, amount):
        
        if self.loan_count < 2:
            if Bank.total_balance >= amount:
                Bank.total_balance -= amount
                self.balance += amount
                self.loan_amount += amount
                self.loan_count += 1
                self.transactions.append(f'Took a loan of ${amount}')
                print(f"\n--> Loan of ${amount} taken. New balance: ${self.balance}")
            else:
                print("\n--> Bank is Bankrupt! Unable to Take Loan.") 
        else:
            print("\n--> You have already taken the maximum number of loans.")

    def transfer(self,amount,recipent_acc):
        if recipent_acc.accountNo != self.accountNo:
            if amount<= self.balance:
                if recipent_acc in Account.accounts:
                    recipent_acc.recipent_deposit(amount, self.accountNo)
                    self.balance-= amount
                    self.transactions.append(f'Transfered ${amount} to account {recipent_acc.accountNo}')
                    print(f'\n--> Transfered ${amount} to account {recipent_acc.accountNo}')
                else:
                    print(f'\n--> Account does not exist. Transfer Failed !')
            else:
                print(f'\n--> Insufficient Balance. Transfer Failed !')
        else:
            print("\n--> You can't transfer amount to your own account.")

    @abstractmethod
    def showInfo(self):
        pass


class SavingsAccount(Account):
    def __init__(self, name, email, address, interestRate):
        super().__init__(name, email, address, "Savings")
        self.interestRate = interestRate

    def apply_interest(self):
        interest = self.balance*(self.interestRate/100)
        print("\n--> Interest is applied !")
        self.deposit(interest)

    def showInfo(self):
        print(f"Infos of {self.type} account of {self.name}:\n")
        print(f'\tAccount Type : {self.type}')
        print(f'\tName : {self.name}')
        print(f'\tEmail : {self.email}')
        print(f'\tAddress : {self.address}')
        print(f'\tAccount No : {self.accountNo}')
        print(f'\tCurrent Balance : ${self.balance}\n')

class CurrentAccount(Account):
    def __init__(self,name,email, address):
        super().__init__(name,email,address,"Current")
            
    def showInfo(self):
        print(f"Infos of {self.type} account of {self.name}:\n")
        print(f'\tAccount Type : {self.type}')
        print(f'\tName : {self.name}')
        print(f'\tEmail : {self.email}')
        print(f'\tAddress : {self.address}')
        print(f'\tAccount No : {self.accountNo}')
        print(f'\tCurrent Balance : ${self.balance}\n')
class Bank:
    
    loan_status = True
    total_balance = 0
    def __init__(self):
        self.total_loan = 0
        self.account_list= Account.accounts

        for account in self.account_list:
            if account.loan_amount > 0:
                self.total_loan +=account.loan_amount
        
        
    def delete_account(self, accountNo):
        for account in self.account_list:
            if account.accountNo == accountNo:
                self.account_list.remove(account)
                print(f'\nAccount {accountNo} Deleted successfully!')
                return
        print(f'Account {accountNo} not found.')

    def show_users(self):
        print("List of Users: ")
        print("----------------------")
        for account in self.account_list:
            print(f'Account Number: {account.accountNo}\tName: {account.name}\tEmail: {account.email}')
        print("----------------------")

    def check_total_balance(self):
        print(f"\n--> Total available balance in the bank: ${Bank.total_balance}")
        return Bank.total_balance
    def check_total_loan(self):
        print(f"\n--> Total Loan amount in the bank: ${self.total_loan}")
        return self.total_loan
    

    def change_loan_status(self):
        print("\n--> Choose Loan Status: \n")
        print("\t1. ON")
        print("\t2. OFF")
        change = int(input("\nChoose Option: "))
        if change == 1:
            Bank.loan_status = True
            if Bank.loan_status == True:
                print("\n--> Loan status changed to ON")
            else:
                print("\n--> Something Error Happen")

        elif change == 2:
            Bank.loan_status = False
            if Bank.loan_status == False:
                print("\n--> Loan status changed to OFF")
            else:
                print("\n--> Something Error Happen")
        else:
            print("Invalid Option")







currentUser=None

while(True):   
    main_op=input("\n--> User/Admin ? (U/A): ")
    if main_op == "U":
        while(True):
            if currentUser==None:
                print("\n--> No user logged in !\n")
                print("1. Register/Login as user?")
                print("2. Go to main page !\n")
                op = int(input("Choose Option: "))
                if op == 1:
                    ch=input("\n--> Register/Login (R/L) : ")
                    if ch=="R":
                        name=input("Name: ")
                        email=input("Email: ")
                        for account in Account.accounts:
                            if email == account.email:
                                while email in account.email:
                                    print("This Mail Already Exist. Please provide another email.")
                                    email=input("Email: ")

                        address=input("Address: ")
                        a=input("Savings Account or Current Account (sv/curr) :")
                        if a=="sv":
                            ir=int(input("Interest rate: "))
                            currentUser=SavingsAccount(name,email,address,ir)
                            print("\n--> Account Created Successfully !")
                        else:
                            currentUser=CurrentAccount(name,email,address)
                            print("\n--> Account Created Successfully !")
                    else:
                        flag = 0
                        email=input("Account Email: ")
                        for account in Account.accounts:
                            if account.email==email:
                                currentUser=account
                                flag = 1
                                break
                            else:
                                flag = 0
                        if flag == 0:
                            print("\nNo account exists with this Email.")
                else:
                    break
                            
            else:
                print(f"\nWelcome {currentUser.name} !\n")

                if currentUser.type=="Savings":

                    print("1. Withdraw")
                    print("2. Deposit")
                    print("3. Show Info")
                    print("4. Check Available Balance")
                    print("5. View Transaction History")
                    print("6. Take a Loan")
                    print("7. Transfer Money to Another Account")
                    print("8. Apply Interset")
                    print("9. Logout\n")

                    op=int(input("Choose Option: "))

                    if op==1:
                        amount=int(input("Enter withdraw amount: "))
                        currentUser.withdraw(amount)

                    elif op==2:
                        amount=int(input("Enter deposit amount: "))
                        currentUser.deposit(amount)

                    elif op==3:
                        currentUser.showInfo()

                    elif op==4:
                        currentUser.show_balance()
                    elif op==5:
                        currentUser.show_transactions()
                    elif op==6:
                        
                        if Bank.loan_status == True:
                            amount = int(input("Enter loan amount: "))
                            currentUser.take_loan(amount)
                        else:
                            print("\n--> Loan feature is Disabled by the bank. Unable to take Loan")
                    elif op==7:
                        flag = 0
                        recipent_acc_no = int(input("Enter recipent's account number: "))
                        amount = int(input("Enter amount to transfer: "))
                        for account in Account.accounts:
                            if account.accountNo == recipent_acc_no:
                                currentUser.transfer(amount,account)
                                flag = 1
                        if flag == 0:
                            print("\nRecipent account doesn't exist.")

                    elif op==8:
                        currentUser.apply_interest()

                    elif op==9:
                        currentUser=None
                    else:
                        print("Invalid Option")

                else:
                    print("1. Withdraw")
                    print("2. Deposit")
                    print("3. Show Info")
                    print("4. Check Available Balance")
                    print("5. View Transaction History")
                    print("6. Take a Loan")
                    print("7. Transfer Money to Another Account")
                    print("8. Logout\n")


                    op=int(input("Choose Option: "))

                    if op==1:
                        amount=int(input("Enter withdraw amount: "))
                        currentUser.withdraw(amount)

                    elif op==2:
                        amount=int(input("Enter deposit amount: "))
                        currentUser.deposit(amount)

                    elif op==3:
                        currentUser.showInfo()

                    elif op==4:
                        currentUser.show_balance()
                    elif op==5:
                        currentUser.show_transactions()
                    elif op==6:
                        
                        if Bank.loan_status == True:
                            amount = int(input("Enter loan amount: "))
                            currentUser.take_loan(amount)
                        else:
                            print("\n--> Loan feature is Disabled by the bank. Unable to take Loan")
                    elif op==7:
                        flag = 0
                        recipent_acc_no = int(input("Enter recipent's account number: "))
                        amount = int(input("Enter amount to transfer: "))
                        for account in Account.accounts:
                            if account.accountNo == recipent_acc_no:
                                currentUser.transfer(amount,account)
                                flag = 1
                        if flag == 0:
                            print("\nRecipent account doesn't exist.")

                    elif op==8:
                        currentUser=None

                    else:
                        print("Invalid Option")
    else:

        print("\n--> Login to admin panel\n")
        username = input("-->Username(admin): ")
        password = input("-->Passowrd(123): ")
        
        while True:
            if username != "admin" or password != "123" :
                print("\nUsername & Password not valid! Re-Enter\n")
                username = input("-->Username(admin): ")
                password = input("-->Passowrd(123): ")
            else:
                break
        while(True):
            print("\n--> Admin Panel\n")
            print("\t1. Create an user account.")
            print("\t2. Delete any user account.")
            print("\t3. Show all user accounts list.")
            print("\t4. Check Total Bank Balance.")
            print("\t5. Check total loan amount.")
            print("\t6. Change loan feature of the Bank.")
            print("\t7. Go to main page/Logout!")
            ch=int(input("\nChoose Option: "))
            
            if ch== 1:
                print("\n--> Create an User Account\n")
                name=input("Name: ")
                email=input("Email: ")
                for account in Account.accounts:
                    if email == account.email:
                        while email in account.email:
                            print("This Mail Already Exist. Please provide another email.")
                            email=input("Email: ")
                address=input("Address: ")
                a=input("Savings Account or Current Account (sv/curr): ")
                if a=="sv":
                    ir=int(input("Interest rate: "))
                    currentUser=SavingsAccount(name,email,address,ir)
                    print("\n--> Account Created Successfully !")
                else:
                    currentUser=CurrentAccount(name,email,address)
                    print("\n--> Account Created Successfully !")

            elif ch== 2:
                print("\n--> Delete an User Account\n")
                ac_num = int(input("Enter the Account Number to delete: "))
                Bank().delete_account(ac_num)
            elif ch== 3:
                Bank().show_users()
            elif ch== 4:
                Bank().check_total_balance()
            elif ch== 5:
                Bank().check_total_loan()
            elif ch== 6:
                bank = Bank()
                bank.change_loan_status()
            elif ch== 7:
                currentUser=None
                break
            else:
                print("Invalid Option.")

            
                
            


