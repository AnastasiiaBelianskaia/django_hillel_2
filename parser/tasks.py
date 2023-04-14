import logging
import re
from parser.models import AuthorOfQuote, Quote

from bs4 import BeautifulSoup

from celery import shared_task

from django.core.mail import send_mail

import requests


@shared_task
def quotes_parser():
    number_of_saved_quotes = 0
    page_number = 1
    while True:
        request_to_site = requests.get(f'https://quotes.toscrape.com/page/{page_number}')
        soup = BeautifulSoup(request_to_site.content, 'html.parser')
        for single_quote in soup.findAll('div', class_='quote'):
            text_of_quote = single_quote.find('span', class_='text').text.replace('”', '').replace('“', '')
            if Quote.objects.filter(text=text_of_quote).exists():
                continue
            author_name = single_quote.find('small', class_='author')
            author_url = author_name.find_next_sibling('a', href=True)['href']
            request_to_author_page = requests.get(f'http://quotes.toscrape.com{author_url}')
            author_soup = BeautifulSoup(request_to_author_page.content, 'html.parser')
            author_born_date = author_soup.find('span', class_='author-born-date').text
            author_born_location = author_soup.find('span', class_='author-born-location').text
            author_description = author_soup.find('div', class_='author-description').text.replace('\n', '')
            first_sentences_from_description = '.'.join(re.split(r'[.]', author_description)[:5])
            author = AuthorOfQuote.objects.get_or_create(name=author_name.text,
                                                         born_date=author_born_date,
                                                         born_location=author_born_location,
                                                         description=first_sentences_from_description)
            quote = Quote(text=text_of_quote, author_id=author[0].id)
            quote.save()
            number_of_saved_quotes += 1
            if number_of_saved_quotes == 5:
                return
        go_to_next_page = soup.find('li', class_='next')
        page_number += 1
        if not go_to_next_page:
            send_email()
            return


@shared_task
def send_authors_quotes_to_email(author_id):
    try:
        author = AuthorOfQuote.objects.get(id=author_id)
        quotes = list(author.quotes.values_list('text', flat=True))
        return send_mail(
            'Quotes from author',
            f'{quotes}',
            'from@example.com',
            ['to@example.com'],
            fail_silently=False,
        )
    except AuthorOfQuote.DoesNotExist:
        logging.error('Author does not exist')


def send_email():
    send_mail(
        'Quotes parser',
        'All quotes have been saved to db',
        'from@example.com',
        ['to@example.com'],
        fail_silently=False,
    )
