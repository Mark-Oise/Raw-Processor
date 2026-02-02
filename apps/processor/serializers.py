from rest_framework import serializers
from .models import RawAsset, AssetVariant
from .validators import validate_raw_extension


class RawUploadSerializer(serializers.ModelSerializer):
    file = serializers.FileField(validators=[validate_raw_extension])

    class Meta:
        model = RawAsset
        fields = ['id', 'file', 'status', 'created_at']
        read_only_fields = ['id', 'status', 'created_at']


class AssetVariantSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    class Meta:
        model = AssetVariant
        fields = ['variant_type', 'url']

    def get_url(self, obj):
        # This automatically generates the AWS S3 Pre-signed URL
        return obj.file.url


class AssetListSerializer(serializers.ModelSerializer):
    variants = AssetVariantSerializer(many=True, read_only=True)
    original_url = serializers.SerializerMethodField()

    class Meta:
        model = RawAsset
        fields = [
            'id', 'status', 'created_at',
            'camera_make', 'camera_model', 'iso', 'aperture', 'shutter_speed',
            'original_url', 'variants'
        ]

    def get_original_url(self, obj):
        return obj.file.url
