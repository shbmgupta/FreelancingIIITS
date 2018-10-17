from django.contrib.auth import login, authenticate, logout
from django.http import HttpResponseRedirect, HttpResponsePermanentRedirect
from django.shortcuts import render, reverse, redirect

from .models import *


# Create your views here.
def index(request):
    return render(request, 'index.html')


def signup_user(request):
    context = dict()
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
        skills = request.POST.getlist('skills')
        languages = request.POST.getlist('languages')
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
            for uskill in skills:
                skill = Skill.objects.get(skill_name=uskill)
                skill.skill_name = uskill
                skill.save()
                cuskill = UsersSkill()
                cuskill.skill = skill
                cuskill.user = cuser
                cuskill.level_of_proficiency = request.POST[skill.skill_name]
                cuskill.save()
            for ulanguage in languages:
                language = CommunicationLanguage.objects.get(language_name=ulanguage)
                language.language_name = ulanguage
                language.save()
                culanguage = UsersCommunicationLanguage()
                culanguage.language = language
                culanguage.user = cuser
                culanguage.level_of_fluency = request.POST[language.language_name]
                culanguage.save()
            login(request, user)
            return request(request, 'home.html')
    skill_list = Skill.objects.all()
    language_list = CommunicationLanguage.objects.all()
    context['skill_list'] = skill_list
    context['language_list'] = language_list
    return render(request, 'signup.html', context)


def home(request):
    if not request.user.is_superuser and request.user.is_authenticated:
        context = dict()
        cuser = CustomUser.objects.get(user=request.user.id)
        posted_projects = Project.objects.filter(leader=cuser.id)
        applicable_projects = Project.objects.exclude(isCompleted=True).exclude(leader=cuser.id)
        context['posted_projects'] = posted_projects
        context['applicable_projects'] = applicable_projects
        return render(request, 'home.html', context)


def login_user(request):
    if request.method == 'POST':
        username = request.POST['name']
        password = request.POST['passwd']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return HttpResponsePermanentRedirect(reverse('Portal:home'))
        context = dict()
        context['error_message'] = 'Username or password is incorrect'
        return render(request, 'login.html', context)
    return render(request, 'login.html')


def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('Portal:index'))


def context_data(projects, tasks):
    context = dict()
    decontext = dict()
    p_key = set()
    for task in tasks:
        key = str(task.project.id)
        if key not in p_key:
            decontext[key] = []
            p_key.add(key)
        decontext[key].append(task)
    context['jobs'] = []
    for project in projects:
        context['jobs'] += [(project, decontext[str(project.id)])]
    return context


def jobs_update(request):
    skills = request.POST['skills']
    # languages = request.POST['languages']
    jobs = request.POST['jobs']
    filtered_tasks = []
    for job in jobs:
        tasks = job[1]
        for task in tasks:
            taskskreq = TaskSkillsRequired.objects.filter(task=task)
            skill_list = [Skill.objects.get(id=obj.skill.id).skill_name for obj in taskskreq]
            flag = sum([skill in skills for skill in skill_list])
            if flag != 0:
                filtered_tasks.append(task)
    context = context_data(jobs[0], filtered_tasks)
    return render(request, 'jobs.html', context)


def browse_jobs(request):
    projects = Project.objects.filter(isCompleted=False).order_by('-postedOn')
    tasks = Task.objects.filter(isCompleted=False).order_by('-addedOn')
    context = context_data(projects, tasks)
    skill_list = Skill.objects.all()
    language_list = CommunicationLanguage.objects.all()
    context['skill_list'] = skill_list
    context['language_list'] = language_list
    return render(request, 'browsejobs.html', context)


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
            skills = request.POST.getlist('skills')
            task.project = Project.objects.get(id=project_id)
            task.save()
            for rskill in skills:
                skill = Skill.objects.get(skill_name=rskill)
                task_skill_req = TaskSkillsRequired()
                task_skill_req.task = task
                task_skill_req.skill = skill
                task_skill_req.save()
            return redirect('Portal:project_description', project_id)
        return render(request, 'login.html')
    context['project_id'] = project_id
    skill_list = Skill.objects.all()
    context['skill_list'] = skill_list
    return render(request, "addtask.html", context)


def task_description(request, project_id, task_id):
    task = Task.objects.get(id=task_id, project=project_id)
    context = dict()
    context['task'] = task
    return render(request, 'taskdescription.html', context)
