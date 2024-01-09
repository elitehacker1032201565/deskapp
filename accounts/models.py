# from django.db import models
# from django.contrib.auth.models import AbstractUser, PermissionsMixin, BaseUserManager, Group, Permission
# from indian_cities.dj_city import cities
# from django.utils import timezone
# from django.utils.translation import gettext_lazy as _
# from django.contrib.auth import get_user_model


# STATE = (("Andhra Pradesh","Andhra Pradesh"),("Arunachal Pradesh ","Arunachal Pradesh "),("Assam","Assam"),("Bihar","Bihar"),("Chhattisgarh","Chhattisgarh"),("Goa","Goa"),("Gujarat","Gujarat"),("Haryana","Haryana"),("Himachal Pradesh","Himachal Pradesh"),("Jammu and Kashmir ","Jammu and Kashmir "),("Jharkhand","Jharkhand"),("Karnataka","Karnataka"),("Kerala","Kerala"),("Madhya Pradesh","Madhya Pradesh"),("Maharashtra","Maharashtra"),("Manipur","Manipur"),("Meghalaya","Meghalaya"),("Mizoram","Mizoram"),("Nagaland","Nagaland"),("Odisha","Odisha"),("Punjab","Punjab"),("Rajasthan","Rajasthan"),("Sikkim","Sikkim"),("Tamil Nadu","Tamil Nadu"),("Telangana","Telangana"),("Tripura","Tripura"),("Uttar Pradesh","Uttar Pradesh"),("Uttarakhand","Uttarakhand"),("West Bengal","West Bengal"),("Andaman and Nicobar Islands","Andaman and Nicobar Islands"),("Chandigarh","Chandigarh"),("Dadra and Nagar Haveli","Dadra and Nagar Haveli"),("Daman and Diu","Daman and Diu"),("Lakshadweep","Lakshadweep"),("National Capital Territory of Delhi","National Capital Territory of Delhi"),("Puducherry","Puducherry"))
# GENDERS = (('M', 'Male'), ('F', 'Female'), ('O', 'Other'))
# CREDIT_CARD_type = (
#         ('VISA', 'VISA'),
#         ('MASTER', 'MASTER'),
#         ('AMEX', 'AMEX'),
#         ('DISCOVER', 'DISCOVER'),
#     )


# class CustomUserManager(BaseUserManager):
#     def create_user(self, username, password=None, **extra_fields):
#         if not username:
#             raise ValueError('The username must be set')
#         user = self.model(username=username, **extra_fields)
#         user.set_password(password)
#         user.save(using=self._db)
#         return user
    
#     def create_superuser(self, username, password, **extra_fields):
#         extra_fields.setdefault('is_staff', True)
#         extra_fields.setdefault('is_superuser', True)
        
#         if extra_fields.get('is_staff') is not True:
#             raise ValueError('Superuser must have is_staff=True.')
        
#         if extra_fields.get('is_superuser') is not True:
#             raise ValueError('Superuser must have is_superuser=True.')
        
#         return self.create_user(username, password, **extra_fields)

# class CustomUser(AbstractUser, PermissionsMixin):
#     username = models.CharField(max_length=150, unique=True)
#     # password = models.PasswordInput(max_length=150)
#     state = models.CharField(max_length=255, choices=STATE, default='Null')
#     gender = models.CharField(max_length=1, choices=GENDERS)
#     city = models.CharField(choices=cities, null=False, max_length=20)
#     fullname = models.CharField(max_length=255)
#     email = models.EmailField(max_length=255)
#     credit_card_number = models.CharField(max_length=16)  
#     expiration_date = models.DateField()
#     public_visibility = models.BooleanField(default=True)
#     is_active = models.BooleanField(default=True)
#     is_staff = models.BooleanField(default=False)
    
#     date_joined = models.DateTimeField(default=timezone.now)
#     cvv = models.CharField(max_length=3)
#     credit_card_type = models.CharField(max_length=225, choices=CREDIT_CARD_type, default='VISA')
    
#     objects = CustomUserManager()
    
#     USERNAME_FIELD = 'username'
#     REQUIRED_FIELDS = ['username']

#     groups = models.ManyToManyField(
#         Group,
#         verbose_name=_('groups'),
#         blank=True,
#         help_text=_(
#             'The groups this user belongs to. A user will get all permissions '
#             'granted to each of their groups.'
#         ),
#         related_name='customuser_groups',  # Choose a related name that doesn't clash
#     )
#     user_permissions = models.ManyToManyField(
#         Permission,
#         verbose_name=_('user permissions'),
#         blank=True,
#         help_text=_('Specific permissions for this user.'),
#         related_name='customuser_user_permissions',  # Choose a related name that doesn't clash
#     )

#     def __str__(self):
#         return self.username



from django.contrib.auth.models import AbstractUser, PermissionsMixin, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.contrib.auth import get_user_model


class CustomUserManager(BaseUserManager):
    use_in_migrations = True
    def create_user(self, username,email, password=None, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username,email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(username,email,password, **extra_fields)

    
#CustomUser = get_user_model()

class CustomUser(AbstractUser, PermissionsMixin):
    username = models.CharField(max_length=100)
    email_token = models.CharField(max_length=100,null=True)
    is_verified = models.BooleanField(default=False)
    otp = models.CharField(max_length=6, null=True, blank=True)
    email = models.EmailField(_("email address"), unique=True)
    public_visibility = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email
    
class UploadedFile(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    file = models.FileField(upload_to='uploaded_files/')
    visibility = models.BooleanField(default=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    year_published = models.PositiveIntegerField()

    def __str__(self):
        return self.title

