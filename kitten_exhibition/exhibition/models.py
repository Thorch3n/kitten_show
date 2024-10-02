from django.contrib.auth.models import User
from django.db import models


class Breed(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Kitten(models.Model):
    name = models.CharField(max_length=255)
    color = models.CharField(max_length=50)
    age_in_months = models.PositiveIntegerField()
    description = models.TextField()
    breed = models.ForeignKey(Breed, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.FloatField(default=0)  # Средняя оценка
    rating_count = models.PositiveIntegerField(default=0)  # Количество оценок

    def __str__(self):
        return self.name


def update_rating(self, new_rating):
    total_rating = self.rating * self.rating_count + new_rating
    self.rating_count += 1
    self.rating = total_rating / self.rating_count
    self.save()
