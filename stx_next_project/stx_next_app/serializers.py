from rest_framework import serializers
from .models import *


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookAuthors
        fields = ['author', 'book']
        depth = 2

