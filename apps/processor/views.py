from rest_framework import viewsets, parsers, status
from rest_framework.response import Response
from .models import RawAsset
from .serializers import RawUploadSerializer, AssetListSerializer
from .tasks import process_raw_image


class UploadViewSet(viewsets.ModelViewSet):
    queryset = RawAsset.objects.all().order_by('-created_at')
    parser_classes = [parsers.MultiPartParser, parsers.FormParser]
    http_method_names = ['get', 'post']

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return AssetListSerializer
        return RawUploadSerializer

    def perform_create(self, serializer):
        instance = serializer.save()
        process_raw_image.delay(instance.id)
