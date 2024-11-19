from .views import BorrowBookView
from django.urls import path

urlpatterns = [
    path('borrow/', BorrowBookView.as_view(), name='borrow-book'),
]