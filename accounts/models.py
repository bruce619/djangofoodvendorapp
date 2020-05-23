from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


class MyAccountManager(BaseUserManager):
    def create_user(self, first_name, last_name, email, password=None):
        if not first_name:
            raise ValueError('Users must have a first name')
        if not last_name:
            raise ValueError('Users must have a last name')
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            first_name=first_name,
            last_name=last_name,
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name, last_name, email, password):
        user = self.create_user(
            first_name=first_name,
            last_name=last_name,
            email=self.normalize_email(email),
            password=password
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    username = None
    email = models.EmailField(verbose_name='email', max_length=60, unique=True, blank=False,
                              error_messages={
                                  'unique': "A user with that email already exists.",
                              })
    phonenumber = models.CharField(verbose_name="phone number", max_length=20, unique=True, blank=False,
                                   error_messages={
                                       'unique': "Phone number already exists.",
                                   })
    datetimecreated = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    stripe_customer_id = models.CharField(max_length=50, blank=True, null=True)
    one_click_purchasing = models.BooleanField(default=False)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_vendor = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=False)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __unicode__(self):
        return self.email

    objects = MyAccountManager()

    # For checking permissions. to keep it simple all admin have ALL permissons
    def has_perm(self, perm, obj=None):
        return self.is_admin

    # Does this user have permission to view this app? (ALWAYS YES FOR SIMPLICITY)
    def has_module_perms(self, app_label):
        return True


class Vendor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return self.user.email


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name

