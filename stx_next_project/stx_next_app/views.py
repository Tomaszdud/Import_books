from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView,CreateView, FormView, TemplateView
from .models import Book,ImageLinks,IndustryIdentifiers,BookAuthors, Authors
from .forms import BookAddForm, BookSearchForm, BookImportForm, BookFilter
import datetime
from .services import get_books, camel_case_split
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from .serializers import BookSerializer
from django_filters import rest_framework as filters


class BookList(ListView):
    template_name = 'book_list.html'
    form_class = BookSearchForm
    current = datetime.datetime.now()

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context['form'] = BookSearchForm()
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

        if ((len(published_date_from)>7 and len(published_date_from)< 11) and
             (len(published_date_to) >7 and len(published_date_to)<11)):

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

        elif title is not '' or language is not '':

            book = Book.objects.filter(title__icontains=title,
                                        language__icontains=language)
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
        extralarge_image_link = data['extra_large_image_link']
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
                                extra_large=extralarge_image_link)
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


class BooksImport(TemplateView):
    template_name = 'book_import.html'
    form_class = BookImportForm

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context['form'] = BookImportForm()
        return context


    def get(self,request,*args,**kwargs):

        auth_key = 'AIzaSyAhghFhEl4OCkdUGdCmJ646G8sAgO2k0WQ'
        query = request.GET.get('query')

        if query is not None:

            books = get_books(query,auth_key)

            for index in range(len(books)):
                    
                book = books[index].get('volumeInfo','')

                first_loop = True
                for k,v in book.get('imageLinks',{}).items():

                    k = camel_case_split(k)
                    if first_loop:
                        if k is not None:
                            links = ImageLinks.objects.create(**{k:v})
                            first_loop = False
                            continue
                    setattr(links,k,v)
                    links.save()

                if 3 < len(book.get('publishedDate','')) < 10 :
                    published_date = book.get('publishedDate') + '-' + '01' + '-' + '01'
                else:
                        published_date = book.get('publishedDate','')

                model_book = Book.objects.create(title=book.get('title',''),
                                    published_date=published_date,
                                    page_count=book.get('page_count'),
                                    image_links=links,
                                    language=book.get('language',''))

                for writer in book.get('authors',''):
                    author = Authors.objects.create(author=writer)
                    BookAuthors.objects.create(book=model_book,author=author)

                for i in range(len(book.get('industryIdentifiers',''))):
                    loop = 0
                    check = 1
                    for k,v in book.get('industryIdentifiers',{})[i].items():

                        k = camel_case_split(k)
                        if loop == check:
                            setattr(industry,k,v)
                            industry.save()
                            check +=1
                            continue
                        industry = IndustryIdentifiers.objects.create(**{k:v},book=model_book)
                        loop +=1
                    
        return super().get(request)


class BookRestView(ListAPIView):
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = BookFilter
    serializer_class = BookSerializer

    def get_queryset(self):

        try:
            queryset = BookAuthors.objects.all()
            return queryset
        except Book.DoesNotExist:
            raise Http404
