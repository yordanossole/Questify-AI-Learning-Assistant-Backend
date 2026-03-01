import magic

from fastapi import UploadFile
from sqlalchemy.orm import Session

from app.core.config import settings
from app.services.file_service import FileService
from app.services.chunk_service import ChunkService
from app.models.models import Material, User, Collection
from app.services.embedding_service import EmbeddingService
from app.repositories.material_repository import MaterialRepository
from app.core.exceptions import ValidationException, NotFoundException, ForbiddenException

class MaterialService:
    def __init__(self, db: Session):
        self.material_repo = MaterialRepository(db)
        self.file_service = FileService()
        self.chunk_service= ChunkService(db)
        self.embedding_service = EmbeddingService()

    async def upload(self, file: UploadFile, user):
        file_content = await file.read()
        file_type = magic.from_buffer(file_content, mime=True)
        file_size = file.file.tell()
        await file.seek(0)

        if file_size > settings.MAX_FILE_SIZE_BYTES:
            raise ValidationException("File too large")
        
        file_name = "_".join(file.filename.split()) if file.filename else ""
        
        file_key = await self.file_service.save_document(file=file, new_file_name=file_name, file_type=file_type, folder=settings.MATERIAL_FOLDER)

        material = Material(
            user_id=user.user_id,
            file_name=file_name,
            file_key=file_key,
            file_type=file_type,
            file_size=file_size,
            status="processing"
        )
        material = self.material_repo.create(material)
        return material

    async def delete(self, material_id: str, user: User):
        material = self.material_repo.get_by_id(material_id)
        if not material:
            raise NotFoundException("Material not found")
        
        if material.user_id != user.user_id:
            raise ForbiddenException("Access denied")
        
        await self.file_service.delete_document(file_key=material.file_key)
        self.material_repo.delete(material_id)

    async def preprocess(self, user: User, materials: list[Material]):
        # chunking
        collection_chunks = []
        for material in materials:
            material_chunks = self.chunk_service.get_chunks_by_material_id(material_id=str(material.material_id))
            if not material_chunks:
                file_data = await self.file_service.get_document(material.file_key)
                chunks = await self.chunk_service.extract_and_chunk(file_data)
                material_chunks = self.chunk_service.create_chunks_for_material(user, material.material_id, chunks)
            collection_chunks.append(material_chunks)

        # embedding and saving
        for material_chunks in collection_chunks:
            self.embedding_service.upload_chunks(material_chunks)

    def categorize(self, collection: Collection, material_ids: list[str]):
        materials = []
        for material_id in material_ids:
            material = self.material_repo.update(material_id, updates={"collection_id": collection.collection_id})
            materials.append(material)
        return materials