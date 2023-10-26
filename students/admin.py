from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import StudentDetails,SubjectMarks

class StudentDetailsAdmin(UserAdmin):
    list_display = ('username', 'first_name', 'last_name', 'is_staff')

 
admin.site.register(StudentDetails, StudentDetailsAdmin)
admin.site.register(SubjectMarks)
