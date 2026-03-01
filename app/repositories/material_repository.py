from typing import List, Optional
from sqlalchemy.orm import Session

from app.models.models import Material
from app.core.exceptions import NotFoundException

class MaterialRepository:
	def __init__(self, db: Session):
		self.db = db

	def get_by_id(self, material_id: str) -> Material:
		material = self.db.query(Material).filter(Material.material_id == material_id).first()
		if not material:
			raise NotFoundException("Material not found")
		
		return material

	def get_all(self, skip: int = 0, limit: int = 100) -> List[Material]:
		return self.db.query(Material).offset(skip).limit(limit).all()

	def create(self, material: Material) -> Material:
		self.db.add(material)
		self.db.commit()
		self.db.refresh(material)
		return material

	def update(self, material_id: str, updates: dict) -> Optional[Material]:
		material = self.get_by_id(material_id)
		if not material:
			raise NotFoundException("Material not found")
		for key, value in updates.items():
			setattr(material, key, value)
		self.db.commit()
		self.db.refresh(material)
		return material

	def delete(self, material_id: str) -> bool:
		material = self.get_by_id(material_id)
		if not material:
			raise NotFoundException("Material not found")
		self.db.delete(material)
		self.db.commit()