from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView,CreateView, FormView
from .models import Book,ImageLinks,IndustryIdentifiers
from .forms import BookAddForm

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


class BookAdd(FormView):
    form_class = BookAddForm
    template_name = 'book_add.html'
    success_url = reverse_lazy('book_list')

    def form_valid(self,form):
        pass


