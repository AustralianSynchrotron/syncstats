
from django.db import models


class User(models.Model):
    user_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=30)
    email = models.CharField(max_length=30)


class LaunchState(models.Model):
    launch_id = models.CharField(max_length=100)
    user = models.ForeignKey(User)
    state = models.IntegerField()

    def __unicode__(self):
        return "{launch_id: %s, user: %i}"%(self.launch_id, self.user.user_id)