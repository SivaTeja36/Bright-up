from typing import List
from fastapi import (
    APIRouter, 
    Depends, 
    Request, 
    status
)
from pydantic import PositiveInt

from app.models.base_response_model import (
    ApiResponse, 
    SuccessMessageResponse
)
from app.models.syllabus_models import (
    GetSyllabusResponse,
    SyllabusRequest
)
from app.services.syllabus_service import SyllabusService

router = APIRouter(prefix="/syllabus", tags=["SYLLABUS MANAGEMENT SERVICE"])


@router.post(
    "", 
    response_model=ApiResponse[SuccessMessageResponse],
    status_code=status.HTTP_201_CREATED,
    summary="Create a new syllabus"
)
async def create_syllabus(
    request_state: Request,
    request: SyllabusRequest,
    service: SyllabusService = Depends(SyllabusService)
) -> ApiResponse[SuccessMessageResponse]:
    """
        Create a new syllabus.
    """
    logged_in_user_id = request_state.state.user.user_id
    return ApiResponse(data=service.create_syllabus(request, logged_in_user_id))


@router.get(    
    "", 
    response_model=ApiResponse[List[GetSyllabusResponse]],
    status_code=status.HTTP_200_OK,
    summary="Retrive all syllabus"
)
async def get_all_syllabus(
    service: SyllabusService = Depends(SyllabusService)
) -> ApiResponse[List[GetSyllabusResponse]]:
    """
        Retrive all syllabus.
    """
    return ApiResponse(data=service.get_all_syllabus())


@router.get(
    "/{syllabus_id}", 
    response_model=ApiResponse[GetSyllabusResponse],
    status_code=status.HTTP_200_OK,
    summary="Retrive syllabus by id"
)
async def get_syllabus_by_id(
    syllabus_id: PositiveInt,
    service: SyllabusService = Depends(SyllabusService)
) -> ApiResponse[SuccessMessageResponse]:
    """
        Retrive syllabus by id.
    """
    return ApiResponse(data=service.get_syllabus_by_id(syllabus_id))


@router.put(
    "/{syllabus_id}", 
    response_model=ApiResponse[SuccessMessageResponse],
    status_code=status.HTTP_200_OK,
    summary="Update syllabus by id"
)
async def update_syllabus_by_id(
    request_state: Request,
    syllabus_id: PositiveInt,
    request: SyllabusRequest,
    service: SyllabusService = Depends(SyllabusService)
) -> ApiResponse[SuccessMessageResponse]:
    """
        Update syllabus by id.
    """
    logged_in_user_id = request_state.state.user.user_id
    return ApiResponse(data=service.update_syllabus_by_id(syllabus_id, request, logged_in_user_id))


@router.delete(
    "/{syllabus_id}", 
    response_model=ApiResponse[SuccessMessageResponse],
    status_code=status.HTTP_200_OK,
    summary="Delete syllabus by id"
)
async def delete_syllabus_by_id(
    syllabus_id: PositiveInt,
    service: SyllabusService = Depends(SyllabusService)
) -> ApiResponse[SuccessMessageResponse]:
    """
        Delete syllabus by id.
    """
    return ApiResponse(data=service.delete_syllabus_by_id(syllabus_id))