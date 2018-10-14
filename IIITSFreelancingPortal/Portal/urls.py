from django.urls import path
from .views import *

app_name = 'Portal'
urlpatterns = [
    path('', index, name='index'),
    path('signup/', signup_user, name='signup'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('home/', home, name='home'),
    path('post_project/', post_project, name='post_project'),
    path('project_description/', project_description, name='project_description')
]
