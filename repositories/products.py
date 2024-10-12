from models.products import ProductsModel
from repositories.base_repository import BaseRepository


class ProductsRepository(BaseRepository[ProductsModel]):
    _entity_model = ProductsModel

    async def create_product(self, product_data: dict) -> ProductsModel:
        product_created = await self.create(product_data)
        return product_created

    async def get_product_by_name(self, product_name: str) -> ProductsModel:
        product_found = await self.get("product_name", product_name)
        return product_found

    async def get_product_by_code(self, product_code: int) -> ProductsModel:
        product_found = await self.get("product_code", product_code)
        return product_found

    async def get_all_products(self) -> list[ProductsModel]:
        all_products = await self.get_all("is_deleted", False)
        return all_products

    async def update_product(self, product_code: int, product_data: dict) -> ProductsModel:
        product_updated = await self.update("product_code", product_code, product_data)
        return product_updated

    async def update_all_product(self, product_code: int, product_data: dict) -> ProductsModel:
        product_updated = await self.update_all("product_code", product_code, product_data)
        return product_updated

    async def deactivate_product(self, product_code: int, product_data: dict) -> ProductsModel:
        product_deactivated = await self.deactivate("product_code", product_code, product_data)
        return product_deactivated

    async def delete_product(self, product_code: int):
        product_deleted = await self.delete("product_code", product_code)
        return product_deleted
