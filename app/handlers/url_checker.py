from aiogram import Router, F
from aiogram.types import CallbackQuery, Message

from app.keyboards.main_menu import back_menu
from app.services.url_analysis import analyze_url

router = Router()

WAITING_URL = set()


@router.callback_query(F.data == "url_check")
async def request_url(callback: CallbackQuery):
    WAITING_URL.add(callback.from_user.id)

    await callback.answer()
    await callback.message.edit_text(
        "🔎 <b>Havolani dastlabki tekshirish</b>\n\n"
        "Tekshirmoqchi bo‘lgan URL manzilni yuboring.\n\n"
        "Masalan: https://example.com\n\n"
        "Eslatma: havola ochilmaydi. Bot faqat uning "
        "tarkibidagi ayrim belgilarni tekshiradi.",
        reply_markup=back_menu(),
    )


@router.message(F.text)
async def receive_url(message: Message):
    user_id = message.from_user.id

    if user_id not in WAITING_URL:
        return

    raw_url = message.text.strip()

    if len(raw_url) > 2048:
        await message.answer(
            "Havola juda uzun. 2048 belgidan qisqa URL yuboring."
        )
        return

    WAITING_URL.discard(user_id)

    result = analyze_url(raw_url)

    if not result["valid"]:
        await message.answer(
            f"⚠️ {result['message']}",
            reply_markup=back_menu(),
        )
        return

    warnings = "\n".join(
        f"• {warning}" for warning in result["warnings"]
    )

    await message.answer(
        "🔎 <b>Tekshiruv natijasi</b>\n\n"
        f"Domen: <code>{result['host']}</code>\n"
        f"Protokol: {result['scheme'].upper()}\n\n"
        f"<b>Natijalar:</b>\n{warnings}\n\n"
        "⚠️ Bu tekshiruv sayt xavfsizligini kafolatlamaydi. "
        "Shubhali havolada parol yoki tasdiqlash kodini kiritmang.",
        reply_markup=back_menu(),
    )