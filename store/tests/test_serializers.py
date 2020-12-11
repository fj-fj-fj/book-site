from django.test import TestCase

from store.models import Book
from store.serializers import BooksSerializer


class BookSerializerTestCase(TestCase):
    def test_ok(self):
        book1 = Book.objects.create(name='test1', price=25, author='author 1')
        book2 = Book.objects.create(name='test2', price=55, author='author 2')
        data = BooksSerializer([book1, book2], many=True).data
        expected_data = [
            {
                'id': book1.id,
                'name': 'test1',
                'price': '25.00',
                'author': 'author 1',
                'owner': None,
                'readers': []
            },
            {
                'id': book2.id,
                'name': 'test2',
                'price': '55.00',
                'author': 'author 2',
                'owner': None,
                'readers': []
            }
        ]
        self.assertEqual(expected_data, data)