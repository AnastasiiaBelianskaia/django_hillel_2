from django.db.models import Avg, Count, Max, Min, Q
from django.shortcuts import get_object_or_404, render

from .models import Author, Book, Publisher, Store


def index(request):
    return render(request, 'catalog/index.html')


def authors(request):
    avg_age_rounded = round(Author.objects.aggregate(Avg('age'))['age__avg'])
    oldest_book = Author.objects.aggregate(oldest_book=Min('books__pubdate'))
    all_authors = Author.objects.prefetch_related('books')
    authors_values_list = []
    for author in all_authors:
        all_books = [books.name for books in author.books.all()]
        authors_values_list.append({'name': author.name,
                                    'age': author.age,
                                    'books': all_books,
                                    'id': author.id})
    return render(request, 'catalog/authors_list.html', {'authors': authors_values_list,
                                                         'average_age_rounded': avg_age_rounded,
                                                         'oldest_book': oldest_book,
                                                         })


def author_details(request, pk):
    author = get_object_or_404(Author, id=pk)
    author_books = author.display_books()
    above_500_pages = Count('books', filter=Q(books__pages__gt=500))
    below_500_pages = Count('books', filter=Q(books__pages__lte=500))
    auths = Author.objects.annotate(above_500_pages=above_500_pages).annotate(below_500_pages=below_500_pages)
    above_500 = auths[pk-1].above_500_pages
    below_500 = auths[pk-1].below_500_pages
    return render(request, 'catalog/author_details.html', {'author': author,
                                                           'books': author_books,
                                                           'gt_500_pages': above_500,
                                                           'lte_500_pages': below_500})


def books(request):
    books_count = Book.objects.count()
    avg_price_rounded = round(Book.objects.aggregate(Avg('price'))['price__avg'])
    pages_values = Book.objects.aggregate(Max('pages'), Min('pages'))
    all_books = Book.objects.prefetch_related('authors', 'stores')
    queryset = Book.objects.select_related('publisher').all()
    books_values_list = []
    for book in all_books:
        all_authors = [authors.name for authors in book.authors.all()]
        all_stores = [stores.name for stores in book.stores.all()]
        books_values_list.append({'name': book.name,
                                  'pubdate': book.pubdate,
                                  'rating': book.rating,
                                  'price': book.price,
                                  'authors': all_authors,
                                  'stores': all_stores,
                                  'id': book.id})
    element_index = 0
    for book in queryset:
        books_values_list[element_index].update({'publisher': book.publisher.name})
        element_index += 1

    return render(request, 'catalog/books_list.html', {'books': books_values_list,
                                                       'books_count': books_count,
                                                       'avg_price_rounded': avg_price_rounded,
                                                       'pages_values': pages_values})


def book_details(request, pk):
    book = get_object_or_404(Book, id=pk)
    return render(request, 'catalog/book_details.html', {'book': book})


def publishers(request):
    all_publishers = Publisher.objects.prefetch_related('books')
    publishers_values_list = []
    for publisher in all_publishers:
        all_books = [books.name for books in publisher.books.all()]
        publishers_values_list.append({'name': publisher.name,
                                       'books': all_books,
                                       'id': publisher.id})
    return render(request, 'catalog/publishers_list.html', {'publishers': publishers_values_list})


def publisher_details(request, pk):
    publisher = get_object_or_404(Publisher, id=pk)
    pub_books = publisher.display_books()
    average_rating = Avg('books__rating')
    pubs = Publisher.objects.annotate(average_rating=average_rating)
    books_avg_rating = pubs[pk-1].average_rating
    return render(request, 'catalog/publisher_details.html', {'publisher': publisher,
                                                              'books': pub_books,
                                                              'books_avg_rating': books_avg_rating})


def stores(request):
    stores = Store.objects.prefetch_related('books')
    stores_values_list = []
    for store in stores:
        books = [books.name for books in store.books.all()]
        stores_values_list.append({'name': store.name,
                                   'books': books,
                                   'id': store.id})
    return render(request, 'catalog/stores_list.html', {'stores': stores_values_list})


def store_details(request, pk):
    store = get_object_or_404(Store, id=pk)
    average_price = Avg('books__price')
    stores = Store.objects.annotate(average_price=average_price)
    books_avg_price = round(stores[pk-1].average_price, 2)
    return render(request, 'catalog/store_details.html', {'store': store,
                                                          'books_avg_price': books_avg_price})
