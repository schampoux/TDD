from django.db import models

# Create your models here.

class List(models.Model):
    pass

class Item(models.Model):
    text = models.TextField(default="")
    list = models.ForeignKey(to=List, on_delete=models.DO_NOTHING, default=None)
