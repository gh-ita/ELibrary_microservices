from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Book
from .serializers import BookSerializer
from rest_framework.permissions import IsAuthenticated

class BookListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)

class BookDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        book_id = kwargs['pk']
        try:
            book = Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            return Response({"error": "Book not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = BookSerializer(book)
        return Response(serializer.data)

    def patch(self, request, *args, **kwargs):
        book_id = kwargs['pk']
        try:
            book = Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            return Response({"error": "Book not found."}, status=status.HTTP_404_NOT_FOUND)

        # Update the book's status
        if book.status == 'borrowed':
            return Response({"error": "Book already borrowed."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Borrow the book
        book.borrow()
        return Response({"message": f"Book '{book.title}' borrowed successfully."}, status=status.HTTP_200_OK)
