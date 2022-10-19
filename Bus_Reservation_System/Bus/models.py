from django.db import models
from django.contrib.auth.models import AbstractBaseUser, UserManager, BaseUserManager

# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, email, name, password=None):
        
        if not email:
            raise ValueError('User must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            name=name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password=None):
        
        user = self.create_user(
            email,
            password=password,
            name=name,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    username = None
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin
    
    def __str__(self):
        return self.name


class BusList(models.Model):
    bus_no = models.CharField(max_length=100)
    bus_name = models.CharField(max_length=100)
    from_place = models.CharField(max_length=100)
    to = models.CharField(max_length=100)
    price = models.PositiveIntegerField()

    class Meta:
         unique_together=('bus_no','bus_name')

    # def __str__(self):
    #     return self.bus_name


class Reservation(models.Model):
    bus = models.ForeignKey(BusList,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="users")
    current_date = models.DateTimeField(auto_now_add=True)
    reservation_date = models.DateTimeField()
    booking_status = (
        ('booked','booked'),
        ('cancel', 'cancel') )
    status = models.CharField(choices=booking_status, default="booked", max_length=20)
    
    

# class Price(models.Model):
#     bus = models.ForeignKey(BusList,on_delete=models.CASCADE)
#     price = models.PositiveIntegerField()

#     class Meta:
#          unique_together=('bus','price')