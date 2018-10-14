from django.db import models
from django.contrib.auth.models import User
# Create your models here.

Beginner = Good = 1
Intermediate = VeryGood = 2
Advanced = Excellent = 3

Worst = 1
Bad = 1.5
NotSoGood = 2
Average = 2.5
OK = 3
QuietGood = 3.5
Better = 4
Great = 4.5
Amazing = 5

proficiency_level_choices = (
    (Beginner, 'Beginner'),
    (Intermediate, 'Intermediate'),
    (Advanced, 'Advanced')
)
fluency_level_choices = (
    (Good, 'Good'),
    (VeryGood, 'VeryGood'),
    (Excellent, 'Excellent')
)
rating_choices = (
    (Worst, 'Worst'),
    (Bad, 'Bad'),
    (NotSoGood, 'NotSoGood'),
    (Average, 'Average'),
    (OK, 'OK'),
    (QuietGood, 'QuietGood'),
    (Better, 'Better'),
    (Great, 'Great'),
    (Amazing, 'Amazing'),
)


class CustomUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.IntegerField(blank=False, default=None)
    bio = models.TextField(max_length=500, default=None)
    image = models.ImageField(upload_to='profiles')
    batchYear = models.CharField(max_length=4, choices=(
        ("None", "None"), ("UG-1", "UG-1"), ("UG-2", "UG-2"), ("UG-3", "UG-3"), ("UG-4", "UG-4"), ("MS", "MS"),
        ("Ph.D", "Ph.D")), default='None')
    # gender
    gender = models.CharField(max_length=1, choices=(("M", "Male"), ("F", "Female")), blank=False)

    def __str__(self):
        return self.user.username


class Skill(models.Model):
    skill_name = models.CharField(max_length=20, blank=False, unique=True)

    def __str__(self):
        return self.skill_name


class UsersSkill(models.Model):
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    level_of_proficiency = models.IntegerField(
        default=Beginner,
        choices=proficiency_level_choices,
    )

    def __str__(self):
        return str(self.user.username) + "/" + str(self.skill.skill_name) + "/" + str(self.level_of_proficiency)


class CommunicationLanguage(models.Model):
    language_name = models.CharField(max_length=20, blank=False, unique=True)

    def __str__(self):
        return self.language_name


class UsersCommunicationLanguage(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    language = models.ForeignKey(CommunicationLanguage, on_delete=models.CASCADE)
    level_of_fluency = models.IntegerField(
        default=Good,
        choices=fluency_level_choices
    )

    def __str__(self):
        return str(self.user.username) + "/" + str(self.language.language_name) + "/" + str(self.level_of_fluency)


class Project(models.Model):
    project_name = models.CharField(max_length=30, blank=False)
    description = models.CharField(max_length=100, default=None)
    postedOn = models.DateTimeField(auto_now_add=True, blank=False)
    leader = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    isCompleted = models.BooleanField(default=False)
    deadline = models.DateField(blank=False)
    task_count = models.IntegerField(default=0, blank=False)

    def __str__(self):
        return self.project_name


class Task(models.Model):
    task_name = models.CharField(max_length=30, blank=False)
    addedOn = models.DateTimeField(auto_now_add=True, blank=False)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    credits = models.CharField(max_length=20, blank=False)
    task_description = models.CharField(max_length=100, default=None)
    isCompleted = models.BooleanField(default=False)
    deadline = models.DateField(blank=False)

    def __str__(self):
        return self.task_name


class TaskSkillsRequired(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    proficiency_level_required = models.IntegerField(
        default=Beginner,
        choices=proficiency_level_choices,
    )

    def __str__(self):
        return str(self.task.task_name) + '[id=' + str(self.task.id) + ']'


class Applicant(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    time_of_application = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user.username) + '[id=' + str(self.user.id) + ']'


class Contributor(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    isCreditVerified = models.BooleanField(default=False)
    time_of_selection = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user.username) + '[id=' + str(self.user.id) + ']'


class HoursOfWork(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(blank=True, default=None)

    def __str__(self):
        return str(self.user.username) + '[id=' + str(self.user.id) + ']'


class TaskRating(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    rating = models.DecimalField(
        choices=rating_choices,
        max_digits=2,
        decimal_places=1,
        default=QuietGood
    )

    def __str__(self):
        return str(self.user.username) + '[id=' + str(self.user.id) + ']'


class UserRating(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    rating_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    rating_to = models.ForeignKey(CustomUser, related_name='rating_by', on_delete=models.CASCADE)
    rating = models.DecimalField(
        choices=rating_choices,
        max_digits=2,
        decimal_places=1,
        default=QuietGood
    )

    def __str__(self):
        return str(self.rating_by.username) + '[id=' + str(self.rating_by.id) + ']'


class Notification(models.Model):
    _from = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    _to = models.ForeignKey(CustomUser, related_name='_from', on_delete=models.CASCADE)
    message = models.CharField(default=None, max_length=300)
    hasRead = models.BooleanField(default=False)
    receivingTime = models.DateTimeField(blank=False)



