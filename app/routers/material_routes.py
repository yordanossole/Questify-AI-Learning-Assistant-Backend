import magic

from typing import Annotated
from starlette import status
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, UploadFile, File

from app.db.session import get_db
from app.models.models import User
from app.core.config import settings
from app.core.response import success_response
from app.schemas.response import MaterialResponse
from app.core.dependencies import get_current_user
from app.core.exceptions import ValidationException
from app.repositories.material_repository import MaterialRepository
from app.services.material_service import MaterialService, FileService

router = APIRouter()

@router.post("/upload", status_code=status.HTTP_201_CREATED)
async def upload_material(
	current_user: Annotated[User, Depends(get_current_user)],
	file: UploadFile = File(...),
	db: Session = Depends(get_db)
):
	material_repo = MaterialRepository(db)
	file_service = FileService()
	material_service = MaterialService(material_repo, file_service)
    
	file_content = await file.read()
	file_type = magic.from_buffer(file_content, mime=True)
	await file.seek(0)

	if file_type not in settings.ALLOWED_FILES:
		raise ValidationException("File type not allowed")
	
	material = await material_service.upload(file, current_user)
	data = MaterialResponse.model_validate(material)

	return success_response("Material uploaded successfully", data=data)

@router.delete("/{material_id}")
async def delete_material(
	material_id: str,
	current_user: Annotated[User, Depends(get_current_user)],
	db: Session = Depends(get_db)
):
	material_service = MaterialRepository(db)
	file_service = FileService()
	service = MaterialService(material_service, file_service)
	await service.delete(material_id, current_user)

	return success_response("Material deleted successfully")