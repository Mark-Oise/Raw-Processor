import os
import tempfile
import rawpy
import imageio
import exifread
from PIL import Image
from io import BytesIO

from django.core.files.base import ContentFile
from celery import shared_task
from .models import RawAsset, AssetVariant, AssetStatus, VariantType


@shared_task
def process_raw_image(asset_id):
    # 1. Setup & Retrieval
    try:
        asset = RawAsset.objects.get(id=asset_id)
        asset.status = AssetStatus.PROCESSING
        asset.save()
    except RawAsset.DoesNotExist:
        return "Asset not found"

    temp_path = None

    try:
        # 2. Download from S3 to Temp File
        _, ext = os.path.splitext(asset.file.name)

        with tempfile.NamedTemporaryFile(suffix=ext, delete=False) as temp_file:
            asset.file.open('rb')
            temp_file.write(asset.file.read())
            temp_file.flush()
            temp_path = temp_file.name
            asset.file.close()

        # 3. Extract Metadata
        with open(temp_path, 'rb') as f:
            tags = exifread.process_file(f, details=False)

            asset.camera_make = str(tags.get('Image Make', 'Unknown'))
            asset.camera_model = str(tags.get('Image Model', 'Unknown'))
            asset.iso = str(tags.get('EXIF ISOSpeedRatings', 0))
            asset.shutter_speed = str(tags.get('EXIF ExposureTime', ''))

            if 'EXIF FNumber' in tags:
                f_val = tags['EXIF FNumber'].values[0]
                asset.aperture = f"f/{float(f_val.num) / float(f_val.den)}"

            asset.save()

        # 4. Image Processing (Full Resolution)
        with rawpy.imread(temp_path) as raw:
            rgb = raw.postprocess(use_camera_wb=True)

            # --- A. Generate Preview (Full Res) ---
            preview_buffer = BytesIO()
            imageio.imwrite(preview_buffer, rgb, format='jpg', quality=85)

            AssetVariant.objects.create(
                asset=asset,
                variant_type=VariantType.PREVIEW,
                file=ContentFile(preview_buffer.getvalue(), name=f"{asset.id}_preview.jpg")
            )

            # --- B. Generate Thumbnail (300px) ---
            pil_image = Image.fromarray(rgb)
            pil_image.thumbnail((300, 300))

            thumb_buffer = BytesIO()
            pil_image.save(thumb_buffer, format='JPEG', quality=80)

            AssetVariant.objects.create(
                asset=asset,
                variant_type=VariantType.THUMBNAIL,
                file=ContentFile(thumb_buffer.getvalue(), name=f"{asset.id}_thumb.jpg")
            )

        # 5. Success
        asset.status = AssetStatus.COMPLETED
        asset.save()
        return f"Success: {asset.id}"

    except Exception as e:
        print(f"FAILED processing {asset.id}: {e}")
        asset.status = AssetStatus.FAILED
        asset.save()
        return f"Failed: {e}"

    finally:
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)