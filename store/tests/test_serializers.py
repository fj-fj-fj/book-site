from django.contrib.auth.models import User
from django.db.models import Avg, Case, Count, F, When
from django.test import TestCase

from store.models import Book, UserBookRelation
from store.serializers import BooksSerializer


class BookSerializerTestCase(TestCase):
    def test_ok(self):
        user1 = User.objects.create(username='user1', first_name='Foo', last_name='Bar')
        user2 = User.objects.create(username='user2', first_name='1', last_name='2')
        user3 = User.objects.create(username='user3')

        book1 = Book.objects.create(name='test1', price=25, author='author 1', discount=3)
        book2 = Book.objects.create(name='test2', price=55, author='author 2', owner=user1)

        UserBookRelation.objects.create(user=user1, book=book1, like=True, rate=5)
        UserBookRelation.objects.create(user=user2, book=book1, like=True, rate=5)
        UserBookRelation.objects.create(user=user3, book=book1, like=True, rate=4)

        UserBookRelation.objects.create(user=user1, book=book2, like=True, rate=4)
        user_book2 = UserBookRelation.objects.create(user=user2, book=book2, like=True)
        user_book2.rate = 3
        user_book2.save()
        UserBookRelation.objects.create(user=user3, book=book2, like=False)

        books = Book.objects.all().annotate(
            annotated_likes=Count(Case(When(userbookrelation__like=True, then=1))),
            # rating=Avg('userbookrelation__rate'),
            discount_price=F('price') - F('discount')
        ).order_by('id')
        data = BooksSerializer(books, many=True).data
        expected_data = [
            {
                'id': book1.id,
                'name': 'test1',
                'price': '25.00',
                'author': 'author 1',
                'annotated_likes': 3,
                'rating': '4.67',
                'discount': '3.00',
                'discount_price': 22.0,
                'owner_name': '',
                'readers': [
                    {
                        'first_name': 'Foo',
                        'last_name': 'Bar'
                    },
                    {
                        'first_name': '1',
                        'last_name': '2'
                    },
                    {
                        'first_name': '',
                        'last_name': ''
                    }
                ]
            },
            {
                'id': book2.id,
                'name': 'test2',
                'price': '55.00',
                'author': 'author 2',
                'annotated_likes': 2,
                'rating': '3.50',
                'discount': '0.00',
                'discount_price': 55.0,
                'owner_name': user1.__str__(),
                'readers': [
                    {
                        'first_name': 'Foo',
                        'last_name': 'Bar'
                    },
                    {
                        'first_name': '1',
                        'last_name': '2'
                    },
                    {
                        'first_name': '',
                        'last_name': ''
                    }
                ]
            }
        ]
        self.assertEqual(expected_data, data)


