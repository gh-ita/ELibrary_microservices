import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import BorrowedBook
from .serializers import BorrowedBookSerializer

CATALOG_SERVICE_URL = "http://localhost:8002/api/catalog/books/"  # URL of your catalog service

class BorrowBookView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        book_id = request.data.get("book_id")
        user = request.user

        # Step 1: Check if the book is available by calling the Catalog Service API
        catalog_response = requests.get(f"{CATALOG_SERVICE_URL}{book_id}/", headers={
            'Authorization': f'Bearer {request.headers.get("Authorization").split(" ")[1]}'
        })

        if catalog_response.status_code != 200:
            return Response({"error": "Book not found or unavailable."}, status=status.HTTP_400_BAD_REQUEST)

        # Step 2: Borrow the book and add it to the Borrowed Books table
        borrowed_book = BorrowedBook.objects.create(book_id=book_id, user=user)

        # Step 3: Optionally, mark the book as borrowed or remove it from the catalog
        catalog_update_response = requests.patch(
            f"{CATALOG_SERVICE_URL}{book_id}/", 
            data={"status": "borrowed"},
            headers={'Authorization': f'Bearer {request.headers.get("Authorization").split(" ")[1]}'}
        )

        if catalog_update_response.status_code != 200:
            return Response({"error": "Failed to update catalog."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({
            "message": f"Book {book_id} borrowed successfully."
        }, status=status.HTTP_201_CREATED)
