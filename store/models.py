from django.contrib.auth.models import User
from django.db import models


class Book(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    author = models.CharField(max_length=255)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'Id {self.id}: {self.name}'


    # NOTE: сделать is_published, черновик (разные состояния книги),
    # чтобы можно было ее редактировать и снимать с публикации