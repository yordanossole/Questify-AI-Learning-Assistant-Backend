from typing import List, Optional
from sqlalchemy.orm import Session

from app.models.models import MaterialChunk
from app.core.exceptions import NotFoundException

class ChunkRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, chunk_id) -> Optional[MaterialChunk]:
        return self.db.query(MaterialChunk).filter(MaterialChunk.chunk_id == chunk_id).first()

    def get_all(self, skip: int = 0, limit: int = 100) -> List[MaterialChunk]:
        return self.db.query(MaterialChunk).offset(skip).limit(limit).all()

    def get_by_material_id(self, material_id: str) -> List[MaterialChunk]:
        return self.db.query(MaterialChunk).filter(MaterialChunk.material_id == material_id).all()

    def create(self, chunk: MaterialChunk) -> MaterialChunk:
        self.db.add(chunk)
        self.db.commit()
        self.db.refresh(chunk)
        return chunk

    def update(self, chunk_id, updates: dict) -> Optional[MaterialChunk]:
        chunk = self.get_by_id(chunk_id)
        if not chunk:
            raise NotFoundException("Chunk not found")
        for key, value in updates.items():
            setattr(chunk, key, value)
        self.db.commit()
        self.db.refresh(chunk)
        return chunk

    def delete(self, chunk_id) -> bool:
        chunk = self.get_by_id(chunk_id)
        if not chunk:
            raise NotFoundException("Chunk not found")
        self.db.delete(chunk)
        self.db.commit()
        return True