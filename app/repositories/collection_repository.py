from sqlalchemy.orm import Session
from typing import List, Optional

from app.models.models import Collection
from app.core.exceptions import NotFoundException

class CollectionRepository:
	def __init__(self, db: Session):
		self.db = db

	def get_by_id(self, collection_id) -> Optional[Collection]:
		return self.db.query(Collection).filter(Collection.collection_id == collection_id).first()

	def get_all(self, skip: int = 0, limit: int = 100) -> List[Collection]:
		return self.db.query(Collection).offset(skip).limit(limit).all()

	def create(self, collection: Collection) -> Collection:
		self.db.add(collection)
		self.db.commit()
		self.db.refresh(collection)
		return collection

	def update(self, collection_id, updates: dict) -> Optional[Collection]:
		collection = self.get_by_id(collection_id)
		if not collection:
			raise NotFoundException("Collection not found")
		for key, value in updates.items():
			setattr(collection, key, value)
		self.db.commit()
		self.db.refresh(collection)
		return collection

	def delete(self, collection_id) -> bool:
		collection = self.get_by_id(collection_id)
		if not collection:
			raise NotFoundException("Collection not found")
		self.db.delete(collection)
		self.db.commit()
		return True