from datetime import timedelta
from django.utils.timezone import now
from django.urls import reverse
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model

from books.models import Book
from borrowings.models import Borrowing

BORROWINGS_URL = reverse("borrowings:borrowing-list")


def detail_url(borrowing_id):
    return reverse("borrowings:borrowing-detail", args=[borrowing_id])


def return_url(borrowing_id):
    return reverse("borrowings:borrowing-return-book", args=[borrowing_id])


class BorrowingViewSetTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "user@test.com", "pass123"
        )
        self.admin = get_user_model().objects.create_user(
            "admin@test.com", "pass123", is_staff=True
        )
        self.book = Book.objects.create(
            title="Django Book",
            author="Author",
            cover="HARD",
            inventory=5,
            daily_fee=1.5
        )

    def authenticate(self, user):
        self.client.force_authenticate(user)

    def test_user_can_see_only_their_borrowings(self):
        self.authenticate(self.user)
        Borrowing.objects.create(
            user=self.user,
            book=self.book,
            expected_return_date=now().date() + timedelta(days=5)
        )
        Borrowing.objects.create(
            user=self.admin,
            book=self.book,
            expected_return_date=now().date() + timedelta(days=3)
        )

        res = self.client.get(BORROWINGS_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)

    def test_admin_can_see_all_borrowings(self):
        self.authenticate(self.admin)
        Borrowing.objects.create(user=self.user, book=self.book, expected_return_date=now().date() + timedelta(days=1))
        Borrowing.objects.create(user=self.admin, book=self.book, expected_return_date=now().date() + timedelta(days=2))

        res = self.client.get(BORROWINGS_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 2)

    def test_create_borrowing(self):
        self.authenticate(self.user)
        payload = {
            "book": self.book.id,
            "expected_return_date": (now().date() + timedelta(days=7))
        }
        res = self.client.post(BORROWINGS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.book.refresh_from_db()
        self.assertEqual(self.book.inventory, 4)

    def test_return_book_success(self):
        self.authenticate(self.user)
        borrowing = Borrowing.objects.create(
            user=self.user,
            book=self.book,
            expected_return_date=now().date() + timedelta(days=3)
        )
        url = return_url(borrowing.id)

        res = self.client.post(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        borrowing.refresh_from_db()
        self.assertIsNotNone(borrowing.actual_return_date)
        self.book.refresh_from_db()
        self.assertEqual(self.book.inventory, 6)

    def test_return_book_already_returned(self):
        self.authenticate(self.user)
        borrowing = Borrowing.objects.create(
            user=self.user,
            book=self.book,
            expected_return_date=now().date() + timedelta(days=3),
            actual_return_date=now().date()
        )
        url = return_url(borrowing.id)

        res = self.client.post(url)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("detail", res.data)
        self.assertEqual(res.data["detail"], "Book already returned.")
