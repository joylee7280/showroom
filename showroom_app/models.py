from django.db import models
from django.utils import timezone
# Create your models here.


class pudu_robot(models.Model):
    name = models.CharField(max_length=20)
    robotid = models.CharField(max_length=15)

    def __str__(self):
        return self.name


class reeman_robot(models.Model):
    name = models.CharField(max_length=20)
    host_name = models.CharField(max_length=20)

    def __str__(self):
        return self.name
