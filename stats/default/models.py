
from django.db import models


class Project(models.Model):
    name = models.CharField(max_length=30)


class User(models.Model):
    user_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)


class LaunchState(models.Model):
    launch_id = models.CharField(max_length=100)
    project = models.ForeignKey(Project)
    user = models.ForeignKey(User)
    state = models.CharField(max_length=30)
    enter = models.DateTimeField()
    leave = models.DateTimeField()

    def __unicode__(self):
        return "{launch_id: %s, user: %i}"%(self.launch_id, self.user.user_id)