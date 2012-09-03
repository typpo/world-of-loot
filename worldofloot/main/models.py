from django.db import models
from django.contrib.auth.models import User

class Item(models.Model):
  item_id = models.CharField(max_length=10, primary_key=True)
  item_type = models.CharField(max_length=30)   # gear or mount

  name = models.CharField(max_length=75)
  ilvl = models.IntegerField()
  quality = models.CharField(max_length=20)
  icon = models.CharField(max_length=20)
  slot = models.CharField(max_length=20)

  wants = models.IntegerField(default=1)
  haves = models.IntegerField(default=0)

class Pin(models.Model):
  item = models.ForeignKey(Item)
  user = models.ForeignKey(User, null=True)

class Image(models.Model):
  item = models.ForeignKey(Item)
  image_id = models.CharField(primary_key=True, max_length=20)
  path = models.CharField(max_length=200)
  thumb_path = models.CharField(max_length=200)
  attribution = models.CharField(max_length=25)
