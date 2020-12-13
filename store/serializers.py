from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from store.models import Book, UserBookRelation


class BooksSerializer(ModelSerializer):
    # к каждой книге вывести кол-во лайков
    # 1й вариант: при помощи `likes_count` и `get_likes_count()` (доп. запрос в бд)
    likes_count = serializers.SerializerMethodField()
    # 2й: аннотация (qweryset)
    annotated_likes = serializers.IntegerField(read_only=True)
    rating = serializers.DecimalField(max_digits=3, decimal_places=2, read_only=True)
    # discount_price = serializers.DecimalField(max_digits=3, decimal_places=2, read_only=True)
    discount_price = serializers.FloatField(read_only=True)

    class Meta:
        model = Book
        fields = (
            'id', 'name', 'price', 'author', 'likes_count',
            'annotated_likes', 'rating', 'discount', 'discount_price'
        )

    def get_likes_count(self, instance):
        return UserBookRelation.objects.filter(book=instance, like=True).count()


class UserBookRelationSerializer(ModelSerializer):
    class Meta:
        model = UserBookRelation
        fields = ('book', 'like', 'in_bookmarks', 'rate')
