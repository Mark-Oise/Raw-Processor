import uuid
from django.db import models


class AssetStatus(models.TextChoices):
    PENDING = 'PENDING', 'Pending'
    PROCESSING = 'PROCESSING', 'Processing'
    COMPLETED = 'COMPLETED', 'Completed'
    FAILED = 'FAILED', 'Failed'


class VariantType(models.TextChoices):
    THUMBNAIL = 'THUMB', 'Thumbnail'
    PREVIEW = 'PREVIEW', 'Preview'
    WATERMARKED = 'WATERMARK', 'Watermarked'


class RawAsset(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    file = models.FileField(upload_to='raw/%Y/%m/%d/')
    status = models.CharField(
        max_length=20,
        choices=AssetStatus.choices,
        default=AssetStatus.PENDING,
        db_index=True
    )

    camera_make = models.CharField(max_length=50, blank=True, null=True)
    camera_model = models.CharField(max_length=50, blank=True, null=True)
    iso = models.IntegerField(blank=True, null=True)
    shutter_speed = models.CharField(max_length=30, blank=True, null=True)
    aperture = models.CharField(max_length=20, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.file.name} ({self.status})"


class AssetVariant(models.Model):
    asset = models.ForeignKey(RawAsset, related_name='variants', on_delete=models.CASCADE)
    variant_type = models.CharField(max_length=20, choices=VariantType.choices)
    file = models.ImageField(upload_to='variants/%Y/%m/%d/')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['asset', 'variant_type'], name='unique_variant_per_asset')
        ]

    def __str__(self):
        return f"{self.variant_type} - {self.asset.id}"