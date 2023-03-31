from django.contrib import admin  # noqa: F401

from .models import Author, Publisher, Book, Store  # noqa: F401


class BookAdmin(admin.ModelAdmin):
    list_display = ('name', 'pubdate', 'pages', 'price', 'rating', 'publisher')


admin.site.register(Book, BookAdmin)
