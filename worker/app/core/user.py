from app.prisma.prisma_client import get_prisma

async def get_user_details(user_id: str):
    Prisma = await get_prisma()
    user = await Prisma.user.find_unique(where={"id": user_id})
    return user.tokens, user.email

async def update_user_tokens(user_id: str, tokens: int) -> None:
    Prisma = await get_prisma()
    if tokens < 0:
        tokens = 0
    await Prisma.user.update(where={"id": user_id}, data={"tokens": tokens})

