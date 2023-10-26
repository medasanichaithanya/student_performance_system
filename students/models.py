from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _

class CustomUserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError(_('The Username field must be set'))
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self.create_user(username, password, **extra_fields)

class StudentDetails(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(unique=True, max_length=30)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=True)

    groups = models.ManyToManyField('auth.Group', verbose_name='groups', blank=True, related_name='student_groups')
    user_permissions = models.ManyToManyField('auth.Permission', verbose_name='user permissions', blank=True, related_name='student_user_permissions')

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username

    class Meta:
        permissions = [
            ("can_view_student_details", "Can view student details"),
            ("can_edit_student_details", "Can edit student details"),
        ]

    
class SubjectMarks(models.Model):
    user = models.ForeignKey(StudentDetails, on_delete=models.CASCADE)
    subject_name = models.CharField(max_length=100)
    marks = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.user.username} - {self.subject_name}"
