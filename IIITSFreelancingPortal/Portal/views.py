from django.contrib.auth import login, authenticate, logout
from django.http import HttpResponseRedirect, HttpResponsePermanentRedirect
from django.shortcuts import render, reverse, redirect

from .models import *


# Create your views here.
def index(request):
    return render(request, 'index.html')


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
        context = dict()
        cuser = CustomUser.objects.get(user=request.user.id)
        posted_projects = Project.objects.filter(leader=cuser.id)
        context['posted_projects'] = posted_projects
        return render(request, 'home.html', context)


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
            posted_projects = Project.objects.filter(leader=project.leader)
            context = dict()
            context['posted_projects'] = posted_projects
            return render(request, 'home.html', context)
        return render(request, 'login.html')
    return render(request, "postproject.html")


def project_description(request, project_id):
    project = Project.objects.get(id=project_id)
    added_tasks = Task.objects.filter(project=project.id)
    context = dict()
    context['project'] = project
    context['added_tasks'] = added_tasks
    return render(request, 'projectdescription.html', context)


def add_task(request, project_id):
    context = {}
    if request.method == 'POST':
        if request.user.is_authenticated:
            task = Task()
            task.task_name = request.POST['name']
            task.task_description = request.POST['desc']
            task.credits = request.POST['credit']
            task.deadline = request.POST['deadline']
            task.project = Project.objects.get(id=project_id)
            task.save()
            return redirect('Portal:project_description', project_id)
        return render(request, 'login.html')
    context['project_id'] = project_id
    return render(request, "addtask.html", context)


def task_description(request, project_id, task_id):
    task = Task.objects.filter(id=task_id, project=project_id)
    context = dict()
    context['task'] = task
    return render(request, 'taskdescription.html', context)
