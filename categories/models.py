from django.db import models

# Create your models here.

class BookCategories(models.Model):
    name =models.CharField(max_length=200)
    slug = models.SlugField(max_length=200,unique=True,null=True,blank=True)
    def __str__(self) -> str:
        return self.name
