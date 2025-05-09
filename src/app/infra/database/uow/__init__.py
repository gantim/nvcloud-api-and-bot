from app.infra.database.session import SessionFactory

from .uow import SQLAlchemyUnitOfWork


def get_uow():
    return SQLAlchemyUnitOfWork(SessionFactory)
