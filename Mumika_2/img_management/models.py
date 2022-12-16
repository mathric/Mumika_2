from django.db import models

# Create your models here.

class Tag(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    type_name = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name

class ImageInfo(models.Model):
    id = models.AutoField(primary_key=True)
    tags = models.ManyToManyField(Tag, related_name='images')
    filepath = models.CharField(max_length=100, unique=True)
    # file name not inclue filetype
    filename = models.CharField(max_length=100, null=True, blank=True)
    filetype = models.CharField(max_length=100, null=True, blank=True)
    artwork_name = models.CharField(max_length=100, null=True, blank=True)
    
    def __str__(self):
        return self.filename
