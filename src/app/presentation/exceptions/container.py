from fastapi import HTTPException, status

TicketContainerClosed = HTTPException(
    status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
    detail="Ticket container already closed"
)

ContainerNotFound = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Container not found"
)
