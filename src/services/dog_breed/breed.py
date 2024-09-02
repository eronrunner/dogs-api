from src.models.breeds.breed import BreedModel
from src.services.abstract import Service


class BreedService(Service):

    model = BreedModel

    def __init__(self):
        self.number = 10
        super().__init__()

    def list_all_breeds(self):
        breeds = self.model.list(1, self.number)
        return breeds

    def get_breed(self, breed_id: str):
        breed = self.model.get(breed_id)
        return breed

