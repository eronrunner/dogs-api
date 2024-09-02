import json

from src.helpers.files import path_to_file
from src.models.breeds.breed import BreedModel


def seed_breeds():
    with open("./breeds.json", "r") as file:
        data = json.loads(file.read())
    for breed in data:
        model = BreedModel(**breed)
        with open(path_to_file(f"db/breed/breeds-{model.id}.json"), "w+") as file:
            file.write(json.dumps(model.to_dict(), indent=2))


if __name__ == "__main__":
    seed_breeds()
