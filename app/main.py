from fastapi import FastAPI, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import get_db
from app.models import ReviewHistory, Category
from app.tasks import log_access
from app.services.sentiment_analysis import analyze_sentiment
from typing import List
from datetime import datetime

app = FastAPI()

@app.get("/reviews/trends")
def get_review_trends(db: Session = Depends(get_db)):
    # Log access asynchronously
    log_access.delay("GET /reviews/trends")
    
    # Complex query to get top 5 categories by average stars of latest reviews
    top_categories = (
        db.query(
            Category.id, 
            Category.name, 
            Category.description, 
            func.avg(ReviewHistory.stars).label('average_stars'),
            func.count(ReviewHistory.id).label('total_reviews')
        )
        .join(ReviewHistory, Category.id == ReviewHistory.category_id)
        .filter(
            ReviewHistory.id.in_(
                db.query(func.max(ReviewHistory.id))
                .group_by(ReviewHistory.review_id)
            )
        )
        .group_by(Category.id, Category.name, Category.description)
        .order_by(func.avg(ReviewHistory.stars).desc())
        .limit(5)
        .all()
    )
    
    return [
        {
            "id": cat.id,
            "name": cat.name,
            "description": cat.description,
            "average_stars": float(cat.average_stars),
            "total_reviews": cat.total_reviews
        } for cat in top_categories
    ]

@app.get("/reviews/")
def get_reviews_by_category(
    category_id: int = Query(...),
    page: int = Query(1, ge=1),
    db: Session = Depends(get_db)
):
    # Log access asynchronously
    log_access.delay(f"GET /reviews/?category_id={category_id}")
    
    page_size = 15
    offset = (page - 1) * page_size
    
    # Get latest reviews for the given category
    latest_reviews = (
        db.query(ReviewHistory)
        .filter(
            ReviewHistory.category_id == category_id,
            ReviewHistory.id.in_(
                db.query(func.max(ReviewHistory.id))
                .group_by(ReviewHistory.review_id)
            )
        )
        .order_by(ReviewHistory.created_at.desc())
        .offset(offset)
        .limit(page_size)
        .all()
    )
    
    # Analyze sentiment for reviews with null tone/sentiment
    for review in latest_reviews:
        if not review.tone or not review.sentiment:
            tone, sentiment = analyze_sentiment(review.text, review.stars)
            review.tone = tone or review.tone
            review.sentiment = sentiment or review.sentiment
            db.commit()
    
    return [
        {
            "id": review.id,
            "text": review.text,
            "stars": review.stars,
            "review_id": review.review_id,
            "created_at": review.created_at,
            "tone": review.tone,
            "sentiment": review.sentiment,
            "category_id": review.category_id
        } for review in latest_reviews
    ]