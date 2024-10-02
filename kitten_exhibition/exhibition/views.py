from rest_framework import viewsets, permissions, filters, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import Breed, Kitten
from .serializers import BreedSerializer, KittenSerializer
from .permissions import IsOwnerOrReadOnly

class BreedViewSet(viewsets.ModelViewSet):
    queryset = Breed.objects.all()
    serializer_class = BreedSerializer
    permission_classes = [permissions.AllowAny]


class KittenViewSet(viewsets.ModelViewSet):
    queryset = Kitten.objects.all()
    serializer_class = KittenSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['breed__name']  # Позволяет фильтровать по имени породы

    def perform_create(self, serializer):
        # Привязываем пользователя к котенку
        serializer.save(user=self.request.user)

    def get_queryset(self):
        # Если пользователь - администратор, возвращаем всех котят, иначе только его
        if self.request.user.is_superuser:
            return Kitten.objects.all()
        return Kitten.objects.filter(user=self.request.user)

    @action(detail=False, methods=['get'], permission_classes=[permissions.AllowAny])
    def by_breed(self, request):
        # Получение котят по id породы
        breed_id = request.query_params.get('breed_id')
        if breed_id:
            kittens = self.get_queryset().filter(breed_id=breed_id)
            serializer = self.get_serializer(kittens, many=True)
            return Response(serializer.data)
        return Response({"error": "breed_id is required"}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def rate_kitten(self, request, pk=None):
        # Оценка котенка
        kitten = self.get_object()
        rating_value = request.data.get('rating')

        # Проверяем валидность рейтинга
        if rating_value is None or not (1 <= int(rating_value) <= 5):
            return Response({'error': 'Rating must be between 1 and 5.'}, status=status.HTTP_400_BAD_REQUEST)

        # Обновляем рейтинг котенка
        kitten.update_rating(new_rating=int(rating_value))

        return Response({'message': f'Kitten {kitten.name} rated successfully with {rating_value}.', 'new_rating': kitten.rating}, status=status.HTTP_200_OK)