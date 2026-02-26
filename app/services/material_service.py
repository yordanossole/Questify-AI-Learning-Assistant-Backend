import magic

from fastapi import UploadFile

from app.models.models import Material, User
from app.services.file_service import FileService
from app.core.config import settings
from app.repositories.material_repository import MaterialRepository
from app.core.exceptions import ValidationException, NotFoundException, ForbiddenException

class MaterialService:
    def __init__(self, material_repo: MaterialRepository, file_service: FileService):
        self.material_repo = material_repo
        self.file_service = file_service

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