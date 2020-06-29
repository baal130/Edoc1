from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

class Chat(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    message = models.CharField(max_length=200)

    def __unicode__(self):
        return self.message