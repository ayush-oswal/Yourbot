from app.prisma.prisma_client import Prisma

async def get_user_tokens(user_id: str) -> int:
    user = await Prisma.user.find_unique(where={"id": user_id})
    return user.tokens

async def update_user_tokens(user_id: str, tokens: int) -> None:
    await Prisma.user.update(where={"id": user_id}, data={"tokens": tokens})

