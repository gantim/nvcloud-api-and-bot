from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.domain.schemas.user import UserProfile
from app.domain.use_cases.info_user import ProfileUserUseCase
from app.presentation.dependencies.use_cases import get_profile_user_use_case


def get_user_router() -> APIRouter:
    router = APIRouter(prefix='/user', tags=['User'])


    @router.get('/profile', status_code=status.HTTP_200_OK)
    async def profile_handler(use_case: Annotated[ProfileUserUseCase, Depends(get_profile_user_use_case)]) -> UserProfile:
        return await use_case()

    return router
