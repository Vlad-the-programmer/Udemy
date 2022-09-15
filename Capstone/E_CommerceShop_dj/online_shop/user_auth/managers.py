from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    def email_validator(self, email):
        try:
            validate_email(email)
        except ValidationError:
            raise ValueError(_("You must provide a valid email address"))
        
    def create_user(self, email, password, first_name, description, gender, featured_img, username, last_name, phone, **extra_fields):
        if not email:
            raise ValueError("User must have an email")
        if not password:
            raise ValueError("User must have a password")
        if email:
            email = self.normalize_email(email)
            self.email_validator(email)

        user = self.model(
            email=email,
            first_name = first_name, 
            username = username, 
            last_name = last_name, 
            phone = phone, 
            featured_img = featured_img,
            description = description,
            gender = gender,
            **extra_fields
        )
        
        user.set_password(password)  # change password to hash
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        
        user.save(using=self._db)
        return user
        
    def create_superuser(self, email, password, first_name, description, gender, featured_img, username, last_name, phone, **extra_fields):
        

        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superusers must have is_superuser=True"))
        
        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superusers must have is_staff=True"))
        
        if not email:
            raise ValueError("User must have an email")
        
        if not password:
            raise ValueError("User must have a password")
        
        if email:
            email = self.normalize_email(email)
            self.email_validator(email)
            
        user = self.create_user(
            email, password, first_name, description, gender, featured_img,
            username, last_name, phone, **extra_fields)
        
        user.save(using=self._db)
        return user