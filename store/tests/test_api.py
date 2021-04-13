import json

from django.contrib.auth.models import User
from django.db import connection
from django.db.models import Avg, Case, Count, F, When
from django.test.utils import CaptureQueriesContext
from django.urls import reverse
from rest_framework import status
from rest_framework.exceptions import ErrorDetail
from rest_framework.test import APITestCase

from store.models import Book, UserBookRelation
from store.serializers import BooksSerializer


class BooksApiTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username='test_username')
        self.book1 = Book.objects.create(name='test1', price=25, author='author 1', owner=self.user)
        self.book2 = Book.objects.create(name='test2', price=55, author='author 2', discount=5)
        self.book3 = Book.objects.create(name='test3 author 2', price=25, author='author 3', owner=self.user)

        UserBookRelation.objects.create(user=self.user, book=self.book1, like=True, rate=5)

    def test_get(self):
        url = reverse('book-list')

        # test `select_related` and `prefetch_related`
        with CaptureQueriesContext(connection) as queries:
            response = self.client.get(url)

            # without `prefetch_related` or 'select_related` 2 != 4
            # without `prefetch_related` and 'select_related` 2 != 6
            # with `prefetch_related` and 'select_related`:
            self.assertEqual(2, len(queries))

        books = Book.objects.all().annotate(
            annotated_likes=Count(Case(When(userbookrelation__like=True, then=1))),
            # rating=Avg('userbookrelation__rate'),
            discount_price=F('price') - F('discount'),
        ).order_by('id')
        serializer_data = BooksSerializer(books, many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)
        book1, = [book for book in serializer_data if book.get('name') == 'test1']
        self.assertEqual(book1['rating'], '5.00')
        self.assertEqual(book1['annotated_likes'], 1)

    def test_get_filter(self):
        url = reverse('book-list')
        response = self.client.get(url, data={'price': 25})
        books = Book.objects.filter(id__in=[self.book1.id, self.book3.id]).annotate(
            annotated_likes=Count(Case(When(userbookrelation__like=True, then=1))),
            # rating=Avg('userbookrelation__rate'),
            discount_price=F('price') - F('discount')
        )
        serializer_data = BooksSerializer(books, many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_get_search(self):
        url = reverse('book-list')
        response = self.client.get(url, data={'search': 'author 2'})
        books = Book.objects.filter(id__in=[self.book2.id, self.book3.id]).annotate(
            annotated_likes=Count(Case(When(userbookrelation__like=True, then=1))),
            # rating=Avg('userbookrelation__rate'),
            discount_price=F('price') - F('discount')
        )
        serializer_data = BooksSerializer(books, many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_get_ordering(self):
        url = reverse('book-list')
        response = self.client.get(url, data={'ordering': '-price'})
        books = Book.objects.filter(id__in=[self.book2.id, self.book1.id, self.book3.id]).annotate(
            annotated_likes=Count(Case(When(userbookrelation__like=True, then=1))),
            # rating=Avg('userbookrelation__rate'),
            discount_price=F('price') - F('discount')
        )
        serializer_data = BooksSerializer(books, many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_create(self):
        self.assertEqual(3, Book.objects.all().count())
        url = reverse('book-list')
        data = {
            'name': 'a bite or py',
            'price': '200.2',
            'author': 'au au'
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user)
        response = self.client.post(url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(4, Book.objects.all().count())
        self.assertEqual(self.user, Book.objects.last().owner)

    def test_update(self):
        url = reverse('book-detail', args=(self.book1.id,))
        data = {
            'name': self.book1.name,
            'price': 666,
            'author': self.book1.author
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user)
        response = self.client.put(url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)

        # self.assertEqual(666, self.book1.price)
        # AssertionError: 666 != 25  # wtf
        # self.book1 = Book.objects.get(id=self.book1.id)  # or
        self.book1.refresh_from_db()
        self.assertEqual(666, self.book1.price)  # OK

    def test_update_not_owner(self):
        self.user2 = User.objects.create(username='test_username2')
        url = reverse('book-detail', args=(self.book1.id,))
        data = {
            'name': self.book1.name,
            'price': 666,
            'author': self.book1.author
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user2)
        response = self.client.put(url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        self.book1.refresh_from_db()
        self.assertEqual(25, self.book1.price)
        self.assertEqual({'detail': ErrorDetail(string='You do not have permission to perform this action.',
                                                code='permission_denied')}, response.data)

    def test_update_not_owner_but_staff(self):
        self.user2 = User.objects.create(username='test_username2', is_staff=True)
        url = reverse('book-detail', args=(self.book1.id,))
        data = {
            'name': self.book1.name,
            'price': 777,
            'author': self.book1.author
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user2)
        response = self.client.put(url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.book1.refresh_from_db()
        self.assertEqual(777, self.book1.price)

    def test_delete(self):
        self.assertEqual(3, Book.objects.all().count())
        url = reverse('book-detail', args=(self.book3.id,))
        self.client.force_login(self.user)
        response = self.client.delete(url)
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        self.assertEqual(2, Book.objects.all().count())

    def test_delete_not_owner(self):
        self.user2 = User.objects.create(username='test_username2')
        self.assertEqual(3, Book.objects.all().count())
        url = reverse('book-detail', args=(self.book3.id,))
        self.client.force_login(self.user2)
        response = self.client.delete(url)
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        self.assertEqual(3, Book.objects.all().count())

    def test_delete_not_owner_but_staff(self):
        self.user2 = User.objects.create(username='test_username2', is_staff=True)
        self.assertEqual(3, Book.objects.all().count())
        url = reverse('book-detail', args=(self.book3.id,))
        self.client.force_login(self.user2)
        response = self.client.delete(url)
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        self.assertEqual(2, Book.objects.all().count())

    def test_filter_by_discount(self):
        url = reverse('book-list')
        response = self.client.get(url, data={'discount': '5.00'})
        books = Book.objects.filter(id__in=[self.book2.id]).annotate(
            annotated_likes=Count(Case(When(userbookrelation__like=True, then=1))),
            # rating=Avg('userbookrelation__rate'),
            discount_price=F('price') - F('discount')
        )
        serializer_data = BooksSerializer(books, many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_discount_price(self):
        pass


class BooksRelationTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username='test_username')
        self.user2 = User.objects.create(username='test_username2')
        self.book1 = Book.objects.create(name='test1', price=25, author='author 1')
        self.book2 = Book.objects.create(name='test2', price=55, author='author 2')

    def test_like(self):
        url = reverse('userbookrelation-detail', args=(self.book1.id,))
        data = {
            'like': True
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user)
        response = self.client.patch(url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        relation = UserBookRelation.objects.get(user=self.user, book=self.book1)
        self.assertTrue(relation.like)

    def test_rate(self):
        url = reverse('userbookrelation-detail', args=(self.book1.id,))
        data = {
            'rate': 3,
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user)
        response = self.client.patch(url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        relation = UserBookRelation.objects.get(user=self.user, book=self.book1)
        self.assertEqual(3, relation.rate)

    def test_rate_wrong(self):
        url = reverse('userbookrelation-detail', args=(self.book1.id,))
        data = {
            'rate': 6,
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user)
        response = self.client.patch(url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code, response.data)
