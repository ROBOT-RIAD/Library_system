from django.contrib import admin
from .import models


# Register your models here.
class BookAdmin(admin.ModelAdmin):
    list_display =['title','price']

admin.site.register(models.Book,BookAdmin)
admin.site.register(models.Review)
