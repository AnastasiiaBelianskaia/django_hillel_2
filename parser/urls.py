from django.urls import path

from . import views

app_name = 'parser'
urlpatterns = [
    path('', views.index, name='index'),
    path('quotes/', views.quotes_list, name='quotes_list'),
    ]
