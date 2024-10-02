import pytest
from django.urls import reverse
from rest_framework import status
from .models import Breed, Kitten
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.fixture
def user(db):
    return User.objects.create_user(username='testuser', password='password')

@pytest.fixture
def breed(db):
    return Breed.objects.create(name='Persian')

@pytest.fixture
def kitten(db, breed):
    return Kitten.objects.create(name='Fluffy', age=2, breed=breed)

@pytest.mark.django_db
def test_kitten_creation(client, user):
    client.login(username='testuser', password='password')
    response = client.post(reverse('kitten-list'), {'name': 'Mittens', 'age': 1, 'breed': 1})
    assert response.status_code == status.HTTP_201_CREATED
    assert Kitten.objects.count() == 1
    assert Kitten.objects.get().name == 'Mittens'

@pytest.mark.django_db
def test_kitten_list(client, user, kitten):
    client.login(username='testuser', password='password')
    response = client.get(reverse('kitten-list'))
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]['name'] == 'Fluffy'

@pytest.mark.django_db
def test_kitten_detail(client, user, kitten):
    client.login(username='testuser', password='password')
    response = client.get(reverse('kitten-detail', args=[kitten.id]))
    assert response.status_code == status.HTTP_200_OK
    assert response.data['name'] == 'Fluffy'

@pytest.mark.django_db
def test_kitten_update(client, user, kitten):
    client.login(username='testuser', password='password')
    response = client.put(reverse('kitten-detail', args=[kitten.id]), {'name': 'Updated Fluffy', 'age': 3, 'breed': kitten.breed.id})
    assert response.status_code == status.HTTP_200_OK
    kitten.refresh_from_db()
    assert kitten.name == 'Updated Fluffy'

@pytest.mark.django_db
def test_kitten_delete(client, user, kitten):
    client.login(username='testuser', password='password')
    response = client.delete(reverse('kitten-detail', args=[kitten.id]))
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Kitten.objects.count() == 0
