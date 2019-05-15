from django.contrib import admin

from books.models import Book, Category, Author

admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Book)
