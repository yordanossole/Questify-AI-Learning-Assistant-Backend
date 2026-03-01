import magic

from typing import Annotated
from starlette import status
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, UploadFile, File

from app.db.session import get_db
from app.models.models import User
from app.core.config import settings
from app.core.response import success_response
from app.schemas.response import MaterialResponse, CollectionResponse
from app.schemas.request import MaterialsRequest
from app.core.dependencies import get_current_user
from app.core.exceptions import ValidationException
from app.services.material_service import MaterialService
from app.services.collection_service import CollectionService

router = APIRouter()

@router.post("/upload", status_code=status.HTTP_201_CREATED)
async def upload_material(
	current_user: Annotated[User, Depends(get_current_user)],
	file: UploadFile = File(...),
	db: Session = Depends(get_db)
):
	material_service = MaterialService(db)
    
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
	material_service = MaterialService(db)
	await material_service.delete(material_id, current_user)

	return success_response("Material deleted successfully")

@router.post("/preprocess")
async def preprocess_materials(
	payload: MaterialsRequest,
	current_user: Annotated[User, Depends(get_current_user)],
	db: Session = Depends(get_db)
):
	material_ids = payload.material_ids
	collection_service = CollectionService(db)
	material_service = MaterialService(db)

	collection = collection_service.create_category(current_user)
	materials = material_service.categorize(collection, material_ids)
	await material_service.preprocess(current_user, materials)
	data = CollectionResponse.model_validate(collection)

	return success_response("Success", data=data)