from models.base_models import DBModels


class ProductsModel(DBModels):
    _collection_name = 'products'
    product_code: int
    product_name: str
    product_category: str
    product_brand: str
    product_unit_presentation: str
    product_quantity_presentation: int
    product_price: float
    supplier_name: str
