import json

from starlette import status
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from app.schemas.response import ApiResponse

def success_response(message: str, data=None, status_code: int=status.HTTP_200_OK):
    if isinstance(data, BaseModel):
        data = json.loads(data.model_dump_json())

    return JSONResponse(
        status_code=status_code,
        content=ApiResponse(success=True, message=message, data=data).model_dump()
    )

def error_response(message: str, status_code: int=status.HTTP_400_BAD_REQUEST):
    return JSONResponse(
        status_code=status_code,
        content=ApiResponse(success=False, message=message, data=None).model_dump()
    )