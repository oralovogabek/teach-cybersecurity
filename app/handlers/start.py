from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery

from app.keyboards.main_menu import main_menu

router = Router()


@router.message(CommandStart())
async def start_handler(message: Message):
    await message.answer(
        "🛡 <b>CyberGuard UZ</b>\n\n"
        "Assalomu alaykum!\n\n"
        "Bu bot orqali siz:\n"
        "• Internetdagi firibgarliklardan saqlanishni\n"
        "• Application Security asoslarini\n"
        "• Networking va Linux xavfsizligini\n"
        "• Kiberxavfsizlikning boshqa yo‘nalishlarini\n"
        "o‘rganishingiz mumkin.\n\n"
        "Boshlash uchun kerakli bo‘limni tanlang.",
        reply_markup=main_menu(),
    )


@router.callback_query(F.data == "main_menu")
async def return_to_menu(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text(
        "🛡 <b>CyberGuard UZ</b>\n\n"
        "Kerakli bo‘limni tanlang:",
        reply_markup=main_menu(),
    )


@router.message(Command("help"))
async def help_command(message: Message):
    await message.answer(
        "ℹ️ <b>Yordam</b>\n\n"
        "/start — asosiy menyu\n"
        "/help — yordam\n\n"
        "Bo‘limlarni tugmalar orqali tanlashingiz mumkin."
    )


@router.callback_query(F.data == "help")
async def help_callback(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text(
        "ℹ️ <b>Botdan foydalanish</b>\n\n"
        "📚 O‘rganish — xavfsizlik darslari.\n"
        "🔎 Havola tekshirish — shubhali URL belgilarini "
        "dastlabki tekshirish.\n"
        "🧠 Test — bilimingizni sinash.\n"
        "📊 Natijam — test natijalaringiz.\n\n"
        "Eslatma: URL tekshiruvi saytning mutlaq xavfsizligini "
        "kafolatlamaydi.",
        reply_markup=main_menu(),
    )