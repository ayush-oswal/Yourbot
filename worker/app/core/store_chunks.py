from app.prisma.prisma_client import Prisma

async def store_chunks(chunks: list[str]):
    """
    Store chunks in postgres
    """
    try:
        chunk_ids = []
        for chunkText in chunks:
            chunk = await Prisma.chunk.create(
            data = {
                    "chunkText": chunkText
                }
            )
            chunk_ids.append(chunk.id)
        return chunk_ids
    except Exception as e:
        raise RuntimeError(f"Error storing chunks: {str(e)}")