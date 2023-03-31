from catalog.models import Publisher

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Creates publishers for database (from 10 to 1000)'  # noqa: A003

    def add_arguments(self, parser):
        parser.add_argument('quantity', type=int, choices=range(10, 1001))

    def handle(self, *args, **kwargs):
        quantity = kwargs['quantity']
        publishers_list = []
        for number in range(quantity):
            publishers_list.append(Publisher(name=f'Publisher{number}'))
        Publisher.objects.bulk_create(publishers_list)
        self.stdout.write(f"{quantity} publishers have been created in database!")
