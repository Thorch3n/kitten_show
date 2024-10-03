from django.contrib.auth.models import User
from django.db import models


class Breed(models.Model):
    class Meta:
        verbose_name_plural = 'Породы'
        verbose_name = 'Порода'

    name = models.CharField(
        max_length=255,
        verbose_name='Название породы',
    )

    def __str__(self):
        return self.name


class Kitten(models.Model):
    class Meta:
        verbose_name_plural = 'Котята'
        verbose_name = 'Котенок'
    name = models.CharField(
        max_length=255,
        verbose_name='Кличка котенка',
    )
    color = models.CharField(
        max_length=50,
        verbose_name='Цвет котенка',
    )
    age_in_months = models.PositiveIntegerField(verbose_name='Возраст котенка (полных месяцев)')
    description = models.TextField(verbose_name='Описание котенка')
    breed = models.ForeignKey(
        Breed,
        on_delete=models.CASCADE,
        verbose_name='Порода'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор'
    )
    rating = models.FloatField(
        default=0,
        verbose_name='Рейтинг',
    )
    rating_count = models.PositiveIntegerField(
        default=0,
        verbose_name='Общее количество голосов'
    )

    def __str__(self):
        return self.name

    def update_rating(self, new_rating):
        total_rating = self.rating * self.rating_count + new_rating
        self.rating_count += 1
        self.rating = total_rating / self.rating_count
        self.save()
