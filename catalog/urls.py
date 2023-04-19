from django.urls import path

from . import views

app_name = 'catalog'
urlpatterns = [
    path('', views.index, name='index'),
    path('authors/', views.authors, name='authors'),
    path('authors/<int:pk>/', views.author_details, name='author_details'),
    path('books/', views.BooksListView.as_view(), name='books'),
    path('books/<int:pk>/', views.BooksDetailView.as_view(), name='book_details'),
    path('books/create/', views.BookCreate.as_view(), name='book_create'),
    path('books/<int:pk>/update/', views.BookUpdate.as_view(), name='book_update'),
    path('books/<int:pk>/delete/', views.BookDelete.as_view(), name='book_delete'),
    path('publishers/', views.publishers, name='publishers'),
    path('publishers/<int:pk>/', views.publisher_details, name='publisher_details'),
    path('stores/', views.stores, name='stores'),
    path('stores/<int:pk>/', views.store_details, name='store_details'),
    path('notification/', views.celery, name='celery'),
    path('set_timezone/', views.set_timezone, name='set_timezone'),
]
