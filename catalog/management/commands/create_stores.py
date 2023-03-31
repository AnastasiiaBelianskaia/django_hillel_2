from django.core.management.base import BaseCommand
from catalog.models import Store, Book

import random


class Command(BaseCommand):
    help = 'Creates stores for database (from 10 to 1000)'

    def add_arguments(self, parser):
        parser.add_argument('quantity', type=int, choices=range(10, 1001))

    def handle(self, *args, **kwargs):
        quantity = kwargs['quantity']
        stores_list = []
        books_count = Book.objects.count()
        for number in range(quantity):
            stores_list.append(Store(name=f'Publisher{number}'))
        Store.objects.bulk_create(stores_list)
        stores_count = Store.objects.count()
        for store_num in range(1, stores_count):
            store = Store.objects.get(id=store_num)
            book = Book.objects.get(id=random.randrange(1, books_count))
            store.books.add(book)
        self.stdout.write(f"{quantity} stores have been created in database!")