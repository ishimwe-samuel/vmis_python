from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class MyAccountManager(BaseUserManager):
    def create_user(self, email, username, surname=None, phone_number=None, orgunitid=None, orgunitname=None, orgunitlevel=None, parentorgunitid=None, parentorgunitname=None, password=None,admin=False):
        if admin:
            if not email:
                raise ValueError("User must have an email address")
            if not username:
                raise ValueError("User must have a username")
        else:
            if not surname:
                raise ValueError("User must have a orgunit id , parent orgunit id and orgunit level")
            if not orgunitid or not parentorgunitid or not orgunitlevel:
                raise ValueError("User must have a orgunit id , parent orgunit id and orgunit level")
            if not orgunitname or not parentorgunitname or not orgunitlevel:
                raise ValueError("User must have a orgunit name , parent orgunit name and orgunit level")
        user = self.model(
            email=self.normalize_email(email),
            username=username,
            surname=surname,
            phone_number=phone_number,
            orgunitid=orgunitid,
            orgunitname=orgunitname,
            orgunitlevel=orgunitlevel,
            parentorgunitid=parentorgunitid,
            parentorgunitname=parentorgunitname,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(email=self.normalize_email(email),username=username,password=password,admin=True)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(verbose_name="email",
                              unique=True, max_length=100)
    username = models.CharField(unique=True, max_length=50)
    surname = models.CharField(max_length=50,null=True)
    phone_number = models.IntegerField(null=True)
    orgunitid = models.CharField(
        verbose_name="organisation unit id", max_length=50,null=True)
    orgunitname = models.CharField(
        verbose_name="organisation unit name", max_length=50,null=True)
    orgunitlevel = models.IntegerField(null=True)
    parentorgunitid = models.CharField(
        verbose_name="parent orgunit name", max_length=50,null=True)
    parentorgunitname = models.CharField(
        verbose_name="parent orgunit id", max_length=50,null=True)
    date_joined = models.DateTimeField(
        verbose_name="date joined", auto_now_add=True)
    last_login = models.DateTimeField(verbose_name="last login", auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']
    objects = MyAccountManager()

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True
