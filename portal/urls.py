from django.urls import path
from . import views

app_name = 'Portal'

urlpatterns = [
    path("", views.index, name="index"),

    path("browse_jobs/", views.browse_jobs, name="browse_jobs"),

    path("<int:project_pk>/project_description/", views.project_description, name="project_description"),

    path("<int:project_pk>/<int:task_pk>/task_description/", views.tasks_description, name="tasks_description"),

    path("dashboard/", views.dashboard, name="dashboard"),
    # done
    path("user/<int:userid>/", views.view_profile, name="view_profile"),
    # revise#done

    # working#aakash
    path("post_project/", views.post_project, name="post_project"),
    # revise#done
    path("<int:project_pk>/add_task/", views.add_task, name="add_task"),
    # done
    # path("<int:project_pk>/project_tasks/", views.project_tasks, name='project_tasks'),
    path("<int:userid>/dashboard/", views.dashboard, name="dashboard"),
    # revise#sagar
    path("<int:userid>/myprojects/", views.myprojects, name="myprojects"),
    # revise#sagar

    path("<int:userid>/<int:project_pk>/<int:task_pk>/applicants/", views.project_task_applicants,
         name="project_task_applicants"),
    path("<int:userid>/<int:project_pk>/<int:task_pk>/rating/", views.project_task_rating, name="project_task_rating"),

]
# post_project/

##until login system is made
# <hirer_username>/<project_id>/add_task/
# <hirer_username>/dashboard/
# <hirer_username>/myprojects/
# <hirer_username>/<project_id>/description/
# <hirer_username>/<project_id>/<task_id>/applicants/
# <hirer_username>/<project_id>/<task_id>/
# <hirer_username>/<project_id>/<task_id>/rating/

# admin/<admin_username>/
# admin/<admin_username>/task_request

# <freelancer_username>/dashboard/
# <freelancer_username>/myprojects/
# <freelancer_username>/<project_id>/description/
# <hirer_username>/<project_id>/<task_id>/
# <hirer_username>/<project_id>/<task_id>/rating/
# verify credit
