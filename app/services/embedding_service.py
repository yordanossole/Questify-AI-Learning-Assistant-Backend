from typing import List
from upstash_vector.errors import ClientError

from app.models.models import MaterialChunk
from app.infrastructure.vdb_client import index
from app.core.exceptions import ExternalServiceException

class EmbeddingService:
    def __init__(self):
        self.index = index

    def upload_chunks(self, chunks: List[MaterialChunk]):
        try:
            vectors = []

            for chunk in chunks:
                meta_data = {
                    "chunk_index": chunk.chunk_index,
                    "material_id": str(chunk.material_id),
                    "user_id": str(chunk.user_id)
                }
                vectors.append({
                    "id": str(chunk.chunk_id),
                    "data": chunk.content,  
                    "metadata": meta_data
                })

            self.index.upsert(vectors)
        except ClientError as e:
            raise ExternalServiceException(str(e))

    # def search(
    #     self,
    #     query: str,
    #     top_k: int = 5,
    #     filter: Dict | None = None,
    # ):
    #     """
    #     Perform semantic search.
    #     Returns items with metadata and text
    #     """
    #     return self.index.query(
    #         vector=query,      # Upstash API will generate embedding from string
    #         top_k=top_k,
    #         filter=filter,
    #         include_metadata=True,
    #         include_vector=False,
    #         include_text=True  # get chunk text back
    #     )