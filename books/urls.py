from django.urls import path

from books.views import (
    BookListView,
    AddNewBookView,
    SearchAPIView
)

urlpatterns = [
    path('list', BookListView.as_view(), name='books'),
    path('add', AddNewBookView.as_view(), name='add'),
    path('api', SearchAPIView.as_view(), name='api')
]
