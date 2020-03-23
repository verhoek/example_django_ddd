from rest_framework import serializers
from rest_framework.generics import CreateAPIView, UpdateAPIView

from app.models import RootEntity


class RootEntitySerializer(serializers.ModelSerializer):
    class Meta:
        model = RootEntity
        fields = '__all__'


class CreateRootEntityView(CreateAPIView):
    serializer_class = RootEntitySerializer

    queryset = RootEntity.objects.all()


class UpdateRootEntityView(UpdateAPIView):
    serializer_class = RootEntitySerializer

    queryset = RootEntity.objects.all()
