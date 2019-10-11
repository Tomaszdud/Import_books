from django import forms
import datetime

current = datetime.datetime.now()

class BookAddForm(forms.Form):
    title = forms.CharField()
    authors = forms.CharField(label='Authors (separated by a comma)')
    published_date = forms.DateField(required=False,widget = forms.SelectDateWidget(years=range(1,current.year+1)))
    page_count = forms.IntegerField(required=False)
    small_thumbnail_image_link = forms.URLField(required=False)
    thumbnail_image_link = forms.URLField(required=False)
    small_image_link = forms.URLField(required=False)
    medium_image_link = forms.URLField(required=False)
    large_image_link = forms.URLField(required=False)
    extralarge_image_link = forms.URLField(required=False)
    language = forms.CharField(required=False,label='Language (acronym)')
    type_industry = forms.CharField(required=False)
    identifier_industry = forms.CharField(required=False)
    second_type_industry = forms.CharField(required=False)
    second_identifier_industry = forms.CharField(required=False)


class SearchBookForm(forms.Form):
    title = forms.CharField(required=False)
    authors = forms.CharField(required=False)
    published_date_from = forms.DateField(required=False,widget=forms.SelectDateWidget(years=range(1,current.year+1)))
    published_date_to = forms.DateField(required=False,widget=forms.SelectDateWidget(years=range(1,current.year+1)))
    language = forms.CharField(required=False,label='Language (acronym)')