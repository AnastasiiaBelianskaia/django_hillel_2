from django.core.management.base import BaseCommand
from catalog.models import Book, Author, Publisher
import random
from faker import Faker

fake = Faker()


class Command(BaseCommand):
    help = 'Creates books for database (from 100 to 1000). ! You need to create authors and publishers first !'

    def add_arguments(self, parser):
        parser.add_argument('quantity', type=int, choices=range(100, 1001))

    def handle(self, *args, **kwargs):
        quantity = kwargs['quantity']
        books_list = []
        publishers_count = Publisher.objects.count()
        authors_count = Author.objects.count()
        for number in range(quantity):
            publisher = Publisher.objects.get(id=random.randrange(1, publishers_count))
            books_list.append(Book(name=f"Book{number}",
                                   pages=random.randrange(200, 800),
                                   price=round(random.uniform(100, 3000), 2),
                                   rating=round(random.uniform(1, 10), 1),
                                   pubdate=fake.date_between(start_date='-200y', end_date='-1y'),
                                   publisher_id=publisher.id,
                                   ))

        Book.objects.bulk_create(books_list)
        books_count = Book.objects.count()
        for book_num in range(1, books_count):
            book = Book.objects.get(id=book_num)
            author = Author.objects.get(id=random.randrange(1, authors_count))
            book.authors.add(author)

        self.stdout.write(f"{quantity} books have been created in database!")
