from django.db import models
from django.contrib.auth.models import User

class Pin(models.Model):
  user = models.ForeignKey(User)
  wowhead_id = models.CharField(max_length=10)
  wants = models.IntegerField(default=0)
  haves = models.IntegerField(default=0)


class Image(models.Model):
  pin = models.ForeignKey(Pin)
  attribution = models.CharField(max_length=100)
  thumb_path = models.CharField(max_length=200)
  path = models.CharField(max_length=200)
