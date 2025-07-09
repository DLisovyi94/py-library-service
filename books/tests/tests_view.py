from django.urls import reverse
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model

from books.models import Book
from books.serializers import BookListSerializer, BookDetailSerializer

BOOKS_URL = reverse("book:book-list")


def detail_url(book_id):
    return reverse("book:book-detail", args=[book_id])


def sample_book(**params):
    defaults = {
        "title": "Test Book",
        "author": "Test Author",
        "cover": "HARD",
        "inventory": 5,
        "daily_fee": 2.5,
    }
    defaults.update(params)
    return Book.objects.create(**defaults)


class PublicBookApiTests(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_list_books_public(self):
        sample_book()
        sample_book(title="Another Book")

        res = self.client.get(BOOKS_URL)

        books = Book.objects.all()
        serializer = BookListSerializer(books, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_retrieve_book_public(self):
        book = sample_book()
        url = detail_url(book.id)
        res = self.client.get(url)

        serializer = BookDetailSerializer(book)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_book_unauthenticated(self):
        payload = {
            "title": "Forbidden Book",
            "author": "Author",
            "cover": "SOFT",
            "inventory": 1,
            "daily_fee": 1.0,
        }
        res = self.client.post(BOOKS_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AdminBookApiTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.admin_user = get_user_model().objects.create_user(
            email="admin@test.com",
            password="adminpass",
            is_staff=True,
        )
        self.client.force_authenticate(self.admin_user)

    def test_create_book_successful(self):
        payload = {
            "title": "New Book",
            "author": "Admin Author",
            "cover": "SOFT",
            "inventory": 10,
            "daily_fee": 3.0,
        }

        res = self.client.post(BOOKS_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        book = Book.objects.get(id=res.data["id"])
        for key in payload:
            self.assertEqual(getattr(book, key), payload[key])

    def test_update_book(self):
        book = sample_book()
        payload = {"title": "Updated Title"}
        url = detail_url(book.id)

        res = self.client.patch(url, payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        book.refresh_from_db()
        self.assertEqual(book.title, payload["title"])

    def test_delete_book(self):
        book = sample_book()
        url = detail_url(book.id)

        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Book.objects.filter(id=book.id).exists())
