from upstash_vector import Index

from app.core.config import settings

index = Index(
            url=settings.UPSTASH_VECTOR_REST_URL,
            token=settings.UPSTASH_VECTOR_REST_TOKEN,
        )