from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)

from typing import ClassVar


class UserManager(BaseUserManager):
    def create_user(self, mobile, password=None, *args, **kwargs):
        if not mobile:
            raise ValueError("Provide a valid mobile number")
        user = self.model(mobile=mobile, password=None, *args, **kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, mobile, password=None, *args, **kwargs):
        pass


class User(AbstractBaseUser, PermissionsMixin):
    mobile_regex_validator = RegexValidator(
        regex=r"^9\d{9}$", message="Incorrect mobile format"
    )
    ME = "9378510273"

    mobile = models.CharField(
        max_length=10, unique=True, db_index=True, validators=[mobile_regex_validator]
    )

    USERNAME_FIELD = "mobile"

    objects = UserManager()

    def __str__(self):
        return f"{self.mobile=}-{self.pk=}"

    @property
    def is_superuser(self) -> bool:
        # Override the is_superuser property for simplicity and only allowing one superuser
        return self.mobile == self.ME

    def has_perms(self, perm_list, obj=None) -> bool:
        return self.is_superuser

    def has_module_perms(self, app_label) -> bool:
        return self.is_superuser
