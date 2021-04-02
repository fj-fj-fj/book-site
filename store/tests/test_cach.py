from django.contrib.auth.models import User
from django.test import TestCase

from store.cach import set_rating
from store.models import Book, UserBookRelation


class CachTestCase(TestCase):
    def setUp(self):
        user1 = User.objects.create(username='user1', first_name='Foo', last_name='Bar')
        user2 = User.objects.create(username='user2', first_name='1', last_name='2')
        user3 = User.objects.create(username='user3')

        self.book1 = Book.objects.create(name='test1', price=25, author='author 1', discount=3)

        UserBookRelation.objects.create(user=user1, book=self.book1, like=True, rate=5)
        UserBookRelation.objects.create(user=user2, book=self.book1, like=True, rate=5)
        UserBookRelation.objects.create(user=user3, book=self.book1, like=True, rate=4)

    def test_ok(self):
        set_rating(self.book1)
        # функция не возвращает обновленную книгу, поэтому refresh
        self.book1.refresh_from_db()
        self.assertEqual('4.67', str(self.book1.rating))
