from django.shortcuts import render  # noqa: F401
from django.http import HttpResponse


def index(request):
    return HttpResponse('Hello, world! You are at the catalog index')
