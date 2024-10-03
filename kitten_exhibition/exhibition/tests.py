import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
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
def kitten(db, breed, user):
    return Kitten.objects.create(name='Fluffy', age_in_months=2, breed=breed, user=user)


@pytest.fixture
def token(client, user):
    response = client.post(reverse('token_obtain_pair'), {'username': 'testuser', 'password': 'password'})
    return response.data['access']


@pytest.mark.django_db
def test_kitten_creation(user, breed):
    client = APIClient()
    response = client.post(reverse('token_obtain_pair'), {'username': 'testuser', 'password': 'password'})
    token = response.data['access']

    client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
    response = client.post(reverse('kitten-list'), {
        'name': 'Mittens',
        'age_in_months': 1,
        'breed': breed.id,
        'color': 'white',
        'description': 'A cute kitten.',
        'user': user.id
    })
    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
def test_kitten_list(user, kitten):
    client = APIClient()
    response = client.post(reverse('token_obtain_pair'), {'username': 'testuser', 'password': 'password'})
    token = response.data['access']

    client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
    response = client.get(reverse('kitten-list'))

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]['name'] == kitten.name


@pytest.mark.django_db
def test_kitten_detail(user, kitten):
    client = APIClient()
    response = client.post(reverse('token_obtain_pair'), {'username': 'testuser', 'password': 'password'})
    token = response.data['access']

    client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
    response = client.get(reverse('kitten-detail', args=[kitten.id]))

    assert response.status_code == status.HTTP_200_OK
    assert response.data['name'] == kitten.name


@pytest.mark.django_db
def test_kitten_update(user, kitten):
    client = APIClient()
    response = client.post(reverse('token_obtain_pair'), {'username': 'testuser', 'password': 'password'})
    token = response.data['access']

    client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
    response = client.put(reverse('kitten-detail', args=[kitten.id]), {
        'name': 'Updated Fluffy',
        'age_in_months': 3,
        'breed': kitten.breed.id,
        'color': 'black',
        'description': 'A black and fluffy kitten.',
        'user': user.id
    })

    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_kitten_delete(user, kitten):
    client = APIClient()
    response = client.post(reverse('token_obtain_pair'), {'username': 'testuser', 'password': 'password'})
    token = response.data['access']

    client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
    response = client.delete(reverse('kitten-detail', args=[kitten.id]))

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Kitten.objects.count() == 0
