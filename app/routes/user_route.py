from typing import List, Optional

from fastapi import (
    APIRouter, 
    Depends,
    Query,
    Request,
    status
)
from pydantic import PositiveInt

from app.models.base_response_model import (
    ApiResponse, 
    GetApiResponse
)
from app.models.user_models import (
    UserCreationRequest, 
    UserCreationResponse,
    GetUserDetailsResponse,
    UserInfoResponse
)
from app.services.user_service import UserService
from app.utils.constants import UPDATED_AT
from app.utils.enums import OrderByTypes

router = APIRouter(prefix="/users", tags=["USER MANAGEMENT SERVICE"])


@router.post(
    "", 
    response_model=ApiResponse[UserCreationResponse], 
    status_code=status.HTTP_201_CREATED
)
async def create_user(
    request_state: Request,
    request: UserCreationRequest, 
    service: UserService = Depends(UserService)
) -> ApiResponse[UserCreationResponse]:
    return ApiResponse(data=service.create_user(
            logged_in_user_id=request_state.state.user.id, 
            request=request
        )
    )


@router.get(
    "", 
    response_model=GetApiResponse[List[GetUserDetailsResponse]], 
    status_code=status.HTTP_200_OK
)
async def get_all_users( 
    search: Optional[str] = Query(default=None),
    filter_by: Optional[str] = Query(default=None),
    filter_values: Optional[str] = Query(default=None),
    sort_by: Optional[str] = Query(default=UPDATED_AT),
    order_by: Optional[OrderByTypes] = OrderByTypes.DESC,
    page: Optional[PositiveInt] = Query(default=1),
    page_size: Optional[PositiveInt] = Query(default=10),
    service: UserService = Depends(UserService)
) -> GetApiResponse[List[GetUserDetailsResponse]]:
    total_count, response = service.get_all_users(
        search=search,
        filter_by=filter_by,
        filter_values=filter_values,
        sort_by=sort_by,
        order_by=order_by,
        page=page,
        page_size=page_size
    )

    return GetApiResponse(
        total_items=total_count,
        page=page,
        page_size=page_size,
        data=response,
    )


@router.get(
    "/data/{user_id}", 
    response_model=ApiResponse[GetUserDetailsResponse], 
    status_code=status.HTTP_200_OK
)
async def get_user_by_id(
    user_id: int, 
    service: UserService = Depends(UserService)
) -> ApiResponse[GetUserDetailsResponse]:
    return ApiResponse(data=service.get_user_by_id(user_id))


@router.get(
    "/info", 
    response_model=ApiResponse[UserInfoResponse], 
    status_code=status.HTTP_200_OK
)
async def get_user_info(
    request_state: Request,
    service: UserService = Depends(UserService)
) -> ApiResponse[UserInfoResponse]:
    return ApiResponse(data=service.get_user_info(request_state))