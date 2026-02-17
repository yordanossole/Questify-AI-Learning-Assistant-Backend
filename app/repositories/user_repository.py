from sqlalchemy.orm import Session
from app.models.models import User

class UserRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_by_user_id(self, user_id):
        return self.db.query(User).filter(User.user_id == user_id).first()

    def get_by_email(self, email: str):
        return self.db.query(User).filter(User.email == email).first()

    def create(self, user: User):
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def verify_user(self, user: User):
        user.is_verified = True
        self.db.commit()
        self.db.refresh(user)
        return user