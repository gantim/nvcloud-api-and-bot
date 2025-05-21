from app.domain.models.user import UserInDB
from app.domain.schemas.user import UserProfile


class ProfileUserUseCase:
    def __init__(self, user: UserInDB):
        self.user = user

    async def __call__(self) -> UserProfile:
        return UserProfile(
            username=self.user.username,
            email=self.user.email,
            full_name=self.user.full_name,
            registration_date=self.user.created_at, # type: ignore
            total_containers=0,
            is_superuser=self.user.is_superuser,
            tg_passcode=self.user.id.__str__() if not self.user.telegram_id else None
        )
