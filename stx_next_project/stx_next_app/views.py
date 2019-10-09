from django.shortcuts import render
from django.views.generic import ListView
from .models import Book,Author,ImageLinks,IndustryIdentifiers,BookAuthors

class BookList(ListView):
    template_name = 'book_list.html'

    def get_queryset(self):
        queryset = super(BookList, self).get_queryset()
        name = self.request.GET.get

        title = name('title')
        author = name('author') 
        language = name('language')
        publised_date = name('published_date')

        queryset = BookAuthors.objects.filter(title_icontains=title)
        return queryset