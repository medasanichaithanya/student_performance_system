"""
URL configuration for student_system project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LogoutView
from students.views import login_views,login_check,create_user,registration_view,store_subject_marks,student_performance

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',login_views, name='default_login_view'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('login_check/',login_check, name='login_check'),
    path('create_user/',create_user, name='create_user'),
    path('registration_view/', registration_view, name='registration_view'),
    path('store-marks/', store_subject_marks, name='store_subject_marks'),
    path('performance/', student_performance, name='performance')
]
