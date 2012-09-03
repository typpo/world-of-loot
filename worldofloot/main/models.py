from django.db import models
from django.contrib.auth.models import User
from tagging.fields import TagField
from tagging.models import Tag

class Item(models.Model):
  item_id = models.CharField(max_length=10, primary_key=True)
  item_type = models.CharField(max_length=30)   # gear or mount

  name = models.CharField(max_length=75)
  ilvl = models.IntegerField(default=-1)
  quality = models.CharField(max_length=20, null=True)
  icon = models.CharField(max_length=20, null=True)
  slot = models.CharField(max_length=20, null=True)

  wants = models.IntegerField(default=1)
  haves = models.IntegerField(default=0)

  tags = TagField()
  def set_tags(self, tags):
    Tag.objects.update_tags(self, tags)
  def get_tags(self):
    return Tag.objects.get_for_object(self)

class Pin(models.Model):
  item = models.ForeignKey(Item)
  user = models.ForeignKey(User, null=True)

class Image(models.Model):
  item = models.ForeignKey(Item)
  image_id = models.CharField(primary_key=True, max_length=20)
  path = models.CharField(max_length=200)
  thumb_path = models.CharField(max_length=200)
  attribution = models.CharField(max_length=25)

# Introspection rules for south
try:
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules([], ["^tagging\.fields\.TagField"])
except ImportError:
    pass

