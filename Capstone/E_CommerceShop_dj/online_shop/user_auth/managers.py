from django.contrib.auth.base_user import BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, email, first_name=None, username=None, last_name=None, phone=None, password=None):
        if not email:
            raise ValueError("User must have an email")
        if not password:
            raise ValueError("User must have a password")

        user = self.model(
            email=self.normalize_email(email),
        )
        user.first_name = first_name 
        user.username = username 
        user.last_name = last_name 
        user.set_password(password)  # change password to hash
        user.phone = phone 
        user.admin = False
        user.staff = True
        user.active = True
        user.save(using=self._db)
        return user
        
    def create_superuser(self, email, first_name=None, username=None, last_name=None, phone=None, password=None):
        if not email:
            raise ValueError("User must have an email")
        if not password:
            raise ValueError("User must have a password")

        user = self.model(
            email=self.normalize_email(email)
        )
        user.first_name = first_name 
        user.username = username 
        user.last_name = last_name
        user.set_password(password)  # change password to hash
        user.phone = phone 
        user.admin = True
        user.staff = True
        user.active = True
        user.save(using=self._db)
        return user