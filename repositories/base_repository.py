from datetime import datetime
from enum import Enum
from typing import TypeVar, Generic, Type

from motor.motor_asyncio import AsyncIOMotorDatabase, AsyncIOMotorCollection
from pydantic import BaseModel

DBModel = TypeVar('DBModel', bound=BaseModel)


class BaseRepository(Generic[DBModel]):
    _entity_model: Type[DBModel]

    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection: AsyncIOMotorCollection = db.get_collection(
            self._entity_model._collection_name.default)

    @staticmethod
    def convert_enum_values(data):
        if isinstance(data, dict):
            return {k: BaseRepository.convert_enum_values(v) for k, v in data.items()}
        elif isinstance(data, list):
            return [BaseRepository.convert_enum_values(item) for item in data]
        elif isinstance(data, Enum):
            return data.value
        else:
            return data

    async def create_user(self, user_data: dict, session=None) -> DBModel:
        print('Creating user in repository')
        user_created = self._entity_model.model_validate(user_data)
        if not user_created:
            return None
        data_parsed_enums = self.convert_enum_values(user_created.model_dump())
        data_parsed_enums["_id"] = data_parsed_enums.pop("id")
        await self.collection.insert_one(data_parsed_enums, session=session)
        print(f'User created in repository: {user_created}')
        return user_created

    async def get_user_by_username(self, username: str) -> DBModel:
        print('Getting user by username in repository')
        user_found = await self.collection.find_one({"username": username})
        if not user_found:
            return None
        print(f'User found by username in repository: {user_found}')
        return self._entity_model.model_validate(user_found)

    async def get_user_by_id(self, user_id: str) -> DBModel:
        print('Getting user by id in repository')
        user_found = await self.collection.find_one({"_id": user_id})
        if not user_found:
            return None
        print(f'User found by id in repository: {user_found}')
        return self._entity_model.model_validate(user_found)

    async def get_all_users(self) -> list[DBModel]:
        print('Getting all users in repository')
        users_found = self.collection.find({"is_deleted": False})
        users_list = await users_found.to_list(None)
        all_users = []
        for user in users_list:
            validated_user = self._entity_model.model_validate(user)
            all_users.append(validated_user)
        print(f'All users found in service: {all_users}')
        return all_users

    async def update_user(self, user_id: str, update_data: dict) -> DBModel:
        print('Updating some user data by id in repository')
        user_found = await self.collection.find_one({"_id": user_id})
        if not user_found:
            return None
        update_data_filtered = {k: v for k, v in update_data.items() if v is not None}
        await self.collection.update_one({"_id": user_id}, {"$set": update_data_filtered})
        user_updated = await self.collection.find_one({"_id": user_id})
        print(f'User updated some data by id in repository: {user_updated}')
        return self._entity_model.model_validate(user_updated)

    async def update_all_user(self, user_id: str, user_data: dict) -> DBModel:
        print('Updating all user by id in repository')
        user_found = await self.collection.find_one({"_id": user_id})
        if not user_found:
            return None
        validated_user = self._entity_model.model_validate(user_data)
        validated_user.id = user_found.get("_id")
        validated_user.create_at = user_found.get("create_at")
        validated_user.update_at = datetime.utcnow()
        await self.collection.replace_one({"_id": user_id}, validated_user.model_dump(by_alias=True))
        user_all_updated = await self.collection.find_one({"_id": user_id})
        print(f'User all updated by id in repository: {user_all_updated}')
        return self._entity_model.model_validate(user_all_updated)

    async def deactivate_user(self, user_id: str, user_data: dict) -> DBModel:
        print('Deactivating user by id in repository')
        user_by_update = await self.collection.update_one({"_id": user_id},
                                                          {"$set": {"is_deleted": user_data['is_deleted']}})
        if not user_by_update:
            return None
        user_deactivated = await self.collection.find_one({"_id": user_id})
        print(f'User deactivated by id in repository: {user_deactivated}')
        return self._entity_model.model_validate(user_deactivated)

    async def delete_user(self, user_id: str):
        print('Deleting user by id in repository')
        user_deleted = await self.collection.find_one_and_delete({"_id": user_id})
        if not user_deleted:
            return None
        print(f'User deleted by id in repository: {user_deleted}')
        return self._entity_model.model_validate(user_deleted)

    async def create_product(self, product_data: dict, session=None) -> DBModel:
        print('Creating product in repository')
        product_created = self._entity_model.model_validate(product_data)
        if not product_created:
            return None
        data_parsed_enums = self.convert_enum_values(product_created.model_dump())
        data_parsed_enums["_id"] = data_parsed_enums.pop("id")
        await self.collection.insert_one(data_parsed_enums, session=session)
        print(f'Product created in repository: {product_created}')
        return product_created

    async def get_product_by_name(self, product_name: str) -> DBModel:
        print('Getting product by name in repository')
        product_found = await self.collection.find_one({"product_name": product_name})
        if not product_found:
            return None
        print(f'Product found by name in repository: {product_found}')
        return self._entity_model.model_validate(product_found)

    async def get_product_by_code(self, code: int) -> DBModel:
        print('Getting product by code in repository')
        product_found = await self.collection.find_one({"product_code": code})
        if not product_found:
            return None
        print(f'Product found by code in repository: {product_found}')
        return self._entity_model.model_validate(product_found)

    async def get_all_products(self) -> list[DBModel]:
        print('Getting all products in repository')
        products_found = self.collection.find({"is_deleted": False})
        products_list = await products_found.to_list(None)
        all_products = []
        for product in products_list:
            validated_product = self._entity_model.model_validate(product)
            all_products.append(validated_product)
        print(f'All products found in service: {all_products}')
        return all_products

    async def update_product(self, product_code: int, update_data: dict) -> DBModel:
        print('Updating some product data by code in repository')
        product_found = await self.collection.find_one({"product_code": product_code})
        if not product_found:
            return None
        update_data_filtered = {k: v for k, v in update_data.items() if v is not None}
        await self.collection.update_one({"product_code": product_code}, {"$set": update_data_filtered})
        product_updated = await self.collection.find_one({"product_code": product_code})
        print(f'Product updated some data by code in repository: {product_updated}')
        return self._entity_model.model_validate(product_updated)

    async def update_all_product(self, product_code: int, product_data: dict) -> DBModel:
        print('Updating all product by code in repository')
        product_found = await self.collection.find_one({'product_code': product_code})
        if not product_found:
            return None
        validated_product = self._entity_model.model_validate(product_data)
        validated_product.id = product_found.get("_id")
        validated_product.create_at = product_found.get("create_at")
        validated_product.update_at = datetime.utcnow()
        await self.collection.replace_one({"product_code": product_code}, validated_product.model_dump(by_alias=True))
        product_all_updated = await self.collection.find_one({"product_code": product_code})
        print(f'Product all updated by code in repository: {product_all_updated}')
        return self._entity_model.model_validate(product_all_updated)

    async def deactivate_product(self, product_code: int, product_data: dict) -> DBModel:
        print('Deactivating product by code in repository')
        product_by_update = await self.collection.update_one({"product_code": product_code},
                                                             {"$set": {"is_deleted": product_data['is_deleted']}})
        if not product_by_update:
            return None
        product_deactivated = await self.collection.find_one({"product_code": product_code})
        print(f'Product deactivated by code in repository: {product_deactivated}')
        return self._entity_model.model_validate(product_deactivated)

    async def delete_product(self, product_code: int):
        print('Deleting product by code in repository')
        product_deleted = await self.collection.find_one_and_delete({"product_code": product_code})
        if not product_deleted:
            return None
        print(f'Product deleted by code in repository: {product_deleted}')
        return self._entity_model.model_validate(product_deleted)
