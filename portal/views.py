from django.shortcuts import render, get_object_or_404
from portal.models import *


def index(request):
    return render(request, "index_new.html", {})


def browse_jobs(request):
    projects_list = Project.objects.order_by('-postedOn')[:]
    context = {
        'projects_list': projects_list
    }
    return render(request, 'browsejobs.html', context)


def project_description(request, project_pk, userid=1):
    user = get_object_or_404(CustomUser, pk=userid)
    project = get_object_or_404(Project, pk=project_pk)
    tasks_list = project.task_set.all()
    context = {
        "user": user,
        "project": project,
        "tasks_list": tasks_list,
    }
    return render(request, "projectdescription.html", context)


def tasks_description(request, project_pk, task_pk, userid=1):
    user = get_object_or_404(CustomUser, userid)
    project = get_object_or_404(Project, pk=project_pk)
    tasks_list = project.task_set.all()
    context = {
        'user': user,
        'project': project,
        'tasks_list': tasks_list,
    }
    return render(request, 'taskdescription.html', context)


def view_profile(request, userid):
    user = get_object_or_404(CustomUser, id=userid)
    users_skills = user.usersskill_set.all()
    users_languages = user.userscommunicationlanguage_set.all()
    return render(request, "userprofile.html",
                  {"user": user,
                   "users_skills": users_skills,
                   "users_languages": users_languages,
                   })


def post_project(request, userid=1):
    context = {}
    if request.method == "POST":
        project = Project()
        project.project_name = request.POST['name']
        project.description = request.POST['desc']
        project.leader = get_object_or_404(CustomUser, id=userid)
        project.deadline = request.POST['deadline']
        project.save()
        context["project_list"] = Project.objects.filter(leader=project.leader)
        return render(request, 'projectdescription.html', context)
    return render(request, "postproject_new.html", context)


def add_task(request, project_pk):
    # add the field of accepting the skills for the post
    context = {}
    if request.method == "POST":
        task = Task()
        task.task_name = request.POST["task_name"]
        task.task_description = request.POST["task_description"]
        task.credits = request.POST["credits"]
        task.deadline = request.POST["deadline"]
        project = get_object_or_404(Project, id=project_pk)
        project.task_count += 1
        task.project = project
        task.save()
        project.save()
        context["message"] = str(task.task_name) + " added to " + str(task.project.project_name)
    return render(request, "addtask_new.html", context)


def dashboard(request, userid=1):
    context = dict()
    context['projects_list'] = Project.objects.filter(leader=userid)
    return render(request, 'dashboard_new.html', context)


def myprojects(request, userid):
    user = get_object_or_404(CustomUser, pk=userid)
    posted = user.project_set.all()
    working = user.contributor_set.all()
    context = {
        "posted": posted,
        "working": working,
    }
    return render(request, "myprojects.html", context)


def project_task_applicants(request, userid, project_pk, task_pk):
    pass


def project_task_rating(request, project_pk, task_pk):
    pass
