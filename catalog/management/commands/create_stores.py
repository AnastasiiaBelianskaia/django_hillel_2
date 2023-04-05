import random

from catalog.models import Book, Store

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Creates stores for database (from 10 to 1000)'  # noqa: A003

    def add_arguments(self, parser):
        parser.add_argument('quantity', type=int, choices=range(10, 1001))

    def handle(self, *args, **kwargs):
        quantity = kwargs['quantity']
        stores_list = []
        for number in range(quantity):
            stores_list.append(Store(name=f'Store{number}'))
        stores = Store.objects.bulk_create(stores_list)
        for store in stores:
            store.books.set(Book.objects.values_list("id", flat=True).order_by('?')[:random.randint(0, 5)])
        self.stdout.write(f"{quantity} stores have been created in database!")
