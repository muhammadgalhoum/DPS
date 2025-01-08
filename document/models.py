from django.db import models

# Create your models here.

class Document(models.Model):
    location = models.CharField(max_length=255)
    width = models.PositiveIntegerField()
    height = models.PositiveIntegerField()

    class Meta:
        abstract = True


class Image(Document):
    number_of_channels = models.PositiveIntegerField()
    
    def __str__(self):
        return f"Image No.{self.id}"


class PDF(Document):
    number_of_pages = models.PositiveIntegerField()
    
    def __str__(self):
        return f"PDF No.{self.id}"
