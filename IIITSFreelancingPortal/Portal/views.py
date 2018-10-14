from django.http import HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect
from django.shortcuts import render, reverse, redirect
from django.contrib.auth import login, authenticate, logout
from .models import *


# Create your views here.
def index(request):
    return HttpResponse('Welcome to IIITS Freelancing Portal')


def signup_user(request):
    if request.method == 'POST':
        username = request.POST['name']
        first_name = request.POST['fname']
        last_name = request.POST['lname']
        email = request.POST['email']
        password = request.POST['passwd']
        phone_number = request.POST['phno']
        bio = request.POST['bio']
        image = request.FILES['image']
        batchYear = request.POST['batch']
        gender = request.POST['gender']
        try:
            if User.objects.get(email=email):
                context = dict()
                context['error_message'] = 'User already exists'
                return render(request, 'signup.html', context)
        except User.DoesNotExist:
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name, email=email,
                                            password=password)
            cuser = CustomUser(user=user, phone_number=phone_number, image=image, bio=bio, batchYear=batchYear,
                               gender=gender)
            user.save()
            cuser.save()
            return request(request, 'login.html')
    return render(request, 'signup.html')


def home(request):
    if request.user.is_authenticated:
        return render(request, 'home.html')


def login_user(request):
    if request.method == 'POST':
        username = request.POST['name']
        password = request.POST['passwd']
        user = authenticate(request, username=username, password=password)
        login(request, user)
        return HttpResponsePermanentRedirect(reverse('Portal:home'))
    return render(request, 'login.html')


def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('Portal:index'))


def post_project(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            project = Project()
            project.project_name = request.POST['name']
            project.description = request.POST['desc']
            project.leader = CustomUser.objects.get(user=request.user.id)
            project.deadline = request.POST['deadline']
            project.save()
            project_list = Project.objects.filter(leader=project.leader)
            context = dict()
            context['project_list'] = project_list
            return render(request, 'projectdescription.html', context)
        return render(request, 'login.html')
    return render(request, "postproject.html")


def project_description(request):
    cuser = CustomUser.objects.get(user=request.user.id)
    project_list = Project.objects.filter(leader=cuser.id)
    print(project_list)
    context = dict()
    context['project_list'] = project_list
    return render(request, 'projectdescription.html', context)
