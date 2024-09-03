import json

from flask import Blueprint, request, make_response, url_for, render_template

from src.services.images.image import ImageService, image_sizes

images = Blueprint("images", __name__, url_prefix="/images")
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@images.route("/upload", methods=["POST"])
def upload():
    if 'file' not in request.files:
        raise make_response("No file part", 400)
    file = request.files['file']
    if file.filename == '':
        raise make_response("No file part", 400)
    if file and allowed_file(file.filename):
        # filename = secure_filename(file.filename)
        ImageService("static/breeds").upload(file, request.form.get("sub_id"), request.form.get("breed_ids", "").split(","))

    return make_response("File uploaded", 201)


@images.route("/<image_id>", methods=["DELETE"])
def delete_image(image_id):
    ImageService("static/breeds").delete(image_id)
    return make_response("File deleted", 204)


@images.route("/search", methods=["GET"])
def search():
    size = request.args.get("size", "med")
    mime_types = request.args.get("mime_types", "jpg").lower().split(",")
    format = request.args.get("format", "json")
    has_breeds = request.args.get("has_breeds", True)
    order = request.args.get("order", "")
    page = int(request.args.get("page", 0))
    limit = int(request.args.get("limit", 1))
    paging = ImageService("static/breeds").search(
        size=size,
        mime_types=mime_types,
        format=format,
        has_breeds=has_breeds,
        order=order,
        page=page,
        limit=limit
    )

    return json.dumps(paging.to_dict()), 200


@images.route("/<image_url>", methods=["GET"])
def view_image(image_url):
    url = ImageService("static/breeds").view_image(image_url)
    return render_template("image.html", image=url_for('static', filename=f"breeds/{url}"))


@images.route("/", methods=["GET"])
def list_images():
    sub_id = "owner_user_id"  # owner id
    order = request.args.get("order", "")
    page = int(request.args.get("page", 0))
    limit = int(request.args.get("limit"))
    paging = ImageService("static/breeds").search(
        sub_id=sub_id,
        order=order,
        page=page,
        limit=limit
    )
    return json.dumps(paging.to_dict()), 200
