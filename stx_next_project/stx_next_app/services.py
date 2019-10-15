import json
import requests
import re


def get_books(query, auth_key):

    url = 'https://www.googleapis.com/books/v1/volumes'
    params = {'q': query, 'maxResults': 3, 'key': auth_key}
    r = requests.get(url, params=params)
    books = r.json()
    books_list = books['items']

    return books_list


def camel_case_split(str):

    words = re.sub('([a-z])([A-Z])', r'\1 \2', str).split()

    new_word = ''
    iteration = 1
    for word in words:
        if iteration == len(words):
            new_word += word
            continue
        new_word += word+'_'
        iteration += 1

    return new_word.lower()
