from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from store.models import Book, UserBookRelation


class BookReaderSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name')


class BooksSerializer(ModelSerializer):
    # # к каждой книге вывести кол-во лайков
    # # 1й вариант: при помощи `likes_count` и `get_likes_count()` (доп. запрос в бд)
    # likes_count = serializers.SerializerMethodField()
    # 2й: аннотация (qweryset)
    annotated_likes = serializers.IntegerField(read_only=True)

    rating = serializers.DecimalField(max_digits=3, decimal_places=2, read_only=True)
    # discount_price = serializers.DecimalField(сука=decimal.InvalidOperation)
    discount_price = serializers.FloatField(read_only=True)
    # нужен `sourse`, поскольку `owner_name` есть только здесь
    owner_name = serializers.CharField(source='owner.username', default='', read_only=True)
    # в `source` необходимости нет, поле есть в `Book`
    readers = BookReaderSerializer(many=True, read_only=True)

    class Meta:
        model = Book
        fields = (
            'id', 'name', 'price', 'author',
            'annotated_likes', 'rating', 'discount',
            'discount_price', 'owner_name', 'readers'
        )

    # def get_likes_count(self, instance):
    #     return UserBookRelation.objects.filter(book=instance, like=True).count()


class UserBookRelationSerializer(ModelSerializer):
    class Meta:
        model = UserBookRelation
        fields = ('book', 'like', 'in_bookmarks', 'rate')
