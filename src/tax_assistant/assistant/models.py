from django.db import models

# Create your models here.


class Session(models.Model):
    user_id = models.UUIDField()
    topic = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_created=True)
    updated_at = models.DateTimeField(auto_now=True)


class Interaction(models.Model):
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_created=True)
    updated_at = models.DateTimeField(auto_now=True)
    user_input = models.CharField(max_length=1024)
    response = models.TextField(null=True)
