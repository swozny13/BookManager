from django import forms

from books.models import Book, Author, Category


class AddNewBookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = [
            'title',
            'authors',
            'categories',
            'description',
        ]


class AddNewAuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = [
            'name'
        ]


class AddNewCategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = [
            'name'
        ]
