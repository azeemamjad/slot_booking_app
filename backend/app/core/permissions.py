from enum import Enum
from typing import List, Dict, Set, Optional
from functools import wraps
from fastapi import HTTPException, status, Depends
from app.schemas.user import UserOut, UserRole
from app.core.dependencies import get_current_user


class Permission(str, Enum):
    # User Management
    USER_READ = "user:read"
    USER_CREATE = "user:create"
    USER_UPDATE = "user:update"
    USER_DELETE = "user:delete"
    USER_READ_ALL = "user:read_all"
    
    # Department Management
    DEPARTMENT_READ = "department:read"
    DEPARTMENT_CREATE = "department:create"
    DEPARTMENT_UPDATE = "department:update"
    DEPARTMENT_DELETE = "department:delete"
    
    # Game Management
    GAME_READ = "game:read"
    GAME_CREATE = "game:create"
    GAME_UPDATE = "game:update"
    GAME_DELETE = "game:delete"
    
    # Slot Management
    SLOT_READ = "slot:read"
    SLOT_CREATE = "slot:create"
    SLOT_UPDATE = "slot:update"
    SLOT_DELETE = "slot:delete"
    
    # Booking Management
    BOOKING_READ = "booking:read"
    BOOKING_CREATE = "booking:create"
    BOOKING_UPDATE = "booking:update"
    BOOKING_DELETE = "booking:delete"
    BOOKING_READ_ALL = "booking:read_all"
    BOOKING_CONFIRM = "booking:confirm"
    BOOKING_RESET = "booking:reset"


class PermissionManager:
    """Manages role-based permissions for the application."""
    
    def __init__(self):
        self._role_permissions: Dict[UserRole, Set[Permission]] = {
            UserRole.admin: {
                # Admin has all permissions
                Permission.USER_READ,
                Permission.USER_CREATE,
                Permission.USER_UPDATE,
                Permission.USER_DELETE,
                Permission.USER_READ_ALL,
                Permission.DEPARTMENT_READ,
                Permission.DEPARTMENT_CREATE,
                Permission.DEPARTMENT_UPDATE,
                Permission.DEPARTMENT_DELETE,
                Permission.GAME_READ,
                Permission.GAME_CREATE,
                Permission.GAME_UPDATE,
                Permission.GAME_DELETE,
                Permission.SLOT_READ,
                Permission.SLOT_CREATE,
                Permission.SLOT_UPDATE,
                Permission.SLOT_DELETE,
                Permission.BOOKING_READ,
                Permission.BOOKING_CREATE,
                Permission.BOOKING_UPDATE,
                Permission.BOOKING_DELETE,
                Permission.BOOKING_READ_ALL,
                Permission.BOOKING_CONFIRM,
                Permission.BOOKING_RESET,
            },
            UserRole.normal: {
                # Normal users have limited permissions
                # Permission.USER_CREATE,  # Can create their own account (via registration)
                Permission.USER_READ,  # Can read own profile
                Permission.USER_UPDATE,  # Can update own profile
                Permission.DEPARTMENT_READ,  # Can view departments
                Permission.GAME_READ,  # Can view games
                Permission.SLOT_READ,  # Can view slots
                Permission.BOOKING_READ,  # Can read own bookings
                Permission.BOOKING_CREATE,  # Can create own bookings
                Permission.BOOKING_UPDATE,  # Can update own bookings
            }
        }
    
    def has_permission(self, user: UserOut, permission: Permission) -> bool:
        """Check if user has a specific permission."""
        user_permissions = self._role_permissions.get(user.role, set())
        return permission in user_permissions
    
    def has_any_permission(self, user: UserOut, permissions: List[Permission]) -> bool:
        """Check if user has any of the specified permissions."""
        user_permissions = self._role_permissions.get(user.role, set())
        return any(permission in user_permissions for permission in permissions)
    
    def has_all_permissions(self, user: UserOut, permissions: List[Permission]) -> bool:
        """Check if user has all of the specified permissions."""
        user_permissions = self._role_permissions.get(user.role, set())
        return all(permission in user_permissions for permission in permissions)
    
    def get_user_permissions(self, user: UserOut) -> Set[Permission]:
        """Get all permissions for a user."""
        return self._role_permissions.get(user.role, set())


# Global permission manager instance
permission_manager = PermissionManager()


def require_permission(permission: Permission):
    """Decorator to require a specific permission."""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Extract current_user from kwargs
            current_user = kwargs.get('current_user')
            if not current_user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Authentication required"
                )
            
            if not permission_manager.has_permission(current_user, permission):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Insufficient permissions. Required: {permission}"
                )
            
            return await func(*args, **kwargs)
        return wrapper
    return decorator


def require_any_permission(permissions: List[Permission]):
    """Decorator to require any of the specified permissions."""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            current_user = kwargs.get('current_user')
            if not current_user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Authentication required"
                )
            
            if not permission_manager.has_any_permission(current_user, permissions):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Insufficient permissions. Required one of: {permissions}"
                )
            
            return await func(*args, **kwargs)
        return wrapper
    return decorator


def require_all_permissions(permissions: List[Permission]):
    """Decorator to require all of the specified permissions."""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            current_user = kwargs.get('current_user')
            if not current_user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Authentication required"
                )
            
            if not permission_manager.has_all_permissions(current_user, permissions):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Insufficient permissions. Required all: {permissions}"
                )
            
            return await func(*args, **kwargs)
        return wrapper
    return decorator


# Permission dependency functions
def require_user_read_permission(current_user: UserOut = Depends(get_current_user)) -> UserOut:
    """Dependency to require user read permission."""
    if not permission_manager.has_permission(current_user, Permission.USER_READ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions to read user data"
        )
    return current_user


def require_user_create_permission(current_user: UserOut = Depends(get_current_user)) -> UserOut:
    """Dependency to require user create permission (for admin user management)."""
    if not permission_manager.has_permission(current_user, Permission.USER_CREATE):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions to create users"
        )
    return current_user


def require_user_update_permission(current_user: UserOut = Depends(get_current_user)) -> UserOut:
    """Dependency to require user update permission."""
    if not permission_manager.has_permission(current_user, Permission.USER_UPDATE):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions to update users"
        )
    return current_user


def require_user_delete_permission(current_user: UserOut = Depends(get_current_user)) -> UserOut:
    """Dependency to require user delete permission."""
    if not permission_manager.has_permission(current_user, Permission.USER_DELETE):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions to delete users"
        )
    return current_user


def require_department_read_permission(current_user: UserOut = Depends(get_current_user)) -> UserOut:
    """Dependency to require department read permission."""
    if not permission_manager.has_permission(current_user, Permission.DEPARTMENT_READ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions to read department data"
        )
    return current_user


def require_department_create_permission(current_user: UserOut = Depends(get_current_user)) -> UserOut:
    """Dependency to require department create permission."""
    if not permission_manager.has_permission(current_user, Permission.DEPARTMENT_CREATE):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions to create departments"
        )
    return current_user


def require_department_update_permission(current_user: UserOut = Depends(get_current_user)) -> UserOut:
    """Dependency to require department update permission."""
    if not permission_manager.has_permission(current_user, Permission.DEPARTMENT_UPDATE):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions to update departments"
        )
    return current_user


def require_department_delete_permission(current_user: UserOut = Depends(get_current_user)) -> UserOut:
    """Dependency to require department delete permission."""
    if not permission_manager.has_permission(current_user, Permission.DEPARTMENT_DELETE):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions to delete departments"
        )
    return current_user


def require_game_read_permission(current_user: UserOut = Depends(get_current_user)) -> UserOut:
    """Dependency to require game read permission."""
    if not permission_manager.has_permission(current_user, Permission.GAME_READ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions to read game data"
        )
    return current_user


def require_game_create_permission(current_user: UserOut = Depends(get_current_user)) -> UserOut:
    """Dependency to require game create permission."""
    if not permission_manager.has_permission(current_user, Permission.GAME_CREATE):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions to create games"
        )
    return current_user


def require_game_update_permission(current_user: UserOut = Depends(get_current_user)) -> UserOut:
    """Dependency to require game update permission."""
    if not permission_manager.has_permission(current_user, Permission.GAME_UPDATE):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions to update games"
        )
    return current_user


def require_game_delete_permission(current_user: UserOut = Depends(get_current_user)) -> UserOut:
    """Dependency to require game delete permission."""
    if not permission_manager.has_permission(current_user, Permission.GAME_DELETE):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions to delete games"
        )
    return current_user


def require_slot_read_permission(current_user: UserOut = Depends(get_current_user)) -> UserOut:
    """Dependency to require slot read permission."""
    if not permission_manager.has_permission(current_user, Permission.SLOT_READ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions to read slot data"
        )
    return current_user


def require_slot_create_permission(current_user: UserOut = Depends(get_current_user)) -> UserOut:
    """Dependency to require slot create permission."""
    if not permission_manager.has_permission(current_user, Permission.SLOT_CREATE):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions to create slots"
        )
    return current_user


def require_slot_update_permission(current_user: UserOut = Depends(get_current_user)) -> UserOut:
    """Dependency to require slot update permission."""
    if not permission_manager.has_permission(current_user, Permission.SLOT_UPDATE):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions to update slots"
        )
    return current_user


def require_slot_delete_permission(current_user: UserOut = Depends(get_current_user)) -> UserOut:
    """Dependency to require slot delete permission."""
    if not permission_manager.has_permission(current_user, Permission.SLOT_DELETE):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions to delete slots"
        )
    return current_user


def require_booking_read_permission(current_user: UserOut = Depends(get_current_user)) -> UserOut:
    """Dependency to require booking read permission."""
    if not permission_manager.has_permission(current_user, Permission.BOOKING_READ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions to read booking data"
        )
    return current_user


def require_booking_create_permission(current_user: UserOut = Depends(get_current_user)) -> UserOut:
    """Dependency to require booking create permission."""
    if not permission_manager.has_permission(current_user, Permission.BOOKING_CREATE):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions to create bookings"
        )
    return current_user


def require_booking_update_permission(current_user: UserOut = Depends(get_current_user)) -> UserOut:
    """Dependency to require booking update permission."""
    if not permission_manager.has_permission(current_user, Permission.BOOKING_UPDATE):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions to update bookings"
        )
    return current_user


def require_booking_delete_permission(current_user: UserOut = Depends(get_current_user)) -> UserOut:
    """Dependency to require booking delete permission."""
    if not permission_manager.has_permission(current_user, Permission.BOOKING_DELETE):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions to delete bookings"
        )
    return current_user


def require_booking_confirm_permission(current_user: UserOut = Depends(get_current_user)) -> UserOut:
    """Dependency to require booking confirm permission."""
    if not permission_manager.has_permission(current_user, Permission.BOOKING_CONFIRM):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions to confirm bookings"
        )
    return current_user


def require_booking_reset_permission(current_user: UserOut = Depends(get_current_user)) -> UserOut:
    """Dependency to require booking reset permission."""
    if not permission_manager.has_permission(current_user, Permission.BOOKING_RESET):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions to reset bookings"
        )
    return current_user



