import os
from flask import Flask, jsonify, request, abort, url_for
from service.models import db, Product, DataValidationError

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URI", "sqlite:///products.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)


def init_db():
    with app.app_context():
        db.create_all()


@app.route("/health")
def health():
    return jsonify(status="OK"), 200


@app.route("/products", methods=["POST"])
def create_products():
    check_content_type("application/json")
    product = Product()
    product.deserialize(request.get_json())
    product.create()
    location_url = url_for("get_products", product_id=product.id, _external=True)
    return jsonify(product.serialize()), 201, {"Location": location_url}


@app.route("/products/<int:product_id>", methods=["GET"])
def get_products(product_id):
    product = Product.find(product_id)
    if not product:
        abort(404)
    return jsonify(product.serialize()), 200


@app.route("/products/<int:product_id>", methods=["PUT"])
def update_products(product_id):
    check_content_type("application/json")
    product = Product.find(product_id)
    if not product:
        abort(404)
    product.deserialize(request.get_json())
    product.id = product_id
    product.update()
    return jsonify(product.serialize()), 200


@app.route("/products/<int:product_id>", methods=["DELETE"])
def delete_products(product_id):
    product = Product.find(product_id)
    if product:
        product.delete()
    return "", 204


@app.route("/products", methods=["GET"])
def list_products():
    name = request.args.get("name")
    category = request.args.get("category")
    available = request.args.get("available")

    if name:
        products = Product.find_by_name(name)
    elif category:
        try:
            products = Product.find_by_category(category.upper())
        except KeyError:
            abort(400)
    elif available:
        products = Product.find_by_availability(str_to_bool(available))
    else:
        products = Product.all()

    results = [product.serialize() for product in products]
    return jsonify(results), 200


def str_to_bool(value):
    return value.lower() in ["true", "1", "yes", "y"]


def check_content_type(content_type):
    if request.headers.get("Content-Type") == content_type:
        return
    abort(415)


@app.errorhandler(DataValidationError)
def request_validation_error(error):
    return jsonify(error=str(error)), 400


if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=8080, debug=True)
