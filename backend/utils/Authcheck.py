from fastapi import HTTPException
from models import User
from schema import UserRole


# Helper function for ownership checks
def check_ownership(resource_owner_id: str, user: User):
    """
    Admins can access anything.
    Others can only access their own resources.
    """
    if user.role == UserRole.admin:
        return   # admin bypasses ownership check

    if resource_owner_id != user.id:
        raise HTTPException(
            status_code=403,
            detail="You do not have permission to access this resource"
        )


