# from typing import List
# from fastapi import UploadFile
# from app.repositories.chunk_repository import ChunkRepository
# from app.models.models import MaterialChunk

# import re
# import tiktoken


# class ChunkService:
#     def __init__(self, chunk_repo: ChunkRepository):
#         self.chunk_repo = chunk_repo

#     def pdf_to_text(self, file) -> str:
#         # Placeholder for PDF extraction logic (keep as noop for now)
#         return ""

#     def chunk_text_semantic(self,
#             self_text: str,
#             model: str = "gpt-4o-mini",
#             max_tokens: int = 600,
#             overlap_tokens: int = 100,
#         ) -> List[str]:
#         enc = tiktoken.encoding_for_model(model)

#         sentences = re.split(r'(?<=[.!?])\s+', self_text)

#         chunks = []
#         current_chunk = []
#         current_tokens = 0

#         for sentence in sentences:
#             sentence_tokens = len(enc.encode(sentence))

#             # if adding this sentence exceeds limit → flush
#             if current_tokens + sentence_tokens > max_tokens and current_chunk:
#                 chunk_text = " ".join(current_chunk)
#                 chunks.append(chunk_text)

#                 # create overlap
#                 overlap_text = enc.encode(chunk_text)[-overlap_tokens:]
#                 overlap_str = enc.decode(overlap_text)

#                 current_chunk = [overlap_str, sentence]
#                 current_tokens = len(enc.encode(overlap_str)) + sentence_tokens
#             else:
#                 current_chunk.append(sentence)
#                 current_tokens += sentence_tokens

#         if current_chunk:
#             chunks.append(" ".join(current_chunk))

#         return chunks

#     def extract_and_chunk(self, file: UploadFile, **kwargs) -> List[str]:
#         raw_text = self.pdf_to_text(file.file)
#         return self.chunk_text_semantic(raw_text, **kwargs)

#     def create_chunks_for_material(self, material_id, chunks: List[str]):
#         for chunk_text in chunks:
#             chunk = MaterialChunk(
#                 material_id=material_id,
#                 chunk_text=chunk_text,
#                 status="pending"
#             )
#             self.chunk_repo.create(chunk)

#     def delete_chunks_for_material(self, material_id):
#         chunks = self.chunk_repo.get_by_material_id(material_id)
#         for chunk in chunks:
#             self.chunk_repo.delete(chunk.chunk_id)

#     def get_chunks_by_material_id(self, material_id, **kwargs):
#         return self.chunk_repo.get_by_material_id(material_id, **kwargs)
