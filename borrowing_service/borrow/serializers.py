from rest_framework import serializers
from .models import BorrowedBook

class BorrowedBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = BorrowedBook
        fields = ['user', 'book_id', 'borrow_date', 'return_date']
