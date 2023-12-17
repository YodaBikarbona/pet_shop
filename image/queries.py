from image.models import Image


def get_image_by_id(_id: int) -> Image | None:
    return Image.objects.filter(id=_id).first()
