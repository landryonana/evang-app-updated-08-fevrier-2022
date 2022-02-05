from django.db import models
from django.contrib.auth.models import User



class History(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    content_object = models.CharField(max_length=200)
    action_type = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering=('-created',)

    def __str__(self):
        return f"{self.action_type} {self.content_object} par {self.user} à {self.created}"
