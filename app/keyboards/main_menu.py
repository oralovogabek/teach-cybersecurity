from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def main_menu() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(
        text="📚 Kiberxavfsizlikni o‘rganish",
        callback_data="learn",
    )
    builder.button(
        text="🔎 Havolani tekshirish",
        callback_data="url_check",
    )
    builder.button(
        text="🧠 Bilimlar testi",
        callback_data="quiz",
    )
    builder.button(
        text="📊 Mening natijam",
        callback_data="progress",
    )
    builder.button(
        text="📖 Kiberxavfsizlik lug‘ati",
        callback_data="glossary",
    )
    builder.button(
        text="ℹ️ Yordam",
        callback_data="help",
    )

    builder.adjust(1)
    return builder.as_markup()


def learning_menu() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    sections = [
        ("🌐 Internet xavfsizligi", "lesson:internet"),
        ("🛡 Application Security", "lesson:appsec"),
        ("🖧 Networking", "lesson:network"),
        ("🐧 Linux Security", "lesson:linux"),
        ("🔬 Ethical Hacking", "lesson:ethical"),
        ("🔐 Cryptography", "lesson:crypto"),
        ("☁️ Cloud Security", "lesson:cloud"),
        ("🦠 Malware va himoyalanish", "lesson:malware"),
    ]

    for title, callback in sections:
        builder.button(text=title, callback_data=callback)

    builder.button(
        text="⬅️ Asosiy menyu",
        callback_data="main_menu",
    )

    builder.adjust(1)
    return builder.as_markup()


def back_menu() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text="⬅️ Asosiy menyu",
        callback_data="main_menu",
    )
    return builder.as_markup()