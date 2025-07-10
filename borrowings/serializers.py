from rest_framework import serializers
from borrowings.models import Borrowing
from books.serializers import BookDetailSerializer


class BorrowingListSerializer(serializers.ModelSerializer):
    book = BookDetailSerializer(read_only=True)

    class Meta:
        model = Borrowing
        fields = (
            "id",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "book",
            "user",
        )


class BorrowingCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = ("expected_return_date", "book")

    def validate_book(self, book):
        if book.inventory < 1:
            raise serializers.ValidationError("This book is not available now.")
        return book

    def create(self, validated_data):
        book = validated_data["book"]
        book.inventory -= 1
        book.save()
        return Borrowing.objects.create(
            user=self.context["request"].user, **validated_data
        )
