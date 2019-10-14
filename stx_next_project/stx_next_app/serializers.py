from rest_framework import serializers
from .models import *

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookAuthors
        fields=['author']
        depth = 3

