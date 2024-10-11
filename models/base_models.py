from datetime import datetime
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, Field


class DBModels(BaseModel):
    _collection_name: str
    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    id: str = Field(default_factory=lambda: str(uuid4()), alias="_id")
    create_at: datetime = Field(default_factory=datetime.utcnow)
    update_at: datetime = Field(default_factory=datetime.utcnow)
    is_deleted: bool = False
