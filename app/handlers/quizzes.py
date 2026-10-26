import json
import random
from pathlib import Path

from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

router = Router()

QUIZ_FILE = (
    Path(__file__).resolve().parents[1]
    / "content"
    / "quizzes.json"
)

with QUIZ_FILE.open("r", encoding="utf-8") as file:
    QUESTIONS = json.load(file)

# MVP uchun vaqtinchalik xotira.
# Bot qayta ishga tushsa, natijalar yo‘qoladi.
SESSIONS = {}
PROGRESS = {}


def question_keyboard(options, question_index):
    builder = InlineKeyboardBuilder()

    for index, option in enumerate(options):
        builder.button(
            text=option,
            callback_data=f"answer:{question_index}:{index}",
        )

    builder.button(
        text="🏠 Asosiy menyu",
        callback_data="main_menu",
    )
    builder.adjust(1)
    return builder.as_markup()


async def send_question(callback, user_id):
    session = SESSIONS[user_id]
    question_index = session["order"][session["position"]]
    question = QUESTIONS[question_index]

    await callback.message.edit_text(
        f"🧠 <b>Test</b>\n\n"
        f"Savol {session['position'] + 1}/"
        f"{len(session['order'])}\n\n"
        f"{question['question']}",
        reply_markup=question_keyboard(
            question["options"],
            question_index,
        ),
    )


@router.callback_query(F.data == "quiz")
async def start_quiz(callback: CallbackQuery):
    await callback.answer()

    if not QUESTIONS:
        await callback.message.edit_text(
            "Hozircha test savollari mavjud emas."
        )
        return

    user_id = callback.from_user.id
    order = list(range(len(QUESTIONS)))
    random.shuffle(order)

    SESSIONS[user_id] = {
        "order": order,
        "position": 0,
        "score": 0,
        "answered": False,
    }

    await send_question(callback, user_id)


@router.callback_query(F.data.startswith("answer:"))
async def check_answer(callback: CallbackQuery):
    user_id = callback.from_user.id
    session = SESSIONS.get(user_id)

    if not session:
        await callback.answer(
            "Testni qaytadan boshlang.",
            show_alert=True,
        )
        return

    parts = callback.data.split(":")

    try:
        question_index = int(parts[1])
        answer_index = int(parts[2])
    except (ValueError, IndexError):
        await callback.answer("Noto‘g‘ri javob.", show_alert=True)
        return

    expected_index = session["order"][session["position"]]

    if question_index != expected_index or session["answered"]:
        await callback.answer(
            "Bu savolga javob berilgan yoki eskirgan.",
            show_alert=True,
        )
        return

    question = QUESTIONS[question_index]

    if not 0 <= answer_index < len(question["options"]):
        await callback.answer("Javob topilmadi.", show_alert=True)
        return

    session["answered"] = True
    correct = answer_index == question["correct"]

    if correct:
        session["score"] += 1
        result_text = "✅ To‘g‘ri javob!"
    else:
        result_text = (
            "❌ Noto‘g‘ri javob.\n"
            f"To‘g‘ri javob: "
            f"{question['options'][question['correct']]}"
        )

    builder = InlineKeyboardBuilder()
    builder.button(
        text="➡️ Keyingi savol",
        callback_data="quiz_next",
    )
    builder.button(
        text="🏠 Asosiy menyu",
        callback_data="main_menu",
    )
    builder.adjust(1)

    await callback.answer("Javob qabul qilindi.")
    await callback.message.edit_text(
        f"{result_text}\n\n"
        f"💡 {question['explanation']}",
        reply_markup=builder.as_markup(),
    )


@router.callback_query(F.data == "quiz_next")
async def next_question(callback: CallbackQuery):
    user_id = callback.from_user.id
    session = SESSIONS.get(user_id)

    if not session:
        await callback.answer("Testni qayta boshlang.", show_alert=True)
        return

    if not session["answered"]:
        await callback.answer("Avval savolga javob bering.")
        return

    session["position"] += 1
    session["answered"] = False

    if session["position"] >= len(session["order"]):
        score = session["score"]
        total = len(session["order"])

        PROGRESS[user_id] = {
            "score": score,
            "total": total,
        }

        await callback.answer()
        await callback.message.edit_text(
            "🏁 <b>Test yakunlandi!</b>\n\n"
            f"Natijangiz: {score}/{total}\n"
            f"Foiz: {score * 100 // total}%\n\n"
            "Mashq qilish uchun testni yana boshlashingiz mumkin.",
            reply_markup=finish_keyboard(),
        )
        SESSIONS.pop(user_id, None)
        return

    await callback.answer()
    await send_question(callback, user_id)


def finish_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text="🔄 Qayta test", callback_data="quiz")
    builder.button(text="🏠 Asosiy menyu", callback_data="main_menu")
    builder.adjust(1)
    return builder.as_markup()