from django.core.management.base import BaseCommand
from catalog.models import Author
import random


class Command(BaseCommand):
    help = 'Creates authors for database (from 10 to 1000)'

    def add_arguments(self, parser):
        parser.add_argument('quantity', type=int, choices=range(10, 1001))

    def handle(self, *args, **kwargs):
        quantity = kwargs['quantity']
        authors_list = []
        for number in range(quantity):
            authors_list.append(Author(name=f"Author{number}",
                                       age=random.randrange(30, 90)))
        Author.objects.bulk_create(authors_list)
        self.stdout.write(f"{quantity} authors have been created in database!")
