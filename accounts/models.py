from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from .managers import UserManager
from locations.models import Province, City



class User(AbstractBaseUser):
    """ This is a custom user model that authenticate user by
         phone_nubber instesd of email. """
    
    phone_number = models.CharField(unique=True, max_length=11)
    name = models.CharField(max_length=32)
    created = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    #backend = "authentication.backend.AuthBackend"
    objects = UserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return f"{self.name}---{self.phone_number}"
    
    @property
    def is_staff(self):
        return self.is_admin
    
    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True
    
class OtpCode(models.Model):
    phone_number = models.CharField(max_length=11)
    code = models.PositiveSmallIntegerField()
    created = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f'code >> {self.code} ____  phone_number >> {self.phone_number}'
    

class PostalInfo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='postalinfo_of_user')
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=250)
    postal_code = models.CharField(max_length=10)
    province = models.ForeignKey(Province, on_delete=models.SET_NULL, null=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True)
    address = models.TextField(null=True)

    def __str__(self) -> str:
        return f'{self.first_name}--{self.last_name} | {self.province}-{self.city}'