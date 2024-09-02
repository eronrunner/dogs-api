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

    def __init__(self, upload_path):
        self.number = 20
        self.upload_path = upload_path
        self.format = "JPEG"
        super().__init__()

    def upload(self, file: FileStorage, sub_id=None, bread_ids=None):
        _id = uuid.uuid4()
        file_path = f"{self.upload_path}/{str(_id.hex)}"
        img = Image.open(file.stream)
        img.save(f"{file_path}.{self.format}")

        print(img, file_path)
        instance = self.model(id=str(_id), sub_id=sub_id, width=img.width, height=img.height,
                              url=f"{str(_id.hex)}.{img.format}", original_file_name=file.filename, approved=1,
                              pending=0, breed_ids=bread_ids)
        instance.create()
        for breed_id in bread_ids:
            BreedModel.patch(breed_id, image=instance.to_dict())

    def search(self, size, mime_types, format, has_breeds, order, page, limit):
        print(page, limit)
        images = self.model.search(has_breeds, order, page, limit)
        print("IMAGES", images)
        return images

    def delete(self, image_id):
        instance = self.model.get(image_id, "default")
        for breed_id in instance.breed_ids or []:
            BreedModel.patch(breed_id, image={})
        instance.delete(image_id)
        if os.path.isfile(f"{self.upload_path}/{instance.url}"):
            os.remove(f"{self.upload_path}/{instance.url}")
        return instance
