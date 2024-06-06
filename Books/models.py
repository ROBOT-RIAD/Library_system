from django.db import models
from categories.models import BookCategories
from accounts.models import UserAccount
from Books.constants import STAR_CHOICES

# Create your models here.

class Book(models.Model):
    account=models.ForeignKey(UserAccount, related_name = 'books',on_delete = models.CASCADE,default=None,null=True,blank=True)
    book_category=models.ForeignKey(BookCategories,on_delete = models.CASCADE)
    title =models.CharField(max_length=200)
    description =models.TextField()
    price =models.IntegerField()
    image =models.ImageField(upload_to='Books/media/uploads/',blank=True,null=True)
    buye = models.BooleanField(default=False)


class Review(models.Model):
    book = models.ForeignKey(Book,on_delete=models.CASCADE)
    rating = models.CharField(choices= STAR_CHOICES,max_length=10)
    body =models.TextField()
    def __str__(self) -> str:
        return f"{self.book.title} - {self.rating}"



