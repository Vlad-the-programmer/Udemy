from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.hashers import make_password

class UserManager(BaseUserManager):
    def create_user(self, email, password, first_name, description, gender, featured_img, username, last_name, phone):
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
        user.featured_img = featured_img
        user.description = description
        user.gender = gender
        user.is_superuser = False
        user.is_staff = True
        user.is_active = True
        user.save(using=self._db)
        return user
        
    def create_superuser(self, email, username, password):
        if not email:
            raise ValueError("User must have an email")
        if not password:
            raise ValueError("User must have a password")

        user = self.model(
            email=self.normalize_email(email)
        )
        user.username = username 
        user.set_password(password)  # change password to hash
        user.is_superuser = True
        user.is_staff = True
        user.is_active = True
        user.save(using=self._db)
        return user