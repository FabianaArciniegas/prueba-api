from fastapi import APIRouter, Request, Response
from fastapi.params import Depends

from api.products.schemas.inputs import ProductInput, PatchProductInput
from api.products.services.products_services import ProductsService
from core.api_response import ApiResponse
from models.products import ProductsModel
from models.response_model import ResponseModel
from utils.response_handler import response_handler

products_router: APIRouter = APIRouter(prefix="/products")


@products_router.post(
    path="",
    tags=["products"],
    description="Create a new product",
)
@response_handler()
async def create_product(
        request: Request,
        response: Response,
        product_input: ProductInput,
        api_response: ApiResponse = Depends(ApiResponse)
) -> ResponseModel[ProductsModel]:
    api_response.logger.info('Creating product in controller')
    product_service = ProductsService(request.app.database, api_response)

    product_created = await product_service.create_product(product_input)
    api_response.logger.info(f'Product created in controller')
    return product_created


@products_router.get(
    path="/{product_id}",
    tags=["products"],
    description="Get a product by id",
)
@response_handler()
async def get_product_by_id(
        request: Request,
        response: Response,
        product_id: str,
        api_response: ApiResponse = Depends(ApiResponse)
) -> ResponseModel[ProductsModel]:
    api_response.logger.info('Getting product in controller')
    product_service = ProductsService(request.app.database, api_response)

    product_found = await product_service.get_product_by_id(product_id)
    api_response.logger.info(f'Product found in controller')
    return product_found


@products_router.get(
    path="/all/",
    tags=["products"],
    description="Get all products",
)
@response_handler()
async def get_all_products(
        request: Request,
        response: Response,
        api_response: ApiResponse = Depends(ApiResponse)
) -> ResponseModel[list[ProductsModel]]:
    api_response.logger.info('Getting all products in controller')
    product_service = ProductsService(request.app.database, api_response)

    all_products = await product_service.get_all_products()
    api_response.logger.info(f'All products found in controller')
    return all_products


@products_router.patch(
    path="/update/{product_id}",
    tags=["products"],
    description="Update some product data",
)
@response_handler()
async def update_product(
        request: Request,
        response: Response,
        product_id: str,
        update_data: PatchProductInput,
        api_response: ApiResponse = Depends(ApiResponse)
) -> ResponseModel[ProductsModel]:
    api_response.logger.info('Updating some product data in controller')
    product_service = ProductsService(request.app.database, api_response)

    product_updated = await product_service.update_product(product_id, update_data)
    api_response.logger.info(f'Product updated some data in controller')
    return product_updated


@products_router.put(
    path="/update-all/{product_id}",
    tags=["products"],
    description="Update all product",
)
@response_handler()
async def update_all_product(
        request: Request,
        response: Response,
        product_id: str,
        product_data: ProductInput,
        api_response: ApiResponse = Depends(ApiResponse)
) -> ResponseModel[ProductsModel]:
    api_response.logger.info('Updating all product in controller')
    product_service = ProductsService(request.app.database, api_response)

    product_all_updated = await product_service.update_all_product(product_id, product_data)
    api_response.logger.info(f'Product all updated in controller')
    return product_all_updated


@products_router.patch(
    path="/disable/{product_id}",
    tags=["products"],
    description="Disable product",
)
@response_handler()
async def disable_product(
        request: Request,
        response: Response,
        product_id: str,
        api_response: ApiResponse = Depends(ApiResponse)
) -> ResponseModel:
    api_response.logger.info('Disabling product in controller')
    product_service = ProductsService(request.app.database, api_response)

    await product_service.disable_product(product_id)
    api_response.logger.info(f'Product disabled in controller')
    return


@products_router.delete(
    path="/delete/{product_id}",
    tags=["products"],
    description="Delete product",
)
@response_handler()
async def delete_product(
        request: Request,
        response: Response,
        product_id: str,
        api_response: ApiResponse = Depends(ApiResponse)
) -> ResponseModel:
    api_response.logger.info('Deleting product in controller')
    product_service = ProductsService(request.app.database, api_response)

    await product_service.delete_product(product_id)
    api_response.logger.info(f'Product deleted in controller')
    return
