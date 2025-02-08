from app.prisma.prisma_client import get_prisma
async def store_chunks(chunks: list[str]):
    """
    Store chunks in postgres
    """
    try:
        chunk_ids = []
        Prisma = await get_prisma()
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