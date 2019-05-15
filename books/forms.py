from django import forms

from books.models import Book


class AddNewBookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = [
            'title',
            'authors',
            'categories',
            'description',
        ]
