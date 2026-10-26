import json
from pathlib import Path

from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.keyboards.main_menu import learning_menu, back_menu

router = Router()

CONTENT_FILE = (
    Path(__file__).resolve().parents[1]
    / "content"
    / "lessons.json"
)

with CONTENT_FILE.open("r", encoding="utf-8") as file:
    LESSONS = json.load(file)


@router.callback_query(F.data == "learn")
async def show_learning_menu(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text(
        "📚 <b>Kiberxavfsizlik darslari</b>\n\n"
        "O‘rganmoqchi bo‘lgan yo‘nalishingizni tanlang:",
        reply_markup=learning_menu(),
    )


@router.callback_query(F.data.startswith("lesson:"))
async def show_lesson_topics(callback: CallbackQuery):
    section_id = callback.data.split(":", 1)[1]
    section = LESSONS.get(section_id)

    await callback.answer()

    if not section:
        await callback.message.answer(
            "Bu bo‘lim topilmadi.",
            reply_markup=back_menu(),
        )
        return

    builder = InlineKeyboardBuilder()

    for index, topic in enumerate(section["topics"]):
        builder.button(
            text=topic["title"],
            callback_data=f"topic:{section_id}:{index}",
        )

    builder.button(
        text="⬅️ Darslar bo‘limi",
        callback_data="learn",
    )
    builder.button(
        text="🏠 Asosiy menyu",
        callback_data="main_menu",
    )
    builder.adjust(1)

    await callback.message.edit_text(
        f"<b>{section['title']}</b>\n\n"
        f"{section['text']}\n\n"
        "O‘rganish uchun mavzuni tanlang:",
        reply_markup=builder.as_markup(),
    )


@router.callback_query(F.data.startswith("topic:"))
async def show_lesson(callback: CallbackQuery):
    parts = callback.data.split(":")

    if len(parts) != 3:
        await callback.answer("Noto‘g‘ri so‘rov.", show_alert=True)
        return

    section_id = parts[1]

    try:
        topic_index = int(parts[2])
    except ValueError:
        await callback.answer("Noto‘g‘ri mavzu.", show_alert=True)
        return

    section = LESSONS.get(section_id)

    if not section or not (
        0 <= topic_index < len(section["topics"])
    ):
        await callback.answer("Mavzu topilmadi.", show_alert=True)
        return

    topic = section["topics"][topic_index]

    await callback.answer()
    await callback.message.edit_text(
        f"<b>{topic['title']}</b>\n\n"
        f"{topic['body']}",
        reply_markup=back_to_topics(section_id),
    )


def back_to_topics(section_id: str):
    builder = InlineKeyboardBuilder()
    builder.button(
        text="⬅️ Mavzular ro‘yxati",
        callback_data=f"lesson:{section_id}",
    )
    builder.button(
        text="🏠 Asosiy menyu",
        callback_data="main_menu",
    )
    builder.adjust(1)
    return builder.as_markup()


@router.callback_query(F.data == "glossary")
async def show_glossary(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text(
        "📖 <b>Kiberxavfsizlik lug‘ati</b>\n\n"
        "<b>Phishing</b> — soxta xabar orqali ma’lumot olishga urinish.\n\n"
        "<b>Firewall</b> — tarmoq trafigini qoidalar asosida boshqaruvchi himoya.\n\n"
        "<b>Encryption</b> — ma’lumotni kalit yordamida shifrlash.\n\n"
        "<b>Vulnerability</b> — tizimdagi zaiflik.\n\n"
        "<b>Authentication</b> — foydalanuvchi kimligini tekshirish.\n\n"
        "<b>Authorization</b> — foydalanuvchining ruxsatlarini tekshirish.",
        reply_markup=back_menu(),
    )