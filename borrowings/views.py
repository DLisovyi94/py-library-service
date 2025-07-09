from rest_framework import viewsets, permissions
from borrowings.models import Borrowing
from borrowings.serializers import BorrowingListSerializer, BorrowingCreateSerializer
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from borrowings.filters import BorrowingFilter


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
