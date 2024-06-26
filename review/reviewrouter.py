from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from config.database import get_db
from models.usermodels import User
from dto.reviewschema import ReviewCreate
from config.token import get_currentUser
from .reviewservice import ReviewService

router = APIRouter(prefix="/review", tags=["Review"])


@router.get("/")
def get_all_reviews(db: Session = Depends(get_db)):
    return ReviewService.get_all(db=db)


@router.post("/create/{productid}")
def create_review(
    productid: int,
    request: ReviewCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_currentUser),
):
    print(request)
    print(productid)
    return ReviewService.create_review(
        request=request, productId=productid, db=db, current_user=current_user
    )


# @router.post("/product")
# def get_review(request: ReviewCreate):
#     return request
