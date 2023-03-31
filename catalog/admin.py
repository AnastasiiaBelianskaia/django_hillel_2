from django.contrib import admin

from .models import Author, Book, Publisher, Store  # noqa: F401


class BookAdmin(admin.ModelAdmin):
    list_display = ('name', 'pubdate', 'pages', 'price', 'rating', 'publisher')


admin.site.register(Book, BookAdmin)
