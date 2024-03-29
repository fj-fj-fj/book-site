from django.db.models import Case, Count, F, When
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.mixins import UpdateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from store.models import Book, UserBookRelation
from store.permissions import IsOwnerOrStaffOrReadOnly
from store.serializers import BooksSerializer, UserBookRelationSerializer


class BookViewSet(ModelViewSet):
    queryset = (Book.objects.all().annotate(
        annotated_likes=Count(Case(When(userbookrelation__like=True, then=1))),
        discount_price=F('price') - F('discount'),
    ).select_related('owner')
     .prefetch_related('readers')
     .order_by('id')
    )

    serializer_class = BooksSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    permission_classes = [IsOwnerOrStaffOrReadOnly]
    filter_fields = ['price', 'discount']
    search_fields = ['name', 'author']
    ordering_fields = ['price', 'author']

    def perform_create(self, serializer) -> None:
        serializer.validated_data['owner'] = self.request.user
        serializer.save()


class UserBookRelationView(UpdateModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticated]
    queryset = UserBookRelation.objects.all()
    serializer_class = UserBookRelationSerializer
    lookup_field = 'book'

    def get_object(self) -> UserBookRelation:
        obj, _ = UserBookRelation.objects.get_or_create(
            user=self.request.user,
            book_id=self.kwargs['book'],
        )
        return obj


def auth(request: HttpRequest) -> HttpResponse:
    return render(request, 'oauth.html')
