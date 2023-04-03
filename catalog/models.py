from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()

    def __str__(self):
        return self.name

    def display_books(self):
        return ', '.join(book.name for book in self.books.all())

    display_books.short_description = 'Books'


class Publisher(models.Model):
    name = models.CharField(max_length=300)

    def __str__(self):
        return self.name

    def display_books(self):
        return ', '.join(book.name for book in self.books.all())

    display_books.short_description = 'Books'


class Book(models.Model):
    name = models.CharField(max_length=300)
    pages = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    rating = models.FloatField()
    authors = models.ManyToManyField(Author, related_name='books')
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE, blank=True, null=True, related_name='books')
    pubdate = models.DateField()

    def __str__(self):
        return self.name

    def display_authors(self):
        return ', '.join(author.name for author in self.authors.all())

    display_authors.short_description = 'Author'


class Store(models.Model):
    name = models.CharField(max_length=300)
    books = models.ManyToManyField(Book, related_name='stores')

    def __str__(self):
        return self.name

    def display_books(self):
        return ', '.join(book.name for book in self.books.all())

    display_books.short_description = 'Books'
