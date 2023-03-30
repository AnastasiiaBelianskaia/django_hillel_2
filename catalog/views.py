from django.http import HttpResponse
from django.shortcuts import render  # noqa: F401


def index(request):
    return HttpResponse('Hello, world! You are at the catalog index')
