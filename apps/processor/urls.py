from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UploadViewSet

router = DefaultRouter()
# This creates the endpoint: POST /api/upload/
router.register(r'upload', UploadViewSet, basename='upload')

urlpatterns = [
    path('', include(router.urls)),
]