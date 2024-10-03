from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter
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


@extend_schema_view(
    by_breed=extend_schema(
        request=None,
        parameters=[
            OpenApiParameter('breed_id', type=int, description="ID породы для фильтрации котят.", required=True)
        ],
        responses={200: KittenSerializer(many=True)},
        description="Получение котят по ID породы."
    )
)
class KittenViewSet(viewsets.ModelViewSet):
    queryset = Kitten.objects.all()
    serializer_class = KittenSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['breed__id']

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return Kitten.objects.all()

    @action(detail=False, methods=['get'], permission_classes=[permissions.AllowAny])
    def by_breed(self, request):
        breed_id = request.query_params.get('breed_id')
        if not breed_id:
            return Response({"error": "breed_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        kittens = self.get_queryset().filter(breed_id=breed_id)
        serializer = self.get_serializer(kittens, many=True)
        return Response(serializer.data)
