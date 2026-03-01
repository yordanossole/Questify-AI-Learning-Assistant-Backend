from sqlalchemy.orm import Session

from app.models.models import Collection, User
from app.repositories.collection_repository import CollectionRepository

class CollectionService:
    def __init__(self, db: Session):
        self.collection_repo = CollectionRepository(db)

    def create_category(self, user: User):
        collection = Collection(user_id=user.user_id)
        return self.collection_repo.create(collection)
