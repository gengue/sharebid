from django.db import models
from django.contrib.auth.models import User

class KeyWord(models.Model):
    name = models.CharField(max_length=255)
    users = models.ManyToManyField(User)

    def __unicode__(self):
        return '%s' % (self.name)
