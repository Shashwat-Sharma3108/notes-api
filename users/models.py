from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):

    first_name = models.CharField(_("first name"), max_length=30, blank=False, db_index=True, null=False)
    last_name = models.CharField(_("last name"), max_length=150, blank=False, db_index=True, null=False)
    email = models.EmailField(_("email address"), db_index=True, null=False, blank=False, unique=True)
    username = models.CharField(max_length=150, unique=True, null=False, blank=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.email} {self.username}"