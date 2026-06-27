import factory
from service.models import Product, Category


class ProductFactory(factory.Factory):
    """Creates fake products for tests."""

    class Meta:
        model = Product

    id = None
    name = factory.Faker("word")
    description = factory.Faker("sentence")
    price = factory.Faker("pyfloat", left_digits=2, right_digits=2, positive=True)
    available = factory.Faker("boolean")
    category = factory.Iterator(
        [
            Category.CLOTHS,
            Category.FOOD,
            Category.HOUSEWARES,
            Category.AUTOMOTIVE,
            Category.TOOLS,
        ]
    )
