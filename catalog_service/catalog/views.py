from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Book
from .serializers import BookSerializer
from rest_framework.permissions import IsAuthenticated

class BookListView(APIView):

    def get(self, request, *args, **kwargs):
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)

class BookDetailView(APIView):

    def get(self, request, *args, **kwargs):
        book_id = kwargs['pk']
        try:
            book = Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            return Response({"error": "Book not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = BookSerializer(book)
        return Response(serializer.data)

    def patch(self, request, *args, **kwargs):
        # Access the book_id (primary key) from the URL
        book_id = kwargs['pk']
        
        # Retrieve the status value from the request body
        status_value = request.data.get("status")

        try:
            # Get the book object by primary key
            book = Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            return Response({"error": "Book not found."}, status=status.HTTP_404_NOT_FOUND)

        # Check if the status value is provided
        if not status_value:
            return Response({"error": "Status is required."}, status=status.HTTP_400_BAD_REQUEST)

        # Update the book's status
        if status_value == 'borrowed':
            if book.status == 'borrowed':
                return Response({"error": "Book already borrowed."}, status=status.HTTP_400_BAD_REQUEST)
            # If status is 'borrowed', perform the borrowing logic (e.g., mark as borrowed)
            book.status = 'borrowed'
            # You could add more logic to mark the book as borrowed (e.g., associate with a user)
            book.borrow()

        elif status_value == 'available':
            if book.status == 'available':
                return Response({"error": "Book is already available."}, status=status.HTTP_400_BAD_REQUEST)
            # If status is 'available', update accordingly
            book.status = 'available'
            book.return_book()

        else:
            return Response({"error": "Invalid status."}, status=status.HTTP_400_BAD_REQUEST)

        # Save the updated book status
        

        return Response({"message": f"Book '{book.title}' status updated to {book.status}."}, status=status.HTTP_200_OK)
