import requests
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import View
from django.views.generic import ListView, CreateView, TemplateView

from books.forms import AddNewBookForm, AddNewAuthorForm, AddNewCategoryForm
from books.models import Book, Author, Category


class HomeView(View):

    def get(self, request, *args, **kwargs):
        current_books = Book.objects.all().count()
        context = {
            'current_books': current_books
        }

        return render(request, 'base.html', context)


def filter_qs(request):
    authors = request.GET.get('authors')
    title = request.GET.get('title')
    queryset = Book.objects.all()

    if authors is None and title is None or authors == '' and title == '':
        qs = queryset
    elif authors == '':
        qs = queryset.filter(title__icontains=title)
    elif title == '':
        qs = queryset.filter(authors__name__icontains=authors)
    else:
        qs = queryset.filter(Q(title__icontains=title)
                             | Q(authors__name__icontains=authors)
                             ).distinct()

    return qs.order_by('title')


class BookListView(ListView):
    template_name = 'books_list.html'
    paginate_by = 5
    context_object_name = 'books'

    def get_queryset(self):
        queryset = filter_qs(self.request)
        return queryset


class AddNewBookView(SuccessMessageMixin, CreateView):
    template_name = 'add_book.html'
    form_class = AddNewBookForm

    def form_valid(self, form):
        return super().form_valid(form)

    def get_success_message(self, cleaned_data):
        return f"Book: <strong>{cleaned_data['title']}</strong>, has been added correct!"

    def get_success_url(self):
        return reverse('books')


class AddNewAuthorView(SuccessMessageMixin, CreateView):
    template_name = 'add_author.html'
    form_class = AddNewAuthorForm

    def form_valid(self, form):
        author_name = form.cleaned_data['name']
        if not Author.objects.filter(name=author_name).exists():
            messages.success(self.request, f"Author: <strong>{author_name}</strong>, has been added correct!")
            return super().form_valid(form)
        else:
            messages.warning(self.request, 'Author already exists!')
            return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('add')


class AddNewCategoryView(SuccessMessageMixin, CreateView):
    template_name = 'add_category.html'
    form_class = AddNewCategoryForm

    def form_valid(self, form):
        category_name = form.cleaned_data['name']
        if not Category.objects.filter(name=category_name).exists():
            messages.success(self.request, f"Category: <strong>{category_name}</strong>, has been added correct!")
            return super().form_valid(form)
        else:
            messages.warning(self.request, 'Category already exists!')
            return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('add')


def if_api_exists(item, field):
    try:
        if field == 'imageLinks':
            result = item[field]['thumbnail']
        else:
            result = item[field]
    except:
        if field == 'description':
            result = 'Lorem ipsum... no description about this book.'
        elif field == 'categories':
            result = ['Without categories']
        elif field == 'authors':
            result = ['Without authors']
        elif field == 'imageLinks':
            result = False
        else:
            result = ['Without data']

    return result


class ImportAPIView(TemplateView):
    template_name = 'import_view.html'

    def get(self, request, *args, **kwargs):
        value = request.GET.get('value')
        context = {
            'value': value
        }
        try:
            if value is not None:
                api_url = f'https://www.googleapis.com/books/v1/volumes?q={value}&maxResults=5'
                api_request = requests.get(api_url)
                json_data = api_request.json()

                added_books = 0
                no_added_books = 0
                if 'items' in json_data:
                    for item in json_data['items']:
                        authors = if_api_exists(item['volumeInfo'], 'authors')
                        categories = if_api_exists(item['volumeInfo'], 'categories')
                        title = if_api_exists(item['volumeInfo'], 'title')
                        description = if_api_exists(item['volumeInfo'], 'description')
                        api_key = item['id']
                        thumbnail = if_api_exists(item['volumeInfo'], 'imageLinks')

                        if not Book.objects.filter(api_key=api_key).exists():
                            create_author = None
                            authors_array = []
                            for author in authors:
                                if not Author.objects.filter(name=author).exists():
                                    create_author = Author.objects.create(name=author)
                                    create_author.save()
                                    authors_array.append(create_author)
                                else:
                                    create_author = Author.objects.get(name=author)
                                    authors_array.append(create_author)

                            create_category = None
                            categories_array = []
                            for category in categories:
                                if not Category.objects.filter(name=category).exists():
                                    create_category = Category.objects.create(name=category)
                                    categories_array.append(create_category)
                                else:
                                    create_category = Category.objects.get(name=category)
                                    categories_array.append(create_category)

                            create_book = Book()
                            create_book.save()
                            for author in authors_array:
                                create_book.authors.add(author)

                            for category in categories_array:
                                create_book.categories.add(category)

                            create_book.title = title
                            create_book.description = description
                            create_book.api_key = api_key
                            if thumbnail is not False:
                                create_book.thumbnail = thumbnail
                            create_book.save()
                            added_books += 1
                        else:
                            no_added_books += 1
                else:
                    context['no_results'] = True

                context['added_books'] = added_books
                context['no_added_books'] = no_added_books
        except:
            context['exception'] = True

        return render(request, 'import_view.html', context)
