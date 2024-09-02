import json

from flask import Blueprint, session
from flask.views import MethodView

from src.services.dog_breed.breed import BreedService

dogs = Blueprint("dog", __name__, url_prefix="/breeds")

dog_breed_service = BreedService()


@dogs.route("/", methods=["GET"])
def get_breeds():
    return dog_breed_service.list_all_breeds(), 200


@dogs.route("/<breed_id>", methods=["GET"])
def get_breed(breed_id: str):
    return dog_breed_service.get_breed(breed_id), 200