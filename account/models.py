from django.db import models
from django.contrib.auth.models import AbstractUser

from baseapp import utils


class Account(AbstractUser):
    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    balance = models.IntegerField(default=0)

    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    phone_number = models.CharField(max_length=100, blank=True, null=True)
    date_of_birth = models.CharField(max_length=100, blank=True, null=True)
    gender = models.CharField(max_length=50, blank=True, null=True)
    next_of_kin = models.CharField(max_length=100, blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    zipcode = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    account_type = models.CharField(max_length=100, blank=True, null=True)

    security_pin = models.CharField(max_length=100, blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    ip_address = models.CharField(max_length=15, blank=True, null=True)

    profile_image = models.ImageField(upload_to="profile/", blank=True, null=True)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    def image_url(self):
        if self.profile_image:
            #
            return f"https://heritagebankonline.net{self.profile_image.url}"
        else:
            return (
                f"https://ui-avatars.com/api/?name={self.first_name} {self.last_name}"
            )

    def get_fullname(self):
        return f"{self.first_name} {self.last_name}"

    def format_balance(self):
        return "{:,}".format(self.balance)

    def in_debt(self):
        if self.balance < 0:
            return True
        return False

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        # Perform custom logic before saving
        if not self.username:
            self.username = utils.gen_random_number()

        # Call parent save method
        super().save(*args, **kwargs)
