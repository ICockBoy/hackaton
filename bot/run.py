import asyncio
from bot.base import dp, bot, scheduler


def add_routers():
    import routers

    for router in routers.routers:
        dp.include_router(router)


async def start():
    scheduler.start()
    add_routers()
    print("bot started!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(start())
