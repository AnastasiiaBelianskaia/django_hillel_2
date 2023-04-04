import random

from catalog.models import Author, Book, Publisher

from django.core.management.base import BaseCommand

from faker import Faker

fake = Faker()


class Command(BaseCommand):
    help = 'Creates books for database (from 100 to 1000).You need to create authors and publishers first'  # noqa: A003

    def add_arguments(self, parser):
        parser.add_argument('quantity', type=int, choices=range(100, 1001))

    def handle(self, *args, **kwargs):
        quantity = kwargs['quantity']
        books_list = []
        for number in range(quantity):
            books_list.append(Book(name=f"Book{number}",
                                   pages=random.randrange(200, 800),
                                   price=round(random.uniform(100, 3000), 2),
                                   rating=round(random.uniform(1, 10), 1),
                                   pubdate=fake.date_between(start_date='-200y', end_date='-1y'),
                                   publisher_id=Publisher.objects.values_list("id", flat=True).order_by('?'),
                                   ))
        Book.objects.bulk_create(books_list)
        for book_num in Book.objects.values_list("id", flat=True):
            book = Book.objects.get(id=book_num)
            book.authors.set(Author.objects.values_list("id", flat=True).order_by('?')[:random.randint(1, 3)])

        self.stdout.write(f"{quantity} books have been created in database!")
