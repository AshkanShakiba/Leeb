from django.db import models
from django.contrib.auth.models import AbstractUser


class LeebUser(AbstractUser):
    credit = models.IntegerField(default=0)
