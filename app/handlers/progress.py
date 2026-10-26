from aiogram import Router, F
from aiogram.types import CallbackQuery

from app.keyboards.main_menu import back_menu
from app.handlers.quizzes import PROGRESS

router = Router()


@router.callback_query(F.data == "progress")
async def show_progress(callback: CallbackQuery):
    await callback.answer()

    result = PROGRESS.get(callback.from_user.id)

    if not result:
        await callback.message.edit_text(
            "📊 <b>Mening natijam</b>\n\n"
            "Sizda hali saqlangan test natijasi yo‘q.\n"
            "Bilimingizni tekshirish uchun testni boshlang!",
            reply_markup=back_menu(),
        )
        return

    score = result["score"]
    total = result["total"]
    percentage = score * 100 // total if total else 0

    await callback.message.edit_text(
        "📊 <b>Mening natijam</b>\n\n"
        f"Oxirgi test: {score}/{total}\n"
        f"Natija: {percentage}%\n\n"
        "Keyingi testlarda ham mashq qilib, "
        "bilimingizni oshirib boring.",
        reply_markup=back_menu(),
    )