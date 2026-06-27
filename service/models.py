from enum import Enum
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class DataValidationError(Exception):
    """Used for data validation errors when deserializing a Product."""
    pass


class Category(Enum):
    UNKNOWN = 0
    CLOTHS = 1
    FOOD = 2
    HOUSEWARES = 3
    AUTOMOTIVE = 4
    TOOLS = 5


class Product(db.Model):
    """Product model for the product catalog."""

    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(63), nullable=False)
    description = db.Column(db.String(256), nullable=False)
    price = db.Column(db.Float, nullable=False)
    available = db.Column(db.Boolean(), nullable=False, default=True)
    category = db.Column(db.Enum(Category), nullable=False, default=Category.UNKNOWN)

    def create(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        if not self.id:
            raise DataValidationError("Update called with empty ID field")
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "price": self.price,
            "available": self.available,
            "category": self.category.name,
        }

    def deserialize(self, data):
        try:
            self.name = data["name"]
            self.description = data["description"]
            self.price = float(data["price"])
            self.available = bool(data["available"])
            category = data.get("category", "UNKNOWN")
            self.category = category if isinstance(category, Category) else Category[category]
        except KeyError as error:
            raise DataValidationError(f"Invalid product: missing {error.args[0]}")
        except (TypeError, ValueError) as error:
            raise DataValidationError(f"Invalid product: {error}")
        return self

    @classmethod
    def all(cls):
        return cls.query.all()

    @classmethod
    def find(cls, product_id):
        return db.session.get(cls, product_id)

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter(cls.name == name)

    @classmethod
    def find_by_category(cls, category):
        if isinstance(category, str):
            category = Category[category]
        return cls.query.filter(cls.category == category)

    @classmethod
    def find_by_availability(cls, available=True):
        return cls.query.filter(cls.available == available)
