# from typing import Optional
# from app.repositories.collection_repository import CollectionRepository
# from app.repositories.material_repository import MaterialRepository


# class CollectionService:
#     def __init__(self, collection_repo: CollectionRepository, material_repo: MaterialRepository):
#         self.collection_repo = collection_repo
#         self.material_repo = material_repo

#     def add_material_to_collection(self, collection_id, material_id, user) -> bool:
#         collection = self.collection_repo.get_by_id(collection_id)
#         material = self.material_repo.get_by_id(material_id)
#         if not collection or not material:
#             return False
#         if collection.user_id != user.user_id or material.user_id != user.user_id:
#             return False

#         # Append material to collection relationship and commit
#         collection.materials.append(material)
#         self.collection_repo.db.commit()
#         return True

#     def get_collection(self, collection_id) -> Optional[object]:
#         return self.collection_repo.get_by_id(collection_id)
