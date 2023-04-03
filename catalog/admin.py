from django.contrib import admin

from .models import Author, Book, Publisher, Store  # noqa: F401


class BooksInLine(admin.TabularInline):
    model = Book


class BookAdmin(admin.ModelAdmin):
    list_display = ('name', 'display_authors', 'pubdate', 'pages', 'price', 'rating', 'publisher')
    search_fields = ['name', 'authors__name', 'publisher__name']
    search_help_text = 'Search by title, author or publisher'
    date_hierarchy = 'pubdate'
    fieldsets = (
        ('Base info', {
            'fields': ('name', 'price')
        }),
        ('More', {
            'fields': (('pages', 'rating'), 'pubdate', 'publisher')
        }),
    )


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'age', 'display_books')


class PublisherAdmin(admin.ModelAdmin):
    list_display = ['name', 'display_books']
    search_fields = ['name', 'books__name']
    search_help_text = 'Search by publisher name or book title'
    inlines = [BooksInLine]


class StoreAdmin(admin.ModelAdmin):
    list_display = ['name', 'display_books']
    search_fields = ['name', 'books__name', 'books__authors__name']
    search_help_text = 'Search by store name, author name or book title'


admin.site.register(Book, BookAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Publisher, PublisherAdmin)
admin.site.register(Store, StoreAdmin)
