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
from app.models.batch_models import (
    BatchRequest,
    GetBatchResponse
)
from app.services.batch_service import BatchService

router = APIRouter(prefix="/batches", tags=["Batch Management Service"])


@router.post(
    "", 
    response_model=ApiResponse[SuccessMessageResponse],
    status_code=status.HTTP_201_CREATED,
    summary="Create a new batch"
)
async def create_batch(
    request_state: Request,
    request: BatchRequest,
    service: BatchService = Depends(BatchService)
) -> ApiResponse[SuccessMessageResponse]:
    """
        Create a new batch.
    """
    logged_in_user_id = request_state.state.user_id
    return ApiResponse(data=service.create_batch(request, logged_in_user_id))


@router.get(    
    "", 
    response_model=ApiResponse[List[GetBatchResponse]],
    status_code=status.HTTP_200_OK,
    summary="Retrieve all batches"
)
async def get_all_batches(
    service: BatchService = Depends(BatchService)
) -> ApiResponse[List[GetBatchResponse]]:
    """
        Retrieve all batches.
    """
    return ApiResponse(data=service.get_all_batches())


@router.get(
    "/{batch_id}", 
    response_model=ApiResponse[GetBatchResponse],
    status_code=status.HTTP_200_OK,
    summary="Retrieve batch by id"
)
async def get_batch_by_id(
    batch_id: PositiveInt,
    service: BatchService = Depends(BatchService)
) -> ApiResponse[GetBatchResponse]:
    """
        Retrieve batch by id.
    """
    return ApiResponse(data=service.get_batch_by_id(batch_id))


@router.put(
    "/{batch_id}", 
    response_model=ApiResponse[SuccessMessageResponse],
    status_code=status.HTTP_200_OK,
    summary="Update batch by id"
)
async def update_batch_by_id(
    request_state: Request,
    batch_id: PositiveInt,
    request: BatchRequest,
    service: BatchService = Depends(BatchService)
) -> ApiResponse[SuccessMessageResponse]:
    """
        Update batch by id.
    """
    logged_in_user_id = request_state.state.user_id
    return ApiResponse(data=service.update_batch_by_id(batch_id, request, logged_in_user_id))


@router.delete(
    "/{batch_id}", 
    response_model=ApiResponse[SuccessMessageResponse],
    status_code=status.HTTP_200_OK,
    summary="Delete batch by id"
)
async def delete_batch_by_id(
    batch_id: PositiveInt,
    service: BatchService = Depends(BatchService)
) -> ApiResponse[SuccessMessageResponse]:
    """
        Delete batch by id.
    """
    return ApiResponse(data=service.delete_batch_by_id(batch_id))