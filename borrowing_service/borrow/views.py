import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import BorrowedBook
from django.contrib.auth.models import User

CATALOG_SERVICE_URL = "http://localhost:8002/catalog/books/"  # URL of your catalog service

class BorrowBookView(APIView):

    def post(self, request, *args, **kwargs):
        book_id = request.data.get("book_id")
        #change this back to retrieve the user from NGINX request
        user_id = request.data.get("user")

        # Step 1: Check if the book is available by calling the Catalog Service API
        catalog_response = requests.get(f"{CATALOG_SERVICE_URL}{book_id}/")

        if catalog_response.status_code != 200:
            return Response({"error": "Book not found or unavailable."}, status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.get(id=user_id)
        # Step 2: Borrow the book and add it to the Borrowed Books table
        borrowed_book = BorrowedBook.objects.create(book_id=book_id, user=user)

        # Step 3: Optionally, mark the book as borrowed or remove it from the catalog
        catalog_update_response = requests.patch(
            f"{CATALOG_SERVICE_URL}{book_id}/", 
            data={"status": "borrowed"}
        )

        if catalog_update_response.status_code != 200:
            return Response({"error": "Failed to update catalog."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({
            "message": f"Book {borrowed_book} borrowed successfully."
        }, status=status.HTTP_201_CREATED)


class ReturnBookView(APIView):
    # Add IsAuthenticated if integrating with NGINX
    # permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        book_id = request.data.get("book_id")
        user_id = request.data.get("user")

        try:
            # Step 1: Find the borrowed book record
            borrowed_book = BorrowedBook.objects.get(book_id=book_id, user__id=user_id)
        except BorrowedBook.DoesNotExist:
            return Response({"error": "No record of this book being borrowed."}, status=status.HTTP_404_NOT_FOUND)

        # Step 2: Delete the record from Borrowed Books table
        borrowed_book.delete()

        # Step 3: Update the book status in the catalog
        catalog_update_response = requests.patch(
            f"{CATALOG_SERVICE_URL}{book_id}/",
            data={"status": "available"}
        )

        if catalog_update_response.status_code != 200:
            print(f"Error updating catalog: {catalog_update_response.status_code}")
            print(f"Response content: {catalog_update_response.text}")
            return Response({"error": "Failed to update catalog."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({
            "message": f"Book {book_id} returned successfully."
        }, status=status.HTTP_200_OK)