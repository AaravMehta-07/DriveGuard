from fastapi import APIRouter, Depends
from pydantic import BaseModel
from ..dependencies import get_current_user, User

router = APIRouter(prefix="/auth", tags=["auth"])

class UserProfile(BaseModel):
    display_name: str | None = None
    avatar_url: str | None = None

@router.get("/profile", response_model=User)
async def get_profile(user: User = Depends(get_current_user)):
    """Get current user profile"""
    return user

@router.put("/profile", response_model=User)
async def update_profile(profile: UserProfile, user: User = Depends(get_current_user)):
    """Update current user profile"""
    return user

@router.delete("/account")
async def delete_account(user: User = Depends(get_current_user)):
    """Delete user account and all associated data"""
    return {"status": "deleted"}
