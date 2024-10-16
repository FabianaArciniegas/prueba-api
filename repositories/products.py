from core.api_response import ApiResponse
from core.errors import InvalidParameterError
from models.products import ProductsModel
from models.response_model import LocationError
from repositories.base_repository import BaseRepository


class ProductsRepository(BaseRepository[ProductsModel]):
    _entity_model = ProductsModel

    def __init__(self, db, api_response: ApiResponse):
        super().__init__(db, api_response)
        self.api_response = api_response

    async def check_if_the_product_exists(self, product_code: int) -> None:
        product_found = await self.collection.find_one({"product_code": product_code})
        if product_found:
            raise InvalidParameterError(message='There is already a product with that product_code',
                                        location=LocationError.Body)
