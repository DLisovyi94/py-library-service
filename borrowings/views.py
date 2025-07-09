from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.utils.timezone import now

from borrowings.models import Borrowing
from borrowings.serializers import BorrowingListSerializer, BorrowingCreateSerializer
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from borrowings.filters import BorrowingFilter


@extend_schema_view(
    list=extend_schema(description="Get borrowings (admin sees all, user sees own)"),
    retrieve=extend_schema(description="Get details of a specific borrowing"),
    create=extend_schema(description="Create new borrowing. Decreases book inventory."),
)
class BorrowingViewSet(viewsets.ModelViewSet):
    queryset = Borrowing.objects.select_related("book", "user")
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = BorrowingFilter
    ordering_fields = ["borrow_date", "expected_return_date"]

    def get_serializer_class(self):
        if self.action == "create":
            return BorrowingCreateSerializer
        return BorrowingListSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = self.queryset

        if not user.is_staff:
            queryset = queryset.filter(user=user)
        elif user.is_staff and "user_id" in self.request.query_params:
            queryset = queryset.filter(
                user__id=self.request.query_params["user_id"]
            )

        return queryset

    @extend_schema(description="Mark a borrowing as returned. Increases book inventory.")
    @action(methods=["post"], detail=True)
    def return_book(self, request, pk=None):
        borrowing = self.get_object()

        if borrowing.actual_return_date:
            return Response({"detail": "Book already returned."}, status=400)

        borrowing.actual_return_date = now().date()
        borrowing.book.inventory += 1
        borrowing.book.save()
        borrowing.save()

        return Response({"detail": "Book successfully returned."}, status=status.HTTP_200_OK)
