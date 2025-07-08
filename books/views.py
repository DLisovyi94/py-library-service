from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAdminUser

from books.models import Book
from books.serializers import (BookSerializer,
                               BookListSerializer,
                               BookDetailSerializer)


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
