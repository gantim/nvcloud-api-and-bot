from fastapi import HTTPException, status

NoPermissions = HTTPException(
    status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
    detail='No permissions for action'
)

UserAlreadySignUp = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Username already registered"
)

UserNotFound = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="User not found"
)

InvalidPassword = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Invalid password"
)

CredentialsException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)

EmailBusy = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Email already registered"
)

UnsupportedGrantType = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Unsupported grant type"
)
