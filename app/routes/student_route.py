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
from app.models.student_models import (
    GetMappedBatchStudentResponse,
    MapStudentToBatchRequest,
    StudentRequest,
    GetStudentResponse,
    UpdatedBatchStudentRequest
)
from app.services.student_service import StudentService

router = APIRouter(prefix="/students", tags=["STUDENT MANAGEMENT SERVICE"])


@router.post(
    "", 
    response_model=ApiResponse[SuccessMessageResponse],
    status_code=status.HTTP_201_CREATED,
    summary="Create a new student"
)
async def create_student(
    request_state: Request,
    request: StudentRequest,
    service: StudentService = Depends(StudentService)
) -> ApiResponse[SuccessMessageResponse]:
    """
        Create a new student.
    """
    logged_in_user_id = request_state.state.user.id
    return ApiResponse(data=service.create_student(request, logged_in_user_id))


@router.get(    
    "", 
    response_model=ApiResponse[List[GetStudentResponse]],
    status_code=status.HTTP_200_OK,
    summary="Retrieve all students"
)
async def get_all_students(
    service: StudentService = Depends(StudentService)
) -> ApiResponse[List[GetStudentResponse]]:
    """
        Retrieve all students.
    """
    return ApiResponse(data=service.get_all_students())


@router.get(
    "/{student_id}", 
    response_model=ApiResponse[GetStudentResponse],
    status_code=status.HTTP_200_OK,
    summary="Retrieve student by id"
)
async def get_student_by_id(
    student_id: PositiveInt,
    service: StudentService = Depends(StudentService)
) -> ApiResponse[GetStudentResponse]:
    """
        Retrieve student by id.
    """
    return ApiResponse(data=service.get_student_by_id(student_id))


@router.put(
    "/{student_id}", 
    response_model=ApiResponse[SuccessMessageResponse],
    status_code=status.HTTP_200_OK,
    summary="Update student by id"
)
async def update_student_by_id(
    request_state: Request,
    student_id: PositiveInt,
    request: StudentRequest,
    service: StudentService = Depends(StudentService)
) -> ApiResponse[SuccessMessageResponse]:
    """
        Update student by id.
    """
    logged_in_user_id = request_state.state.user.id
    return ApiResponse(data=service.update_student_by_id(student_id, request, logged_in_user_id))


@router.delete(
    "/{student_id}", 
    response_model=ApiResponse[SuccessMessageResponse],
    status_code=status.HTTP_200_OK,
    summary="Delete student by id"
)
async def delete_student_by_id(
    student_id: PositiveInt,
    service: StudentService = Depends(StudentService)
) -> ApiResponse[SuccessMessageResponse]:
    """
        Delete student by id.
    """
    return ApiResponse(data=service.delete_student_by_id(student_id))


@router.post(
    "/{student_id}/batches",
    response_model=ApiResponse[SuccessMessageResponse],
    status_code=status.HTTP_201_CREATED,
    summary="Map student to a batch"
)
async def map_student_to_batch(
    student_id: PositiveInt,
    request_state: Request,
    request: MapStudentToBatchRequest,
    service: StudentService = Depends(StudentService)
) -> ApiResponse[SuccessMessageResponse]:
    logged_in_user_id = request_state.state.user.id
    return ApiResponse(data=service.map_student_to_batch(student_id, request, logged_in_user_id))


@router.get(
    "/batches/{batch_id}",
    response_model=ApiResponse[List[GetMappedBatchStudentResponse]],
    status_code=status.HTTP_200_OK,
    summary="Retrieve all students mapped to a batch"
)
async def get_batch_students(
    batch_id: PositiveInt,
    service: StudentService = Depends(StudentService)
) -> ApiResponse[List[GetMappedBatchStudentResponse]]:
    return ApiResponse(data=service.get_batch_students(batch_id))


@router.get(
    "/mappings/{mapping_id}",
    response_model=ApiResponse[GetMappedBatchStudentResponse],
    status_code=status.HTTP_200_OK,
    summary="Retrieve a student-batch mapping by ID"
)
async def get_batch_student_by_id(
    mapping_id: PositiveInt,
    service: StudentService = Depends(StudentService)
) -> ApiResponse[GetMappedBatchStudentResponse]:
    return ApiResponse(data=service.get_batch_student_by_id(mapping_id))


@router.put(
    "/mappings/{mapping_id}",
    response_model=ApiResponse[SuccessMessageResponse],
    status_code=status.HTTP_200_OK,
    summary="Update a student-batch mapping"
)
async def update_batch_student_by_id(
    mapping_id: PositiveInt,
    request_state: Request,
    request: UpdatedBatchStudentRequest,
    service: StudentService = Depends(StudentService)
) -> ApiResponse[SuccessMessageResponse]:
    logged_in_user_id = request_state.state.user.id
    return ApiResponse(data=service.update_batch_student_by_id(mapping_id, request, logged_in_user_id))


@router.delete(
    "/mappings/{mapping_id}",
    response_model=ApiResponse[SuccessMessageResponse],
    status_code=status.HTTP_200_OK,
    summary="Delete a student-batch mapping"
)
async def delete_batch_student_by_id(
    mapping_id: PositiveInt,
    service: StudentService = Depends(StudentService)
) -> ApiResponse[SuccessMessageResponse]:
    return ApiResponse(data=service.delete_batch_student_by_id(mapping_id))