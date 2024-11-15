from app.prisma.prisma_client import get_prisma

async def get_user_tokens(user_id: str) -> int:
    Prisma = await get_prisma()
    user = await Prisma.user.find_unique(where={"id": user_id})
    return user.tokens

async def update_user_tokens(user_id: str, tokens: int) -> None:
    Prisma = await get_prisma()
    await Prisma.user.update(where={"id": user_id}, data={"tokens": tokens})

