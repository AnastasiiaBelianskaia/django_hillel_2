import re

from celery import shared_task

from parser.models import AuthorOfQuote, Quote

import requests
from bs4 import BeautifulSoup
from django.core.mail import send_mail


@shared_task
def quotes_parser():
    number_of_saved_quotes = 0
    page_number = 1
    while True:
        request_to_site = requests.get(f'https://quotes.toscrape.com/page/{page_number}')
        soup = BeautifulSoup(request_to_site.content, 'html.parser')
        for single_quote in soup.findAll('div', class_='quote'):
            text_of_quote = single_quote.find('span', class_='text').text.replace('”', '').replace('“', '')
            if Quote.objects.filter(text=text_of_quote):
                continue
            author_name = single_quote.find('small', class_='author')
            author_url = author_name.find_next_sibling('a', href=True)['href']
            author = AuthorOfQuote.objects.get_or_create(name=author_name.text)
            authors_parser(author_url, pk=author[0].id)
            quote = Quote(text=text_of_quote, author_id=author[0].id)
            quote.save()
            number_of_saved_quotes += 1
            if number_of_saved_quotes == 5:
                return
        go_to_next_page = soup.find('li', class_='next')
        page_number += 1
        if not go_to_next_page:
            return send_mail(
                'Quotes parser',
                'All quotes have been saved to db',
                'from@example.com',
                ['to@example.com'],
                fail_silently=False,
            )


def authors_parser(url, pk):
    request_to_site = requests.get(f'http://quotes.toscrape.com{url}')
    soup = BeautifulSoup(request_to_site.content, 'html.parser')

    author_born_date = soup.find('span', class_='author-born-date').text
    author_born_location = soup.find('span', class_='author-born-location').text
    author_description = soup.find('div', class_='author-description').text.replace('\n', '')
    first_sentences_from_description = '.'.join(re.split(r'[.]', author_description)[:5])

    author = AuthorOfQuote.objects.get(id=pk)
    author.born_date = author_born_date
    author.born_location = author_born_location
    author.description = first_sentences_from_description
    author.save()
