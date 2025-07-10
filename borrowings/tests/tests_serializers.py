from django.test import TestCase
from django.contrib.auth import get_user_model
from datetime import date, timedelta

from books.models import Book
from borrowings.models import Borrowing
from borrowings.serializers import BorrowingCreateSerializer, BorrowingListSerializer


class BorrowingSerializerTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email="test@example.com", password="testpass123"
        )
        self.book = Book.objects.create(
            title="Test Book",
            author="Author",
            cover="HARD",
            inventory=3,
            daily_fee=1.50,
        )

    def test_create_borrowing_valid_data(self):
        data = {
            "expected_return_date": date.today() + timedelta(days=5),
            "book": self.book.id,
        }
        serializer = BorrowingCreateSerializer(
            data=data, context={"request": self._mock_request(self.user)}
        )

        self.assertTrue(serializer.is_valid(), serializer.errors)
        borrowing = serializer.save()

        self.assertEqual(borrowing.book, self.book)
        self.assertEqual(borrowing.user, self.user)
        self.assertEqual(borrowing.book.inventory, 2)  # inventory decreased

    def test_create_borrowing_book_unavailable(self):
        self.book.inventory = 0
        self.book.save()
        data = {
            "expected_return_date": date.today() + timedelta(days=3),
            "book": self.book.id,
        }
        serializer = BorrowingCreateSerializer(
            data=data, context={"request": self._mock_request(self.user)}
        )

        self.assertFalse(serializer.is_valid())
        self.assertIn("book", serializer.errors)
        self.assertEqual(
            serializer.errors["book"][0], "This book is not available now."
        )

    def test_list_serializer_fields(self):
        borrowing = Borrowing.objects.create(
            user=self.user,
            book=self.book,
            expected_return_date=date.today() + timedelta(days=7),
        )
        serializer = BorrowingListSerializer(borrowing)
        data = serializer.data

        self.assertEqual(data["id"], borrowing.id)
        self.assertEqual(data["book"]["title"], self.book.title)
        self.assertEqual(data["user"], self.user.id)

    def _mock_request(self, user):
        class MockRequest:
            pass

        mock_request = MockRequest()
        mock_request.user = user
        return mock_request
