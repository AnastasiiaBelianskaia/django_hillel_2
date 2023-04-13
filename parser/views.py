from django.shortcuts import render
from .models import Quote


def index(request):
    return render(request, 'parser/index.html')


def quotes_list(request):
    quotes = Quote.objects.all()
    return render(request, 'parser/quotes_list.html', {'quotes': quotes})
