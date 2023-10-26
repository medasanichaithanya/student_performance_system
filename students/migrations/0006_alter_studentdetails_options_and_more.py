# Generated by Django 4.2.6 on 2023-10-26 10:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0005_alter_studentdetails_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='studentdetails',
            options={'permissions': [('can_view_student_details', 'Can view student details'), ('can_edit_student_details', 'Can edit student details')]},
        ),
        migrations.RemoveField(
            model_name='studentdetails',
            name='date_joined',
        ),
        migrations.RemoveField(
            model_name='studentdetails',
            name='email',
        ),
        migrations.AlterField(
            model_name='studentdetails',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='studentdetails',
            name='is_staff',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='studentdetails',
            name='is_superuser',
            field=models.BooleanField(default=True),
        ),
    ]
