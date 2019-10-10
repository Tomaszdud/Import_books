from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView,CreateView, FormView
from .models import Book,ImageLinks,IndustryIdentifiers,BookAuthors, Authors
from .forms import BookAddForm

class BookAdd(FormView):
    form_class = BookAddForm
    template_name = 'book_add.html'
    success_url = reverse_lazy('book_add')

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


