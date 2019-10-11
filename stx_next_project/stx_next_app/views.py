from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView,CreateView, FormView
from .models import Book,ImageLinks,IndustryIdentifiers,BookAuthors, Authors
from .forms import BookAddForm, SearchBookForm
import datetime


class BookList(ListView):
    template_name = 'book_list.html'
    form_class = SearchBookForm
    current = datetime.datetime.now()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = SearchBookForm()
        return context

    def get_queryset(self):
        queryset = Book.objects.all()
        field = self.request.GET.get
        
        authors = field('authors','')
        title = field('title','')
        language = field('language','')
        published_date_from_month = field('published_date_from_month','')
        published_date_from_year = field('published_date_from_year','')
        published_date_from_day = field('published_date_from_day','')
        published_date_to_month = field('published_date_to_month','')
        published_date_to_year = field('published_date_to_year','')
        published_date_to_day = field('published_date_to_day','')

        published_date_from = published_date_from_year + '-' + published_date_from_month + '-' + published_date_from_day
        published_date_to = published_date_to_year + '-' + published_date_to_month + '-' + published_date_to_day

        if (authors is not '' and
            len(published_date_from) is 8 and
            len(published_date_to) is 8):

            queryset = BookAuthors.objects.filter(author__author__icontains=authors,
                                                    book__title__icontains=title,
                                                    book__language__icontains=language,
                                                    book__published_date__range=[published_date_from,published_date_to])
            return queryset

        elif authors is not '':

            queryset = BookAuthors.objects.filter(author__author__icontains=authors,
                                        book__title__icontains=title,
                                        book__language__icontains=language)
            return queryset

        elif (title is not '' or 
            language is not '' or
            len(published_date_from) is 8 and
             len(published_date_to) is 8):

            book = Book.objects.filter(title__icontains=title,
                                        language__icontains=language,
                                        published_date__range=[published_date_from,published_date_to])
            queryset = book
            return queryset

        return queryset



class BookAdd(FormView):
    form_class = BookAddForm
    template_name = 'book_add.html'
    success_url = reverse_lazy('book_list')

    def form_valid(self,form):
        data = form.cleaned_data

        title = data['title']
        authors = data['authors']
        published_date = data['published_date']
        page_count = data['page_count']
        small_thumbnail_image_link = data['small_thumbnail_image_link']
        thumbnail_image_link = data['thumbnail_image_link']
        small_image_link = data['small_image_link']
        medium_image_link = data['medium_image_link']
        large_image_link = data['large_image_link']
        extralarge_image_link = data['extralarge_image_link']
        language = data['language']
        type_industry = data['type_industry']
        identifier_industry = data['identifier_industry']
        second_type_industry = data['second_type_industry']
        second_identifier_industry = data['second_identifier_industry']

        images = ImageLinks.objects.create(small_thumbnail=small_thumbnail_image_link,
                                thumbnail=thumbnail_image_link,
                                small=small_image_link,
                                medium=medium_image_link,
                                large=large_image_link,
                                extraLarge=extralarge_image_link)
        images.save()

        book = Book.objects.create(title=title,
                            published_date=published_date,
                            page_count=page_count,
                            image_links=images,
                            language=language)
        
        book.save()

        for new_author in authors.split(','):
            author = Authors.objects.create(author=new_author)
            author.save()
            book_authors = BookAuthors.objects.create(book=book,author=author)
            book_authors.save()

        industry = IndustryIdentifiers.objects.create(type=type_industry,
                                            identifier=identifier_industry,
                                            book=book)
        industry.save()

        second_industry = IndustryIdentifiers.objects.create(type=second_type_industry,
                                            identifier=second_identifier_industry,
                                            book=book)
        second_industry.save()

        return super().form_valid(form)


