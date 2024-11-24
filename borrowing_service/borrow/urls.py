from .views import BorrowBookView, ReturnBookView
from django.urls import path

urlpatterns = [
    path('borrow/', BorrowBookView.as_view(), name='borrow-book'),
    path("return/",  ReturnBookView.as_view(), name='return-book')
]