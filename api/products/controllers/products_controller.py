from fastapi import APIRouter, Request, Response, HTTPException

from api.products.schemas.inputs import ProductInput, PatchProductInput
from api.products.services.products_services import ProductsService
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
) -> ProductsModel:
    print('Creating product in controller')
    product_service = ProductsService(request.app.database)
    try:
        product_created = await product_service.create_product(product_input)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    print(f'Product created in controller')
    return product_created


@products_router.get(
    path="/{product_id}",
    tags=["products"],
    description="Get a product by id",
)
async def get_product_by_id(
        request: Request,
        response: Response,
        product_id: str
) -> ProductsModel:
    print('Getting product in controller')
    product_service = ProductsService(request.app.database)
    try:
        product_found = await product_service.get_product_by_id(product_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    print(f'Product found in controller')
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
    print(f'All products found in controller')
    return all_products


@products_router.patch(
    path="/update/{product_id}",
    tags=["products"],
    description="Update some product data",
)
async def update_product(
        request: Request,
        response: Response,
        product_id: str,
        update_data: PatchProductInput
) -> ProductsModel:
    print('Updating some product data in controller')
    product_service = ProductsService(request.app.database)
    try:
        product_updated = await product_service.update_product(product_id, update_data)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    print(f'Product updated some data in controller')
    return product_updated


@products_router.put(
    path="/updateall/{product_id}",
    tags=["products"],
    description="Update all product",
)
async def update_all_product(
        request: Request,
        response: Response,
        product_id: str,
        product_data: ProductInput
) -> ProductsModel:
    print('Updating all product in controller')
    product_service = ProductsService(request.app.database)
    try:
        product_all_updated = await product_service.update_all_product(product_id, product_data)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    print(f'Product all updated in controller')
    return product_all_updated


@products_router.patch(
    path="/disable/{product_id}",
    tags=["products"],
    description="Disable product",
)
async def disable_product(
        request: Request,
        response: Response,
        product_id: str
) -> ProductsModel:
    print('Disabling product in controller')
    product_service = ProductsService(request.app.database)
    try:
        product_disabled = await product_service.disable_product(product_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    print(f'Product disabled in controller')
    return product_disabled


@products_router.delete(
    path="/delete/{product_id}",
    tags=["products"],
    description="Delete product",
)
async def delete_product(
        request: Request,
        response: Response,
        product_id: str
) -> ProductsModel:
    print('Deleting product in controller')
    product_service = ProductsService(request.app.database)
    try:
        product_deleted = await product_service.delete_product(product_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    print(f'Product deleted in controller')
    return product_deleted
