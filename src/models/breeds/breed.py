import json
import os.path
from os.path import isfile
from typing import List, Union

from src.helpers.files import ls_all_files_in_directory


class WeightModel:

    def __init__(self, **kwargs):
        self.imperial = kwargs.get("imperial")
        self.metric = kwargs.get("metric")

    def to_dict(self):
        return {
            "imperial": self.imperial,
            "metric": self.metric
        }

    @staticmethod
    def from_json(json_raw: str):
        data = json.loads(json_raw)
        return WeightModel(**data)


class ImageModel:

    def __init__(self, **kwargs):
        self.id = kwargs.get("id")
        self.width = kwargs.get("width")
        self.height = kwargs.get("height")
        self.url = kwargs.get("url")

    def to_dict(self):
        return {
            "id": self.id,
            "width": self.width,
            "height": self.height,
            "url": self.url
        }

    @staticmethod
    def from_json(json_raw: str):
        data = json.loads(json_raw) if isinstance(json_raw, str) else json_raw
        return ImageModel(**data)


class BreedModel:

    def __init__(self, **kwargs):
        self.id = kwargs.get("id")
        self.name = kwargs.get("name")
        self.cfa_url = kwargs.get("cfa_url")
        self.vetstreet_url = kwargs.get("vetstreet_url")
        self.vcahospitals_url = kwargs.get("vcahospitals_url")
        self.temperament = kwargs.get("temperament")
        self.origin = kwargs.get("origin")
        self.country_codes = kwargs.get("country_codes")
        self.country_code = kwargs.get("country_code")
        self.description = kwargs.get("description")
        self.life_span = kwargs.get("life_span")
        self.indoor = kwargs.get("indoor")
        self.lap = kwargs.get("lap")
        self.alt_names = kwargs.get("alt_names")
        self.adaptability = kwargs.get("adaptability")
        self.affection_level = kwargs.get("affection_level")
        self.child_friendly = kwargs.get("child_friendly")
        self.dog_friendly = kwargs.get("dog_friendly")
        self.energy_level = kwargs.get("energy_level")
        self.grooming = kwargs.get("grooming")
        self.health_issues = kwargs.get("health_issues")
        self.intelligence = kwargs.get("intelligence")
        self.shedding_level = kwargs.get("shedding_level")
        self.social_needs = kwargs.get("social_needs")
        self.stranger_friendly = kwargs.get("stranger_friendly")
        self.vocalisation = kwargs.get("vocalisation")
        self.experimental = kwargs.get("experimental")
        self.hairless = kwargs.get("hairless")
        self.natural = kwargs.get("natural")
        self.rare = kwargs.get("rare")
        self.rex = kwargs.get("rex")
        self.suppressed_tail = kwargs.get("suppressed_tail")
        self.short_legs = kwargs.get("short_legs")
        self.wikipedia_url = kwargs.get("wikipedia_url")
        self.hypoallergenic = kwargs.get("hypoallergenic")
        self.reference_image_id = kwargs.get("reference_image_id")
        self.image: ImageModel = ImageModel(**kwargs.get("image", {}))
        self.weight: WeightModel = WeightModel(**kwargs.get("weight", {}))

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "cfa_url": self.cfa_url,
            "vetstreet_url": self.vetstreet_url,
            "vcahospitals_url": self.vcahospitals_url,
            "temperament": self.temperament,
            "origin": self.origin,
            "country_codes": self.country_codes,
            "country_code": self.country_code,
            "description": self.description,
            "life_span": self.life_span,
            "indoor": self.indoor,
            "lap": self.lap,
            "alt_names": self.alt_names,
            "adaptability": self.adaptability,
            "affection_level": self.affection_level,
            "child_friendly": self.child_friendly,
            "dog_friendly": self.dog_friendly,
            "energy_level": self.energy_level,
            "grooming": self.grooming,
            "health_issues": self.health_issues,
            "intelligence": self.intelligence,
            "shedding_level": self.shedding_level,
            "social_needs": self.social_needs,
            "stranger_friendly": self.stranger_friendly,
            "vocalisation": self.vocalisation,
            "experimental": self.experimental,
            "hairless": self.hairless,
            "natural": self.natural,
            "rare": self.rare,
            "rex": self.rex,
            "suppressed_tail": self.suppressed_tail,
            "short_legs": self.short_legs,
            "wikipedia_url": self.wikipedia_url,
            "hypoallergenic": self.hypoallergenic,
            "reference_image_id": self.reference_image_id,
            "image": self.image.to_dict() if self.image else None,
            "weight": self.weight.to_dict() if self.weight else None
        }

    @staticmethod
    def from_json(json_raw: str):
        data = json.loads(json_raw) if isinstance(json_raw, str) else json_raw
        return BreedModel(**data)

    @staticmethod
    def list(fmt="dict") -> List["BreedModel"]:
        breeds = []
        for directory, filename in ls_all_files_in_directory("db/breed"):
            print(directory, filename)
            with open(f"db/breed/{filename}") as file:
                data = json.loads(file.read())
                model = BreedModel(**data)
                if fmt == "dict":
                    breeds.append(model.to_dict())
                elif fmt == "json":
                    breeds.append(data)
                else:
                    breeds.append(model)
        return breeds

    @staticmethod
    def get(breed_id, fmt="dict") -> Union["BreedModel", dict]:
        with open(f"db/breed/breeds-{breed_id}.json") as file:
            data = json.loads(file.read())
            model = BreedModel(**data)
            if fmt == "dict":
                return model.to_dict()
            elif fmt == "json":
                return data
            else:
                return model

    def create(self):
        with open(f"db/breed/breeds-{self.id}.json", "w") as file:
            file.write(json.dumps(self.to_dict()))
        return self.to_dict()

    @staticmethod
    def patch(breed_id: str, **kwargs):
        print(breed_id)
        if isfile(f"db/breed/breeds-{breed_id}.json"):
            with open(f"db/breed/breeds-{breed_id}.json", "r") as file:
                data = json.loads(file.read())
            with open(f"db/breed/breeds-{breed_id}.json", "w") as file:
                data.update(kwargs)
                file.write(json.dumps(BreedModel(**data).to_dict(), indent=2))
        else:
            raise FileNotFoundError(f"Not found: {breed_id}")
        return True

    @staticmethod
    def delete(breed_id):
        if os.path.isfile(f"db/breed/breeds-{breed_id}.json"):
            os.remove(f"db/breed/breeds-{breed_id}.json")
            return True
        else:
            raise FileNotFoundError(f"Not found: {breed_id}")
