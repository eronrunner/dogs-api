import json
import os
from os.path import isfile
from typing import List, Union

import jsonutils as js

from src.helpers.files import ls_all_files_in_directory
from src.models.abstract import GenericModel


class ImageModel(GenericModel):

    def __init__(self, **kwargs):
        super().__init__()
        self.id = kwargs.get("id")
        self.width = kwargs.get("width")
        self.height = kwargs.get("height")
        self.url = kwargs.get("url")
        self.sub_id = kwargs.get("sub_id")
        self.original_file_name = kwargs.get("original_file_name")
        self.pending = kwargs.get("pending")
        self.approved = kwargs.get("approved")
        self.breed_ids = kwargs.get("breed_ids")

    def to_dict(self):
        return {
            "id": self.id,
            "sub_id": self.sub_id,
            "width": self.width,
            "height": self.height,
            "url": self.url,
            "original_file_name": self.original_file_name,
            "pending": self.pending,
            "approved": self.approved,
            "breed_ids": self.breed_ids
        }

    @staticmethod
    def from_json(json_raw: str):
        data = json.loads(json_raw) if isinstance(json_raw, str) else json_raw
        return ImageModel(**data)

    @staticmethod
    def list(fmt="dict") -> List["ImageModel"]:
        images = []
        for directory, filename in ls_all_files_in_directory("db/image"):
            print(directory, filename)
            with open(f"db/image/{filename}") as file:
                data = json.loads(file.read())
                model = ImageModel(**data)
                if fmt == "dict":
                    images.append(model.to_dict())
                elif fmt == "json":
                    images.append(data)
                else:
                    images.append(model)
        return images

    @staticmethod
    def get(image_id: int, fmt="dict") -> Union["ImageModel", dict]:
        if isfile(f"db/image/images-{image_id}.json"):
            with open(f"db/image/images-{image_id}.json") as file:
                data = json.loads(file.read())
                model = ImageModel(**data)
                if fmt == "dict":
                    return model.to_dict()
                elif fmt == "json":
                    return data
                else:
                    return model
        else:
            raise FileNotFoundError(f"Not found: {image_id}")

    def create(self):
        with open(f"db/image/images-{self.id}.json", "w") as file:
            file.write(json.dumps(self.to_dict(), indent=2))
        return self

    @staticmethod
    def search(has_breeds: bool, order: str, page: int, limit: int):
        json_data = js.JSONObject(ImageModel.list())
        json_data = json_data.query(breed_ids__isnull=not has_breeds, include_parent_=True)
        if order.lower() == "asc":
            order = "id"
            json_data = json_data.order_by(order)
        elif order.lower() == "desc":
            order = "-id"
            json_data = json_data.order_by(order)
        data = list(json_data)
        return data[page * limit: (page + 1) * limit]

    @staticmethod
    def delete(image_id):
        if isfile(f"db/image/images-{image_id}.json"):
            os.remove(f"db/image/images-{image_id}.json")
        else:
            raise FileNotFoundError(f"Not found: {image_id}")
        return True
