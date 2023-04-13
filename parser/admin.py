from django.contrib import admin

from .models import AuthorOfQuote, Quote


class AuthorOfQuoteAdmin(admin.ModelAdmin):
    list_display = ['name', 'born_date', 'born_location']
    fields = ('name', 'born_date', 'born_location', 'description')


class QuoteAdmin(admin.ModelAdmin):
    list_display = ('text', 'author')
    raw_id_fields = ('author',)
    search_fields = ['author__name']
    search_help_text = 'Search by author name'


admin.site.register(AuthorOfQuote, AuthorOfQuoteAdmin)
admin.site.register(Quote, QuoteAdmin)
