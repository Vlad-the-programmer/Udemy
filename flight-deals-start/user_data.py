

class User:
    def __init__(self):
        self.name = input("Enter your name: ").title()
        self.last_name = input("Enter your last name: ").title()
        self.email = input("Enter your email: ")
        self.check_email = input("Enter your email again: ")

    def check_email(self):
        if self.email == self.check_email:
            print("You're in the club!")
        else:
            print("The email is not identical!...")

