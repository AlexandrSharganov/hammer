import uuid

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models, IntegrityError
from phonenumber_field.modelfields import PhoneNumberField


class UserManager(BaseUserManager):

    def create_user(self, phone_number, password=None, **extra_fields):
            user = self.model(phone_number=phone_number, **extra_fields)
            if password:
                user.set_password(password)
            try:
                user.save(using=self._db)
            except IntegrityError:
                raise IntegrityError("User with this phone number already exists")
            return user

    def create_superuser(self, phone_number, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if not extra_fields.get('is_staff'):
            raise ValueError('Superuser must have is_staff=True.')
        
        if not extra_fields.get('is_superuser'):
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(phone_number, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):

    phone_number = PhoneNumberField(unique=True)
    invite_code = models.CharField(
        max_length=6,
        unique=True,
        blank=True
    )
    activated_invite_code = models.ForeignKey(
        'User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='referals'
    )

    objects = UserManager()

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'phone_number'

    def __str__(self):
        return str(self.phone_number)
