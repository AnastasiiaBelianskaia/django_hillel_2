from django.core import management
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Fills database with users, authors, publishers, books and stores. Range 100-1000'  # noqa: A003

    def add_arguments(self, parser):
        parser.add_argument('quantity', type=int, choices=range(100, 1001))

    def handle(self, *args, **kwargs):
        quantity = kwargs['quantity']

        management.call_command('create_authors', quantity)
        management.call_command('create_publishers', quantity)
        management.call_command('create_books', quantity)
        management.call_command('create_stores', quantity)
        management.call_command('create_users', quantity)
