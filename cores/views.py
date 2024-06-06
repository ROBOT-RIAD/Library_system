from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views.generic import ListView
from Books.models import Book
from categories.models import BookCategories

class HomeView(ListView):
    model = Book
    template_name = 'cores/index.html'
    context_object_name = 'data'

    def get_queryset(self):
        book_slug = self.kwargs.get('slug')
        if book_slug:
            book_category = BookCategories.objects.get(slug=book_slug)
            return Book.objects.filter(book_category=book_category)
        else:
            return Book.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['book_categories'] = BookCategories.objects.all()
        return context
