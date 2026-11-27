from pathlib import Path

IMAGE_EXTENSIONS = {"jpg", "jpeg", "png", "webp"}
VIDEO_EXTENSIONS = {"mp4", "webm"}
ALLOWED_EXTENSIONS = IMAGE_EXTENSIONS | VIDEO_EXTENSIONS

IMAGE_MAX_BYTES = 8 * 1024 * 1024
VIDEO_MAX_BYTES = 30 * 1024 * 1024


def file_extension(filename):
    return Path(filename).suffix.lower().lstrip(".")


def media_kind_for_filename(filename):
    if file_extension(filename) in VIDEO_EXTENSIONS:
        return "video"
    return "image"


def product_image_upload_path(instance, filename):
    folder = "video" if media_kind_for_filename(filename) == "video" else "image"
    return f"products/{instance.product_variant.sku}/{folder}/{filename}"
