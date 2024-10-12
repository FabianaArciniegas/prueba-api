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

    async def create(self, data: dict, session=None) -> DBModel:
        print(f'Creating in repository')
        document_created = self._entity_model.model_validate(data)
        if not document_created:
            return None
        data_parsed_enums = self.convert_enum_values(document_created.model_dump())
        data_parsed_enums["_id"] = data_parsed_enums.pop("id")
        await self.collection.insert_one(data_parsed_enums, session=session)
        print(f'Created in repository: {document_created}')
        return document_created

    async def get(self, field_name: str, field_value: str | int) -> DBModel:
        print('Getting in repository')
        document_found = await self.collection.find_one({field_name: field_value})
        if not document_found:
            return None
        print(f'Found in repository: {document_found}')
        return self._entity_model.model_validate(document_found)

    async def get_all(self, field_name: str, field_value: bool) -> list[DBModel]:
        print('Getting all in repository')
        documents_found = self.collection.find({field_name: field_value})
        documents_list = await documents_found.to_list(None)
        if not documents_list:
            return None
        all_documents = []
        for document in documents_list:
            validated_document = self._entity_model.model_validate(document)
            all_documents.append(validated_document)
        print(f'All documents found in repository: {all_documents}')
        return all_documents

    async def update(self, field_name: str, field_value: str | int, update_data: dict) -> DBModel:
        print('Updating some document data in repository')
        update_data_filtered = {k: v for k, v in update_data.items() if v is not None}
        update_data_filtered["update_at"] = datetime.utcnow()
        await self.collection.update_one({field_name: field_value}, {"$set": update_data_filtered})
        document_updated = await self.collection.find_one({field_name: field_value})
        print(f'User updated document data in repository: {document_updated}')
        return self._entity_model.model_validate(document_updated)

    async def update_all(self, field_name: str, field_value: str | int, update_data: dict) -> DBModel:
        print('Updating all document in repository')
        validated_document = self._entity_model.model_validate(update_data)
        await self.collection.replace_one({field_name: field_value}, validated_document.model_dump(exclude={"id"}))
        document_all_updated = await self.collection.find_one({field_name: field_value})
        print(f'Document all updated in repository: {document_all_updated}')
        return self._entity_model.model_validate(document_all_updated)

    async def deactivate(self, field_name: str, field_value: str | int, update_data: dict) -> DBModel:
        print('Deactivating document in repository')
        document_by_update = await self.collection.update_one({field_name: field_value},
                                                              {"$set": {"is_deleted": update_data['is_deleted'],
                                                                        "update_at": datetime.utcnow()}})
        if not document_by_update:
            return None
        document_deactivated = await self.collection.find_one({field_name: field_value})
        print(f'Document deactivated in repository: {document_deactivated}')
        return self._entity_model.model_validate(document_deactivated)

    async def delete(self, field_name: str, field_value: str | int):
        print('Deleting document in repository')
        document_deleted = await self.collection.find_one_and_delete({field_name: field_value})
        if not document_deleted:
            return None
        print(f'Document deleted in repository: {document_deleted}')
        return self._entity_model.model_validate(document_deleted)
