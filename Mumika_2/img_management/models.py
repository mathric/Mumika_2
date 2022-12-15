from django.db import models

# Create your models here.

class Tag(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    parent_id = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.name

class ImageInfo(models.Model):
    id = models.AutoField(primary_key=True)
    path = models.CharField(max_length=100)
    tags = models.ManyToManyField(Tag, related_name='images')
    name = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name
