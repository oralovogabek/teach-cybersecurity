import ipaddress
from urllib.parse import urlsplit


SUSPICIOUS_WORDS = (
    "login",
    "verify",
    "password",
    "account",
    "wallet",
    "telegram",
    "secure",
)


def analyze_url(raw_url: str) -> dict:
    raw_url = raw_url.strip()

    if not raw_url or len(raw_url) > 2048:
        return {
            "valid": False,
            "message": "Havola bo‘sh yoki juda uzun.",
            "warnings": [],
        }

    if any(ord(char) < 32 for char in raw_url):
        return {
            "valid": False,
            "message": "Havolada ruxsat etilmagan belgilar mavjud.",
            "warnings": [],
        }

    try:
        parsed = urlsplit(raw_url)

        if parsed.scheme.lower() not in ("http", "https"):
            raise ValueError("Faqat HTTP yoki HTTPS havolalar qabul qilinadi.")

        if not parsed.hostname:
            raise ValueError("Domen nomi topilmadi.")

        host = parsed.hostname.rstrip(".").lower()

        # Port noto‘g‘ri berilgan holatlarni ham tekshirish.
        _ = parsed.port

        if not host or any(char.isspace() for char in host):
            raise ValueError("Domen formati noto‘g‘ri.")

    except ValueError as exc:
        return {
            "valid": False,
            "message": f"Havola formati noto‘g‘ri: {exc}",
            "warnings": [],
        }

    warnings = []

    if parsed.scheme.lower() == "http":
        warnings.append(
            "HTTPS yo‘q: ulanish shifrlanmagan bo‘lishi mumkin."
        )

    if parsed.username is not None or parsed.password is not None:
        warnings.append(
            "Havolada @ belgisi orqali yashirilgan manzil bo‘lishi mumkin."
        )

    try:
        ipaddress.ip_address(host)
        warnings.append(
            "Domen o‘rniga IP manzil ishlatilgan. "
            "Bu o‘z-o‘zidan zararli degani emas."
        )
    except ValueError:
        pass

    if host.startswith("xn--") or ".xn--" in host:
        warnings.append(
            "Domen xalqaro belgilarni kodlash shaklida yozilgan. "
            "Ko‘rinishi o‘xshash belgilarni tekshiring."
        )

    if host.count(".") >= 4:
        warnings.append(
            "Domen ko‘p darajali. Asosiy domenni diqqat bilan tekshiring."
        )

    full_url = raw_url.lower()

    if any(word in full_url for word in SUSPICIOUS_WORDS):
        warnings.append(
            "Havolada login yoki tasdiqlash bilan bog‘liq so‘zlar bor. "
            "Bu faqat tekshirish kerak bo‘lgan belgi."
        )

    if not warnings:
        warnings.append(
            "Oddiy tekshiruvda aniq ogohlantiruvchi belgi topilmadi. "
            "Bu havola xavfsizligini kafolatlamaydi."
        )

    return {
        "valid": True,
        "host": host,
        "scheme": parsed.scheme.lower(),
        "warnings": warnings,
    }