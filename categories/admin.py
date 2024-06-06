from django.contrib import admin
from .models import BookCategories

# Register your models here.
class BookCategoriesAdmin(admin.ModelAdmin):
    prepopulated_fields ={'slug':('name',)}
    list_display=['name','slug']

admin.site.register(BookCategories,BookCategoriesAdmin)
