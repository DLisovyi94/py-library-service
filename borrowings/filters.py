import django_filters
from borrowings.models import Borrowing

class BorrowingFilter(django_filters.FilterSet):
    is_active = django_filters.BooleanFilter(method="filter_is_active")

    class Meta:
        model = Borrowing
        fields = ["user", "is_active"]

    def filter_is_active(self, queryset, name, value):
        if value:
            return queryset.filter(actual_return_date__isnull=True)
        return queryset.filter(actual_return_date__isnull=False)
