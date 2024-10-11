from fastapi import APIRouter, Request, Response, HTTPException

from api.users.schemas.inputs import ProductInput, PatchProductInput
from api.users.services.products_services import ProductsService
from models.products import ProductsModel

products_router: APIRouter = APIRouter(prefix="/products")


@products_router.post(
    path="",
    tags=["products"],
    description="Create a new product",
)
async def create_product(
        request: Request,
        response: Response,
        product_input: ProductInput
) -> ProductInput:
    print('Creating product in controller')
    product_service = ProductsService(request.app.database)
    try:
        product_created = await product_service.create_product(product_input)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    print(f'Product created in controller: {product_created}')
    return product_created


@products_router.get(
    path="/productname/{product_name}",
    tags=["products"],
    description="Get a product by name",
)
async def get_product_by_name(
        request: Request,
        response: Response,
        product_name: str
) -> ProductsModel:
    print('Getting product by name in controller')
    product_service = ProductsService(request.app.database)
    try:
        product_found = await product_service.get_product_by_name(product_name)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    print(f'Product found by name in controller: {product_found}')
    return product_found


@products_router.get(
    path="/code/{product_code}",
    tags=["products"],
    description="Get a product by code",
)
async def get_product_by_code(
        request: Request,
        response: Response,
        product_code: int
) -> ProductsModel:
    print('Getting product by code in controller')
    product_service = ProductsService(request.app.database)
    try:
        product_found = await product_service.get_product_by_code(product_code)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    print(f'Product found by code in controller: {product_found}')
    return product_found


@products_router.get(
    path="/all/",
    tags=["products"],
    description="Get all products",
)
async def get_all_products(
        request: Request,
        response: Response,
) -> list[ProductsModel]:
    print('Getting all products in controller')
    product_service = ProductsService(request.app.database)
    try:
        all_products = await product_service.get_all_products()
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    print(f'All products found in controller: {all_products}')
    return all_products


@products_router.patch(
    path="/update/{product_code}",
    tags=["products"],
    description="Update some product data by code",
)
async def update_product(
        request: Request,
        response: Response,
        product_code: int,
        update_data: PatchProductInput
) -> ProductsModel:
    print('Updating some product data by code in controller')
    product_service = ProductsService(request.app.database)
    try:
        product_updated = await product_service.update_product(product_code, update_data)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    print(f'Product updated some data by code in controller: {product_updated}')
    return product_updated


@products_router.put(
    path="/updateall/{product_code}",
    tags=["products"],
    description="Update all product by code",
)
async def update_all_product(
        request: Request,
        response: Response,
        product_code: int,
        update_all_product: ProductInput
) -> ProductsModel:
    print('Updating all product by code in controller')
    product_service = ProductsService(request.app.database)
    try:
        product_all_updated = await product_service.update_all_product(product_code, update_all_product)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    print(f'Product all updated by code in controller: {product_all_updated}')
    return product_all_updated


@products_router.patch(
    path="/isdeleted/{product_code}",
    tags=["products"],
    description="Deactivate product by code",
)
async def deactivate_product(
        request: Request,
        response: Response,
        product_code: int
) -> ProductsModel:
    print('Deactivating product by code in controller')
    product_service = ProductsService(request.app.database)
    try:
        product_disabled = await product_service.deactivate_product(product_code)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    print(f'Product disabled by code in controller: {product_disabled}')
    return product_disabled


@products_router.delete(
    path="/delete/{product_code}",
    tags=["products"],
    description="Delete product by code",
)
async def delete_product(
        request: Request,
        response: Response,
        product_code: int
) -> ProductsModel:
    print('Deleting product by code in controller')
    product_service = ProductsService(request.app.database)
    try:
        product_deleted = await product_service.delete_product(product_code)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    print(f'Product deleted by code in controller: {product_deleted}')
    return product_deleted
