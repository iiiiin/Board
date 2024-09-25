from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


# Create your models here.

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError("Users must have an email address")
        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)
        return user

class CustomUser(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key=True)
    email = models.EmailField()
    password = models.CharField(max_length=300)
    name = models.CharField(max_length=300)

    USERNAME_FIELD = "id"

class Post(models.Model):
    postid = models.AutoField(primary_key=True)
    title = models.CharField(max_length=300)
    content = models.TextField()
    postdate = models.DateTimeField(auto_now=True)
    id = models.ForeignKey(CustomUser,on_delete=models.CASCADE)

