from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import StudentDetails,SubjectMarks

class StudentDetailsAdmin(UserAdmin):
    # Define the list of fields to be displayed in the admin list view
    list_display = ('username', 'first_name', 'last_name', 'is_staff')

    # Optionally, you can customize other admin options, such as fieldsets

# Register the custom admin class for your custom user model
admin.site.register(StudentDetails, StudentDetailsAdmin)
admin.site.register(SubjectMarks)
