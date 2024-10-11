from motor.motor_asyncio import AsyncIOMotorDatabase

from api.users.schemas.inputs import ProductInput, PatchProductInput
from models.products import ProductsModel
from repositories.products import ProductsRepository


class ProductsService:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self.products_repository = ProductsRepository(self.db)

    async def create_product(self, product_input: ProductInput):
        print('Creating product in service')
        product_created = await self.products_repository.create_product(product_input.model_dump())
        if product_created is None:
            raise ValueError("Product not created")
        print(f'Product created in service: {product_created}')
        return product_created

    async def get_product_by_name(self, product_name: str) -> ProductsModel:
        print('Getting product by name in service')
        product_found = await self.products_repository.get_product_by_name(product_name)
        if product_found is None:
            raise ValueError("Product not found")
        print(f'Product found by name in service: {product_found}')
        return product_found

    async def get_product_by_code(self, code: int) -> ProductsModel:
        print('Getting product by code in service')
        product_found = await self.products_repository.get_product_by_code(code)
        if product_found is None:
            raise ValueError("Product not found")
        print(f'Product found by code in service: {product_found}')
        return product_found

    async def get_all_products(self) -> list[ProductsModel]:
        print('Getting all products in service')
        all_products = await self.products_repository.get_all_products()
        print(f'All products in service: {all_products}')
        return all_products

    async def update_product(self, product_code: int, update_data: PatchProductInput) -> ProductsModel:
        print('Updating some product data by code in service')
        product_updated = await self.products_repository.update_product(product_code, update_data.model_dump())
        if product_updated is None:
            raise ValueError("Product not updated")
        print(f'Product updated some data by code in service: {product_updated}')
        return product_updated

    async def update_all_product(self, product_code: int, product_data: ProductInput) -> ProductsModel:
        print('Updating all product by code in service')
        product = await self.get_product_by_code(product_code)
        if product is None:
            raise ValueError("Product not found")
        product.product_code = product_data.product_code
        product.product_name = product_data.product_name
        product.product_category = product_data.product_category
        product.product_brand = product_data.product_brand
        product.product_unit_presentation = product_data.product_unit_presentation
        product.product_quantity_presentation = product_data.product_quantity_presentation
        product.product_price = product_data.product_price
        product.supplier_name = product_data.supplier_name
        product_all_updated = await self.products_repository.update_all_product(product_code, product.model_dump())
        if product_all_updated is None:
            raise ValueError("Product not updated")
        print(f'Product all updated by code in service: {product_all_updated}')
        return product_all_updated

    async def deactivate_product(self, product_code: int):
        print('Deactivating product by code in service')
        product_by_deactivate = await self.products_repository.get_product_by_code(product_code)
        if product_by_deactivate is None:
            raise ValueError("Product not found")
        product_by_deactivate.is_deleted = True
        product_disabled = await self.products_repository.deactivate_product(product_code,
                                                                             product_by_deactivate.model_dump())
        if product_disabled is None:
            raise ValueError("Product not disabled")
        print(f'Product disabled by code in service: {product_disabled}')
        return product_disabled

    async def delete_product(self, product_code: int):
        print('Deleting product by code in service')
        product_deleted = await self.products_repository.delete_product(product_code)
        if product_deleted is None:
            raise ValueError("Product not deleted")
        print(f'Product deleted by code in service: {product_deleted}')
        return product_deleted
