from behave import given
from service.models import db, Product


@given("the following products")
def step_impl(context):
    """Load background product data before each scenario."""
    db.session.query(Product).delete()
    db.session.commit()

    for row in context.table:
        product = Product()
        product.deserialize(
            {
                "name": row["name"],
                "description": row["description"],
                "price": float(row["price"]),
                "available": row["available"].lower() == "true",
                "category": row["category"],
            }
        )
        product.create()
