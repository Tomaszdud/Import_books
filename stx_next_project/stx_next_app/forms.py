from django import forms

class BookAddForm(forms.Form):
    title = forms.CharField()
    authors = forms.CharField()
    published_date = forms.DateField()
    page_count = forms.IntegerField()
    image_links = forms.URLField()
    language = forms.CharField()
    type_industry = forms.CharField()
    identifier_industry = forms.CharField()
    sec_type_industry = forms.CharField()
    sec_identifier_industry = forms.CharField()