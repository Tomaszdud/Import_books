from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView,CreateView, FormView, TemplateView
from .models import Book,ImageLinks,IndustryIdentifiers,BookAuthors, Authors
from .forms import BookAddForm, BookSearchForm, BookImportForm
import datetime
from .services import get_books, camel_case_split


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

                try:

                    book = books[index]['volumeInfo']

                    first_loop=True
                    for key,value in book.items():
                        if key == 'imageLinks':

                            for k,v in value.items():
                                k = camel_case_split(k)
                                if first_loop:
                                    links = ImageLinks.objects.create(**{k:v})
                                    first_loop = False
                                    continue
                                setattr(links,k,v)
                                links.save()                                
                                        
                        continue

                except KeyError:
                    pass

                try:
                    first_loop=True
                    for key,value in book.items():
                        key = camel_case_split(key)
                        if first_loop:
                            model_book = Book.objects.create(**{key:value},image_links=links)
                            first_loop = False
                            continue
                        elif key == 'authors':
                            for name in book[key]:
                                author = Authors.objects.create(author=name)
                                BookAuthors.objects.create(book=model_book,author=author)
                        elif key == 'language':
                            setattr(model_book,key,value)
                            model_book.save()
                        elif key == 'page_count':
                            setattr(model_book,key,value)
                        elif key == 'published_date':
                            setattr(model_book,key,value)                 
                        elif key == 'industry_identifiers':
                            first_l=True
                            for i in range(len(book['industryIdentifiers'])):
                                for field, val in book['industryIdentifiers'][i].items():
                                    if first_loop:
                                        industry = IndustryIdentifiers.objects.create(**{field:val},book=model_book)
                                        industry.save()
                                        first_loop=False
                                        continue
                                    x = IndustryIdentifiers.objects.order_by("-pk")[0]
                                    setattr(x,field,val)
                                    x.save()
                                    first_l = True
                except Exception:
                    print('ops'.s)

        return super().get(request)