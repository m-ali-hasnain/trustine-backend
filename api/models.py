from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils import timezone
from django.core.exceptions import ValidationError
from .managers import CustomUserManager
from .constants import ROLE_CHOICES, STUDENT

class Course(models.Model):
    name = models.CharField(max_length=255, unique=True)
    credit_hours = models.IntegerField(default=3)

    def __str__(self):
        return self.name

class User(AbstractBaseUser, PermissionsMixin):

    # Defining User fields
    email = models.EmailField(unique=True)
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, blank=True, null=True, default=STUDENT) # Defaults to admin
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    courses = models.ManyToManyField(Course, through='CourseRegistration', related_name='students')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    # Helper method to get credit hours for registered courses so far
    def get_credit_hours(self):
        total_credit_hours = self.courses.aggregate(total_credit_hours=models.Sum('credit_hours')).get('total_credit_hours')
        return total_credit_hours or 0

    def __str__(self):
        return self.email
    
class CourseRegistration(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    registration_date = models.DateTimeField(default=timezone.now)
    def save(self, *args, **kwargs):
        user_credit_hours = self.user.get_credit_hours()
        if user_credit_hours + self.course.credit_hours > 30:
            raise ValidationError("Cannot exceed the maximum credit hours (30 hours).")
        super().save(*args, **kwargs)
