from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Avg, Count, Max, Min, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views import generic

from .forms import CeleryForm
from .models import Author, Book, Publisher, Store
from .tasks import send_email_celery

common_timezones = ['Europe/Kyiv', 'Europe/Helsinki', 'Etc/Greenwich', 'Europe/London']


def index(request):
    return render(request, 'catalog/index.html')


def authors(request):
    vals = Author.objects.aggregate(Avg('age'), Min('books__pubdate'))
    all_authors = Author.objects.prefetch_related('books')
    return render(request, 'catalog/authors_list.html', {'aggr_values': vals,
                                                         'authors': all_authors})


def author_details(request, pk):
    above_500_pages = Count('books', filter=Q(books__pages__gt=500))
    below_500_pages = Count('books', filter=Q(books__pages__lte=500))
    author = get_object_or_404(
        Author.objects.annotate(above_500_pages=above_500_pages).annotate(below_500_pages=below_500_pages),
        id=pk)
    return render(request, 'catalog/author_details.html', {'author': author})


class BooksListView(generic.ListView):
    model = Book
    template_name = 'catalog/books_list.html'
    paginate_by = 10

    def get_queryset(self):
        return Book.objects.prefetch_related('authors', 'stores').select_related('publisher')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['values'] = Book.objects.aggregate(Max('pages'), Min('pages'), Avg('price'), Count("id"))
        return context


class BooksDetailView(generic.DetailView):
    model = Book
    template_name = 'catalog/book_details.html'


class BookCreate(LoginRequiredMixin, generic.CreateView):
    model = Book
    fields = ['name', 'pages', 'price', 'authors', 'publisher', 'pubdate']
    success_url = reverse_lazy('catalog:books')


class BookUpdate(LoginRequiredMixin, generic.UpdateView):
    model = Book
    fields = ['name', 'pages', 'price', 'authors', 'publisher', 'pubdate']


class BookDelete(LoginRequiredMixin, generic.DeleteView):
    model = Book
    success_url = reverse_lazy('catalog:books')


def publishers(request):
    all_publishers = Publisher.objects.prefetch_related('books')
    return render(request, 'catalog/publishers_list.html', {'publishers': all_publishers})


def publisher_details(request, pk):
    publisher = get_object_or_404(Publisher.objects.annotate(average_rating=Avg('books__rating')), id=pk)
    return render(request, 'catalog/publisher_details.html', {'publisher': publisher})


def stores(request):
    all_stores = Store.objects.prefetch_related('books')
    return render(request, 'catalog/stores_list.html', {'stores': all_stores})


def store_details(request, pk):
    store = get_object_or_404(Store.objects.annotate(average_price=Avg('books__price')), id=pk)
    return render(request, 'catalog/store_details.html', {'store': store})


def set_timezone(request):
    if request.method == 'POST':
        request.session['django_timezone'] = request.POST['timezone']
        return redirect('catalog:celery')
    else:
        return render(request, 'catalog/set_timezone.html', {'timezones': common_timezones})


def celery(request):
    if not request.session.get('django_timezone'):
        return redirect('catalog:set_timezone')
    if request.method == 'POST':
        celery_form = CeleryForm(request.POST)
        if celery_form.is_valid():
            email = celery_form.cleaned_data['email']
            text = celery_form.cleaned_data['notification_text']
            time = celery_form.cleaned_data['date_time']
            send_email_celery.apply_async((email, text), eta=time)
            return redirect('catalog:celery')
    else:
        celery_form = CeleryForm()
    return render(request, 'catalog/form_for_notification.html', {'celery_form': celery_form})
