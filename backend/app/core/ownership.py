from fastapi import HTTPException, status
from app.schemas.user import UserOut, UserRole


def check_self_or_admin(user: UserOut, resource_user_id: int) -> bool:
    """Check if user can access a resource (own data or admin)."""
    return user.role == UserRole.admin or user.id == resource_user_id


def require_self_or_admin(user: UserOut, resource_user_id: int) -> None:
    """Require that user can access the resource (own data or admin)."""
    if not check_self_or_admin(user, resource_user_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only access your own data"
        )


def check_booking_ownership(user: UserOut, booking_user_id: int) -> bool:
    """Check if user can access a booking (own booking or admin)."""
    return user.role == UserRole.admin or user.id == booking_user_id


def require_booking_ownership(user: UserOut, booking_user_id: int) -> None:
    """Require that user can access the booking (own booking or admin)."""
    if not check_booking_ownership(user, booking_user_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only access your own bookings"
        )


def check_user_ownership(user: UserOut, target_user_id: int) -> bool:
    """Check if user can access another user's data (own data or admin)."""
    return user.role == UserRole.admin or user.id == target_user_id


def require_user_ownership(user: UserOut, target_user_id: int) -> None:
    """Require that user can access the target user's data (own data or admin)."""
    if not check_user_ownership(user, target_user_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only access your own user data"
        )


def require_admin(user: UserOut) -> None:
    """Require that user is an admin."""
    if user.role != UserRole.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )


def is_admin(user: UserOut) -> bool:
    """Check if user is an admin."""
    return user.role == UserRole.admin
