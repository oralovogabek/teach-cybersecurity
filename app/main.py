import asyncio
import logging

from aiogram import Bot, Dispatcher

from app.config import BOT_TOKEN
from app.handlers import start, learning, quizzes, url_checker, progress


async def main():
    logging.basicConfig(level=logging.INFO)

    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    # Routerlarni ro‘yxatdan o‘tkazish
    dp.include_router(start.router)
    dp.include_router(learning.router)
    dp.include_router(quizzes.router)
    dp.include_router(url_checker.router)
    dp.include_router(progress.router)

    try:
        logging.info("CyberGuard UZ ishga tushmoqda...")
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())