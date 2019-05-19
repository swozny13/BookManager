from django.urls import path

from books.views import BookListView, AddNewBookView, AddNewAuthorView, AddNewCategoryView, ImportAPIView

urlpatterns = [
    path('list', BookListView.as_view(), name='books'),
    path('add', AddNewBookView.as_view(), name='add'),
    path('author/add', AddNewAuthorView.as_view(), name='add_author'),
    path('category/add', AddNewCategoryView.as_view(), name='add_category'),
    path('api', ImportAPIView.as_view(), name='api')
]
