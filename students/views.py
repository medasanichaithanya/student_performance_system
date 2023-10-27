from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password
from .models import StudentDetails,SubjectMarks
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.db.models import Sum, Max
from rest_framework.decorators import api_view
from django.http import HttpResponse


@api_view(['GET'])
def login_views(request):
    if request.method == 'GET':
        return render(request, 'login_form.html')


@api_view(['GET'])
def registration_view(request):
    if request.method == 'GET':
        return render(request, 'registration_form.html')


@api_view(['POST'])
def create_user(request):
    try:
        data = request.data
        username = data.get('username')
        password = data.get('password')
        first_name = data.get('first_name')
        last_name = data.get('last_name')

        hashed_password = make_password(password)

        user = StudentDetails(
            username=username,
            password=hashed_password,
            first_name=first_name,
            last_name=last_name
        )
        user.save()
        return redirect('/',{'user_error':False}) 
    
    except Exception as e:
        html_content = "<html><body><h1>Some Error Occured</h1></body></html>"
        return HttpResponse(html_content)

@api_view(['POST'])
def login_check(request):
    try:
        username = request.POST['username']
        password = request.POST['password']
        try:
            user = StudentDetails.objects.get(username=username)
        except StudentDetails.DoesNotExist:
            return render(request,'login_form.html',{'user_error':True})

        user = authenticate(request, username=user.username, password=password)

        if user is not None:
            login(request, user)
            student_name = user.first_name  
            
            check_marks = SubjectMarks.objects.filter(user__username=user.username).exists()
            if check_marks:
                response = student_performance(user = user.username)
                return render(request,'performance.html',response)
            else:
                return render(request, 'dashboard.html', {'student_name': student_name})
        else:
            return render(request,'login_form.html',{'user_error':True})
        
    except Exception as e:
        html_content = "<html><body><h1>Some Error Occured</h1></body></html>"
        return HttpResponse(html_content)
    
    
def student_performance(user):
    try:
        student = user
        marks = SubjectMarks.objects.filter(user__username=student)
        # Calculate total marks
        total_marks = marks.aggregate(Sum('marks'))['marks__sum']

        # Calculate individual subject marks
        math_marks = marks.filter(subject_name='Math').first().marks
        science_marks = marks.filter(subject_name='Science').first().marks
        hindi_marks = marks.filter(subject_name='Hindi').first().marks
        english_marks = marks.filter(subject_name='English').first().marks
        social_marks = marks.filter(subject_name='Social').first().marks

        total_marks_by_student = SubjectMarks.objects.values('user__username').annotate(total_marks=Sum('marks'))
        # Find the highest total marks and the corresponding student
        overall_highest_scorer = total_marks_by_student.order_by('-total_marks').first()

        # Calculate individual subject's highest scorers
        math_highest_scorer = SubjectMarks.objects.filter(subject_name='Math').values('user__username').annotate(max_score=Max('marks')).order_by('-max_score').first()
        science_highest_scorer = SubjectMarks.objects.filter(subject_name='Science').values('user__username').annotate(max_score=Max('marks')).order_by('-max_score').first()
        hindi_highest_scorer = SubjectMarks.objects.filter(subject_name='Hindi').values('user__username').annotate(max_score=Max('marks')).order_by('-max_score').first()
        social_highest_scorer = SubjectMarks.objects.filter(subject_name='Social').values('user__username').annotate(max_score=Max('marks')).order_by('-max_score').first()
        english_highest_scorer = SubjectMarks.objects.filter(subject_name='English').values('user__username').annotate(max_score=Max('marks')).order_by('-max_score').first()

        context = {
            'student_name': student,
            'total_marks': total_marks,
            'math_marks': math_marks,
            'science_marks': science_marks,
            'hindi_marks': hindi_marks,
            'english_marks': english_marks,
            'social_marks': social_marks,
            'overall_highest_scorer': overall_highest_scorer,
            'math_highest_scorer': math_highest_scorer,
            'science_highest_scorer': science_highest_scorer,
            'hindi_highest_scorer': hindi_highest_scorer,
            'social_highest_scorer': social_highest_scorer,
            'english_highest_scorer': english_highest_scorer
        }

        return context
    except Exception as e:
        html_content = "<html><body><h1>Some Error Occured</h1></body></html>"
        return HttpResponse(html_content)
    
@api_view(['POST'])
def store_subject_marks(request):
    try:
        student = request.user  
        subject_marks = {}
        subjects = ['Math', 'Science', 'English', 'Hindi', 'Social']

        for subject in subjects:
            marks = request.POST.get(subject.lower())
            if marks is not None:
                marks = int(marks)
                SubjectMarks.objects.create(user=student, subject_name=subject, marks=marks)
                subject_marks[subject] = marks

        response = student_performance(user = student)
        return render(request,'performance.html',response)
    
    except Exception as e:
        html_content = "<html><body><h1>Some Error Occured</h1></body></html>"
        return HttpResponse(html_content)

    









