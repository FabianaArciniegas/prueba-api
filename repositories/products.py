from models.products import ProductsModel
from repositories.base_repository import BaseRepository


class ProductsRepository(BaseRepository[ProductsModel]):
    _entity_model = ProductsModel
