import os
import uuid
from enum import Enum

from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename
from PIL import Image

from src.models.breeds.breed import BreedModel
from src.models.images.image import ImageModel
from src.services.abstract import Service


image_sizes = {
    "thumb": (100, 100),
    "small": (400, 400),
    "med": (800, 800),
    "full": (-1, -1)
}


class ImageService(Service):
    model = ImageModel
    per_page = 20

    def __init__(self, upload_path):
        super().__init__()
        self.upload_path = upload_path

    def upload(self, file: FileStorage, sub_id=None, bread_ids=None):
        _id = uuid.uuid4()
        file_path = f"{self.upload_path}"
        img = Image.open(file.stream)
        image_url = f"{_id.hex}-full.{img.format.lower()}"
        for size, dimensions in image_sizes.items():
            save_path = f"{file_path}/{_id.hex}-{size}.{img.format.lower()}"
            if dimensions[0] == -1:
                img.save(f"{save_path}")
            else:
                other = img.copy()
                other.thumbnail(dimensions)
                other.save(f"{save_path}")

        instance = self.model(id=str(_id), sub_id=sub_id, width=img.width, height=img.height,
                              url=image_url, original_file_name=file.filename, approved=1,
                              pending=0, breed_ids=bread_ids)
        instance.create()
        for breed_id in bread_ids:
            BreedModel.patch(breed_id, image=instance.to_dict())

    def search(self, **kwargs):
        size = kwargs.get("size", "med")
        mime_types = kwargs.get("mime_types", [])
        has_breeds = kwargs.get("has_breeds", True)
        order = kwargs.get("order", "")
        page = int(kwargs.get("page", 0))
        limit = int(kwargs.get("limit", self.per_page))
        sub_id = kwargs.get("sub_id", None)

        size = size.lower().strip()
        print(page, limit)
        pagination = self.model.search(
            sub_id=sub_id,
            mime_types=mime_types,
            has_breeds=has_breeds,
            order=order,
            page=page,
            limit=limit
        )
        for item in pagination.items:
            ext = item["url"].split(".")[-1]
            item["url"] = f"{item['id']}-{size}.{ext}"
        return pagination

    def delete(self, image_id):
        instance = self.model.get(image_id, "default")
        for breed_id in instance.breed_ids or []:
            BreedModel.patch(breed_id, image={})
        instance.delete(image_id)
        if os.path.isfile(f"{self.upload_path}/{instance.url}"):
            os.remove(f"{self.upload_path}/{instance.url}")
        return instance

    def view_image(self, image_url):
        if os.path.isfile(f"{self.upload_path}/{image_url}"):
            return image_url
        else:
            raise FileNotFoundError(f"Not found: {image_url}")