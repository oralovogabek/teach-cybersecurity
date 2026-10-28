
import asyncio
import logging
import os
from contextlib import suppress

from aiohttp import web
from aiogram import Bot, Dispatcher

from app.config import BOT_TOKEN
from app.handlers import (
    start,
    learning,
    quizzes,
    url_checker,
    progress,
)


# Logging sozlamalari
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)

logger = logging.getLogger(__name__)

# Hosting PORT qiymatini beradi.
# Lokal kompyuterda standart port: 10000
HOST = "0.0.0.0"
PORT = int(os.getenv("PORT", "10000"))


async def home(request: web.Request) -> web.Response:
    """Asosiy sahifa."""
    return web.json_response(
        {
            "service": "CyberGuard UZ",
            "status": "running",
            "message": "CyberGuard UZ serveri ishlayapti!",
        }
    )


async def health(request: web.Request) -> web.Response:
    """Server holatini tekshirish endpointi."""
    return web.json_response(
        {
            "service": "CyberGuard UZ",
            "status": "ok",
        }
    )


async def start_web_server() -> web.AppRunner:
    """aiohttp serverini ishga tushiradi."""
    app = web.Application()

    app.router.add_get("/", home)
    app.router.add_get("/health", health)

    runner = web.AppRunner(app)
    await runner.setup()

    site = web.TCPSite(
        runner,
        host=HOST,
        port=PORT,
    )
    await site.start()

    logger.info("HTTP server ishga tushdi: %s:%s", HOST, PORT)

    return runner


def setup_dispatcher() -> Dispatcher:
    """Dispatcher va barcha handlerlarni sozlaydi."""
    dp = Dispatcher()

    dp.include_router(start.router)
    dp.include_router(learning.router)
    dp.include_router(quizzes.router)
    dp.include_router(url_checker.router)
    dp.include_router(progress.router)

    logger.info("Barcha routerlar ro‘yxatdan o‘tkazildi.")

    return dp


async def main() -> None:
    """Bot va HTTP serverni birgalikda ishga tushiradi."""
    if not BOT_TOKEN:
        raise RuntimeError(
            "BOT_TOKEN topilmadi. app/config.py va .env faylini tekshiring."
        )

    bot = Bot(token=BOT_TOKEN)
    dp = setup_dispatcher()
    runner = None

    try:
        # HTTP serverni ishga tushirish
        runner = await start_web_server()

        # Telegram botni ishga tushirish
        logger.info("CyberGuard UZ bot ishga tushmoqda...")

        await dp.start_polling(
            bot,
            close_bot_session=False,
        )

    except asyncio.CancelledError:
        logger.info("Bot vazifasi bekor qilindi.")
        raise

    except Exception:
        logger.exception("Bot ishlashida xatolik yuz berdi.")
        raise

    finally:
        # HTTP serverni yopish
        if runner is not None:
            with suppress(Exception):
                await runner.cleanup()

        # Telegram sessiyasini yopish
        with suppress(Exception):
            await bot.session.close()

        logger.info("CyberGuard UZ to‘xtatildi.")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Dastur to‘xtatildi.")
