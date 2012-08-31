from django.db import models
from django.contrib.auth.models import User

class Pin(models.Model):
  item = models.ForeignKey(Item)
  user = models.ForeignKey(User)
  wants = models.IntegerField(default=0)
  haves = models.IntegerField(default=0)

class Item(models.Model):
  id = models.CharField(max_length=10)
  url = models.CharField(max_length=100)
  attribution = models.CharField(max_length=100)
  item_type = models.CharField(max_length=30)

class Image(models.Model):
  item = models.ForeignKey(Item)
  thumb_path = models.CharField(max_length=200)
  path = models.CharField(max_length=200)
