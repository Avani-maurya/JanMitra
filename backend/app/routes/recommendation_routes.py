from fastapi import APIRouter

from backend.app.models.user import User
from backend.app.services.recommendation_service import get_recommendations


router = APIRouter(
    prefix="/api/recommendations",
    tags=["Recommendations"],
)


@router.post("")
def recommend_schemes(user: User):
    return {
        "recommendations": get_recommendations(user)
    }