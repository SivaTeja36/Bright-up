from typing import List
from fastapi import (
    APIRouter, 
    Depends, 
    Request, 
    status
)
from pydantic import PositiveInt

from app.models.base_response_models import (
    ApiResponse, 
    SuccessMessageResponse
)
from app.models.batch_models import (
    BatchRequest,
    BatchStudentPaymentRequest,
    ClassScheduleRequest,
    GetBatchResponse,
    GetBatchStudentPayment,
    GetClassScheduleResponse,
    GetMappedBatchStudentResponse,
    MapUserToBatchRequest,
    UpdateClassScheduleRequest,
    UpdatedBatchStudentRequest
)
from app.models.user_models import GetUserDetailsResponse
from app.services.batch_service import BatchService

router = APIRouter(prefix="/batches", tags=["BATCH MANAGEMENT SERVICE"])


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
    logged_in_user_id = request_state.state.user.id
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
    logged_in_user_id = request_state.state.user.id
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


@router.post(
    "/{batch_id}/students",
    response_model=ApiResponse[SuccessMessageResponse],
    status_code=status.HTTP_201_CREATED
)
async def create_batch_students(
    request_state: Request,
    batch_id: PositiveInt,
    request: MapUserToBatchRequest,
    service: BatchService = Depends(BatchService)
) -> ApiResponse[SuccessMessageResponse]:
    loggedin_user_id = request_state.state.user.id
    return ApiResponse(data=service.create_batch_students(
            batch_id=batch_id, 
            request=request, 
            logged_in_user_id=loggedin_user_id
        )
    )


@router.get(
    "/{batch_id}/students",
    response_model=ApiResponse[List[GetMappedBatchStudentResponse]],
    status_code=status.HTTP_200_OK,
    summary="Retrieve all batch students"
)
async def get_batch_students(
    batch_id: PositiveInt,
    service: BatchService = Depends(BatchService)
) -> ApiResponse[List[GetMappedBatchStudentResponse]]:
    return ApiResponse(data=service.get_batch_students(batch_id))


@router.get(
    "/{batch_id}/students/{batch_student_id}",
    response_model=ApiResponse[GetMappedBatchStudentResponse],
    status_code=status.HTTP_200_OK,
    summary="Retrieve a batch student by ID"
)
async def get_batch_student_by_id(
    batch_id: PositiveInt,
    batch_student_id: PositiveInt,
    service: BatchService = Depends(BatchService)
) -> ApiResponse[GetMappedBatchStudentResponse]:
    return ApiResponse(data=service.get_batch_student_by_id(batch_id, batch_student_id))


@router.put(
    "/{batch_id}/students/{batch_student_id}",
    response_model=ApiResponse[SuccessMessageResponse],
    status_code=status.HTTP_200_OK,
    summary="Update a batch student"
)
async def update_batch_student_by_id(
    request_state: Request,
    batch_id: PositiveInt,
    batch_student_id: PositiveInt,
    request: UpdatedBatchStudentRequest,
    service: BatchService = Depends(BatchService)
) -> ApiResponse[SuccessMessageResponse]:
    logged_in_user_id = request_state.state.user.id
    return ApiResponse(data=service.update_batch_student_by_id(
            batch_id=batch_id, 
            batch_student_id=batch_student_id, 
            request=request, 
            logged_in_user_id=logged_in_user_id
        )
    )


@router.delete(
    "/{batch_id}/students/{batch_student_id}",
    response_model=ApiResponse[SuccessMessageResponse],
    status_code=status.HTTP_200_OK,
    summary="Delete a batch student"
)
async def delete_batch_student_by_id(
    batch_id: PositiveInt,
    batch_student_id: PositiveInt,
    service: BatchService = Depends(BatchService)
) -> ApiResponse[SuccessMessageResponse]:
    return ApiResponse(data=service.delete_batch_student_by_id(batch_id, batch_student_id))


@router.post(
    "/{batch_id}/students/{batch_student_id}/payments",
    response_model=ApiResponse[SuccessMessageResponse],
    status_code=status.HTTP_201_CREATED
)
async def create_batch_student_payment(
    request_state: Request,
    batch_id: PositiveInt,
    batch_student_id: PositiveInt,
    request: BatchStudentPaymentRequest,
    service: BatchService = Depends(BatchService)
) -> ApiResponse[SuccessMessageResponse]:
    loggedin_user_id = request_state.state.user.id
    return ApiResponse(data=service.create_batch_student_payment(
            batch_id=batch_id, 
            batch_student_id=batch_student_id,
            request=request, 
            logged_in_user_id=loggedin_user_id
        )
    )

@router.get(
    "/{batch_id}/students/{batch_student_id}/payments",
    response_model=ApiResponse[List[GetBatchStudentPayment]],
    status_code=status.HTTP_201_CREATED
)
async def get_all_batch_student_payments(
    batch_id: PositiveInt,
    batch_student_id: PositiveInt,
    service: BatchService = Depends(BatchService)
) -> ApiResponse[List[GetBatchStudentPayment]]:
    return ApiResponse(data=service.get_all_batch_student_payments(
            batch_id=batch_id, 
            batch_student_id=batch_student_id
        )
    )

@router.put(
    "/{batch_id}/students/{batch_student_id}/payments/{payment_id}",
    response_model=ApiResponse[SuccessMessageResponse],
    status_code=status.HTTP_201_CREATED
)
async def update_batch_student_payment_by_id(
    request_state: Request,
    batch_id: PositiveInt,
    batch_student_id: PositiveInt,
    payment_id: PositiveInt,
    request: BatchStudentPaymentRequest,
    service: BatchService = Depends(BatchService)
) -> ApiResponse[SuccessMessageResponse]:
    loggedin_user_id = request_state.state.user.id
    return ApiResponse(data=service.update_batch_student_payment_by_id(
            batch_id=batch_id, 
            batch_student_id=batch_student_id,
            payment_id=payment_id,
            request=request, 
            logged_in_user_id=loggedin_user_id
        )
    )


@router.post(
    "/{batch_id}/schedule-class",
    response_model=ApiResponse[SuccessMessageResponse],
    status_code=status.HTTP_201_CREATED
)
async def create_class_schedule(
    batch_id: PositiveInt,
    request: ClassScheduleRequest,
    request_state: Request,
    service: BatchService = Depends(BatchService)
) -> ApiResponse[SuccessMessageResponse]:
    user_id = request_state.state.user.id
    return ApiResponse(data=service.create_schedule(batch_id, request, user_id))


@router.get(
    "/{batch_id}/schedule-class",
    response_model=ApiResponse[List[GetClassScheduleResponse]],
    status_code=status.HTTP_200_OK
)
async def get_class_schedules_by_batch(
    batch_id: PositiveInt,
    service: BatchService = Depends(BatchService)
) -> ApiResponse[List[GetClassScheduleResponse]]:
    return ApiResponse(data=service.get_schedules_by_batch(batch_id))


@router.put(
    "/{batch_id}/schedule-class/{schedule_id}",
    response_model=ApiResponse[SuccessMessageResponse],
    status_code=status.HTTP_200_OK
)
async def update_class_schedule_by_id(
    schedule_id: PositiveInt,
    batch_id: PositiveInt,
    request: UpdateClassScheduleRequest,
    request_state: Request,
    service: BatchService = Depends(BatchService)
) -> ApiResponse[SuccessMessageResponse]:
    user_id = request_state.state.user.id
    return ApiResponse(data=service.update_schedule_by_id(schedule_id, batch_id, request, user_id))


@router.delete(
    "/{batch_id}/schedule-class/{schedule_id}",
    response_model=ApiResponse[SuccessMessageResponse],
    status_code=status.HTTP_200_OK
)
async def delete_class_schedule_by_id(
    schedule_id: PositiveInt,
    batch_id: PositiveInt,
    service: BatchService = Depends(BatchService)
) -> ApiResponse[SuccessMessageResponse]:
    return ApiResponse(data=service.delete_schedule_by_id(schedule_id, batch_id))
