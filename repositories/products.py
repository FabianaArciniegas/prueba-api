from models.products import ProductsModel
from repositories.base_repository import BaseRepository


class ProductsRepository(BaseRepository[ProductsModel]):
    _entity_model = ProductsModel

    async def check_if_the_product_exists(self, product_code: int) -> None:
        product_found = await self.collection.find_one({"product_code": product_code})
        if product_found:
            raise ValueError('There is already a product with that product_code')
