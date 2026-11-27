from cloudinary_storage.storage import MediaCloudinaryStorage
from django.utils.deconstruct import deconstructible


@deconstructible
class ProductMediaStorage(MediaCloudinaryStorage):
    """Image storage that uploads files under /video/ as Cloudinary videos.

    Older photos have no /video/ segment in the stored path, so they stay images.
    """

    def _get_resource_type(self, name):
        normalized = name.replace("\\", "/").strip("/")
        if "/video/" in f"/{normalized}/":
            return "video"
        return "image"
