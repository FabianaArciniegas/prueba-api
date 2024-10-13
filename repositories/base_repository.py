from datetime import datetime
from enum import Enum
from typing import TypeVar, Generic, Type, Any

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

    async def create(self, data: dict, raise_exception: bool = True, session=None) -> DBModel:
        print(f'Creating in instance, data: {data}')
        document_created = self._entity_model.model_validate(data)
        data_parsed_enums = self.convert_enum_values(document_created.model_dump())
        data_parsed_enums["_id"] = data_parsed_enums.pop("id")

        await self.collection.insert_one(data_parsed_enums, session=session)
        if not document_created and raise_exception:
            raise ValueError("Instance not created")
        print(f'Instance created: {document_created}')
        return document_created

    async def get_by_id(self, _id: str, raise_exception: bool = True) -> DBModel | None:
        print('Getting in instance')
        document_found = await self.collection.find_one({"_id": _id, "is_deleted": False})
        if not document_found and raise_exception:
            raise ValueError("Instance not found")
        print(f'Instance found: {document_found}')
        return self._entity_model.model_validate(document_found)

    async def get_all(self, raise_exception: bool = True) -> list[DBModel]:
        print('Getting all instances')
        documents_found = self.collection.find({"is_deleted": False})
        documents_list = await documents_found.to_list(None)
        if not documents_list and raise_exception:
            raise ValueError("There are no products")
        all_documents = []
        for document in documents_list:
            validated_document = self._entity_model.model_validate(document)
            all_documents.append(validated_document)
        print(f'All instances found: {all_documents}')
        return all_documents

    async def update(self, _id: str, update_data: dict) -> DBModel:
        print('Updating instance data')
        update_data_filtered = {k: v for k, v in update_data.items() if v is not None}
        update_data_filtered["update_at"] = datetime.utcnow()
        await self.collection.update_one({"_id": _id}, {"$set": update_data_filtered})
        document_updated = await self.collection.find_one({"_id": _id})
        print(f'Instance updated data: {document_updated}')
        return self._entity_model.model_validate(document_updated)

    async def update_all(self, _id: str, product_data: dict) -> DBModel:
        print('Updating instance all data')
        validated_document = self._entity_model.model_validate(product_data)
        await self.collection.replace_one({"_id": _id}, validated_document.model_dump(exclude={"id"}))
        document_all_updated = await self.collection.find_one({"_id": _id})
        print(f'Instance updated all data: {document_all_updated}')
        return self._entity_model.model_validate(document_all_updated)

    async def disable(self, _id: str, update_data: dict) -> DBModel:
        print('Deactivating instance')
        await self.collection.update_one({"_id": _id}, {
            "$set": {"is_deleted": update_data['is_deleted'], "update_at": datetime.utcnow()}})
        document_disabled = await self.collection.find_one({"_id": _id})
        print(f'Instance disabled: {document_disabled}')
        return self._entity_model.model_validate(document_disabled)

    async def delete(self, _id: str):
        print('Deleting instance')
        document_deleted = await self.collection.find_one_and_delete({"_id": _id})
        print(f'Instance deleted: {document_deleted}')
        return self._entity_model.model_validate(document_deleted)
