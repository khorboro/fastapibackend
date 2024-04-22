from fastapi import Depends, HTTPException
from models.productmodels import ProductModel

from config.token import get_currentUser
from models.reviewmodels import ReviewModel
from sqlalchemy import func
from models.usermodels import User
from config.database import get_db
from sqlalchemy.orm import Session
from dto.reviewschema import ReviewCreate


class ReviewService:
    def get_all(db: Session):
        return db.query(ReviewModel).all()

    def create_review(
        request: ReviewCreate,
        productId: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_currentUser),
    ):
        try:
            # Ambil produk yang akan direview
            product = db.query(ProductModel).filter(ProductModel.id == productId).first()

            if not product:
                raise HTTPException(
                    status_code=404,
                    detail="Product not found",
                )

            existing_review = db.query(ReviewModel).filter(
                ReviewModel.user_id == current_user.id,
                ReviewModel.product_id == productId
            ).first()

            if existing_review:
                raise HTTPException(
                    status_code=400,
                    detail="Review already exists",
                )

            review_new = ReviewModel(
                name=current_user.name,
                user_id=current_user.id,
                rating=request.rating,
                comment=request.comment,
                product_id=productId
            )

            db.add(review_new)
            db.commit()

            total_rating, total_reviews = db.query(
                func.sum(ReviewModel.rating), func.count(ReviewModel.id)
            ).filter(
                ReviewModel.product_id == productId
            ).first()

            if total_rating is None:
                total_rating = 0
            if total_reviews is None:
                total_reviews = 0

            current_average_rating = total_rating / total_reviews

            total_rating -= request.rating
            total_reviews -= 1

            new_average_rating = current_average_rating if total_reviews == 0 else total_rating / total_reviews

            product.rating = int(new_average_rating)
            db.commit()
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=500,
                detail="Internal Server Error",
            )