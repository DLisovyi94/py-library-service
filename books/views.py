from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAdminUser

from books.models import Book
from books.serializers import (BookSerializer,
                               BookListSerializer,
                               BookDetailSerializer)


@extend_schema_view(
    list=extend_schema(description="List all books"),
    retrieve=extend_schema(description="Retrieve book details"),
    create=extend_schema(description="Create a new book"),
    update=extend_schema(description="Update book info"),
    partial_update=extend_schema(description="Partially update book info"),
    destroy=extend_schema(description="Delete a book"),
)
class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return BookListSerializer
        if self.action == "retrieve":
            return BookDetailSerializer
        return BookSerializer

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [AllowAny()]
        return [IsAdminUser()]

# Create your views here.
