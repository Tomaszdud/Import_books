from django.shortcuts import render
from django.views.generic import ListView
from .models import Book,Author,ImageLinks,IndustryIdentifiers,BookAuthors

class BookList(ListView):
    template_name = 'book_list.html'
    def get_queryset(self):
        pass
    def get_context_data(self):
        pass