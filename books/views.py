from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render
from django.urls import reverse
from django.views import View
from django.views.generic import ListView, CreateView

from books.forms import AddNewBookForm
from books.models import Book


class HomeView(View):

    def get(self, request, *args, **kwargs):
        current_books = Book.objects.all().count()
        context = {
            'current_books': current_books
        }

        return render(request, 'base.html', context)


class BookListView(ListView):
    template_name = 'books_list.html'
    paginate_by = 5
    context_object_name = 'books'
    queryset = Book.objects.all().order_by('title')


class AddNewBookView(SuccessMessageMixin, CreateView):
    template_name = 'add_book.html'
    form_class = AddNewBookForm
    queryset = Book.objects.all()

    def form_valid(self, form):
        return super().form_valid(form)

    def get_success_message(self, cleaned_data):
        return f"Book: <strong>{cleaned_data['title']}</strong>, has been added correct!"

    def get_success_url(self):
        return reverse('books')


class SearchAPIView(View):
    def get(self, request, *args, **kwargs):
        context = {}

        return render(request, 'search_view.html', context)
