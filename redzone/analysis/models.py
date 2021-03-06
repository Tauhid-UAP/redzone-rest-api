from django.db import models

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

from django.templatetags.static import static

# Create your models here.

# Pass these as two-tuple values
# in GENDER_CHOICES
MALE_NUMBER = 1
FEMALE_NUMBER = 2
MALE = 'Male'
FEMALE = 'Female'

GENDER_CHOICES = [
    (MALE_NUMBER, MALE),
    (FEMALE_NUMBER, FEMALE),
]

class MyAccountManager(BaseUserManager):

    def create_user(self, username, email, password=None):
        if not email:
            raise ValueError("Users must have an email address.")
        if not username:
            raise ValueError("Users must have a username.")

        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )

        user.set_password(password)
        user.save(self, using=self._db)
        return user

    def create_superuser(self, email, username, password):
        user=self.create_user(
            email=self.normalize_email(email),
            password=password,
            username=username,
        )


        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)





class RedZoneUser(AbstractBaseUser):
    # required to include
    email = models.EmailField(verbose_name='email', unique=True, max_length=60)
    username = models.CharField(max_length=60, unique=True)
    date_joined = models.DateField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateField(verbose_name='last login', auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    # new
    first_name = models.CharField(max_length=60, verbose_name='first_name')
    last_name = models.CharField(max_length=60, verbose_name='last_name')
    gender = models.SmallIntegerField(choices=GENDER_CHOICES, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    profession = models.CharField(max_length=60, verbose_name='profession', null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username',]

    objects = MyAccountManager()

    def __str__(self):
        return self.email

    class Meta:
        verbose_name_plural = "RedZone Users"

class Location(models.Model):
    name = models.CharField(max_length=60)

class Routine(models.Model):
    user = models.ForeignKey(to=RedZoneUser, on_delete=models.CASCADE)
    covid_positive = models.BooleanField()
    visited_outside = models.BooleanField()
    other_interaction = models.BooleanField()
    wore_mask = models.BooleanField()
    wore_ppe = models.BooleanField()
    location = models.CharField(max_length=100)
    date = models.DateField(auto_now_add=True)