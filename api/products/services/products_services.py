from datetime import datetime

from motor.motor_asyncio import AsyncIOMotorDatabase

from api.products.schemas.inputs import ProductInput, PatchProductInput
from core.api_response import ApiResponse

from models.products import ProductsModel
from repositories.products import ProductsRepository


class ProductsService:
    def __init__(self, db: AsyncIOMotorDatabase, api_response: ApiResponse):
        self.db = db
        self.api_response = api_response
        self.products_repository = ProductsRepository(self.db, self.api_response)

    async def create_product(self, product_input: ProductInput) -> ProductsModel:
        self.api_response.logger.info('Check product in db')
        await self.products_repository.check_if_the_product_exists(product_input.product_code)

        product_created = await self.products_repository.create(product_input.model_dump())
        self.api_response.logger.info(f'Product created in service')
        return product_created

    async def get_product_by_id(self, product_id: str) -> ProductsModel:
        self.api_response.logger.info('Getting product in db')
        product_found = await self.products_repository.get_by_id(product_id)
        self.api_response.logger.info(f'Product found in service')
        return product_found

    async def get_all_products(self) -> list[ProductsModel]:
        self.api_response.logger.info('Getting all products in db')
        all_products = await self.products_repository.get_all()
        self.api_response.logger.info(f'All products found in service')
        return all_products

    async def update_product(self, product_id: str, update_data: PatchProductInput) -> ProductsModel:
        self.api_response.logger.info('Getting product in db')
        await self.products_repository.get_by_id(product_id)
        await self.products_repository.check_if_the_product_exists(update_data.product_code)

        product_updated = await self.products_repository.update(product_id, update_data.model_dump())
        self.api_response.logger.info(f'Product updated data in service')
        return product_updated

    async def update_all_product(self, product_id: str, product_data: ProductInput) -> ProductsModel:
        self.api_response.logger.info('Getting product in db')
        await self.products_repository.check_if_the_product_exists(product_data.product_code)
        product = await self.products_repository.get_by_id(product_id)

        product.update_at = datetime.utcnow()
        product.product_code = product_data.product_code
        product.product_name = product_data.product_name
        product.product_category = product_data.product_category
        product.product_brand = product_data.product_brand
        product.product_unit_presentation = product_data.product_unit_presentation
        product.product_quantity_presentation = product_data.product_quantity_presentation
        product.product_price = product_data.product_price
        product.supplier_name = product_data.supplier_name
        product_all_updated = await self.products_repository.update_all(product_id, product.model_dump())
        print(f'Product all updated in service')
        return product_all_updated

    async def disable_product(self, product_id: str) -> None:
        self.api_response.logger.info('Getting product in db')
        product = await self.products_repository.get_by_id(product_id)
        product.is_deleted = True

        await self.products_repository.disable(product_id, product.model_dump())
        self.api_response.logger.info(f'Product disabled in service')

    async def delete_product(self, product_id: str) -> None:
        await self.products_repository.delete(product_id)
        self.api_response.logger.info(f'Product deleted in service')
