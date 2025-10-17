import time
import os
import random
from datetime import datetime

# SMS matni (bitta qatorda)
MESSAGE_BASE = "+25 000 soʻm hisobingizda! Ulansangiz — bonus sizniki. Atigi 2% komissiya! Yandex haydovchilarini taklif qilamiz. Pulni Telegram boti orqali 100% yeching. Har qanday avtomobilni Yandex’ga ulaymiz. Batafsil: @RAYYONAA2023, +998978650526"

CHUNK_SIZE = 58  # har 58 belgidan keyin (1–9) raqam qo‘shiladi
DELAY = 5        # SMSlar orasidagi kutish (soniya)
NUMBERS_FILE = "numbers.txt"
LOG_FILE = "sent_log.txt"


def chunk_and_tag(text, index):
    """Matnni bo‘laklarga ajratib, (1–9) raqamlar qo‘shadi va oxirida tartib raqamini biriktiradi."""
    parts = []
    for i in range(0, len(text), CHUNK_SIZE):
        part = text[i:i + CHUNK_SIZE]
        tag = f" ({random.randint(1,9)})"
        parts.append(part + tag)
    return "".join(parts) + f" ({index})"


def send_sms(number, message, retries=2):
    """Termux orqali SMS yuborish, xatolik bo‘lsa qayta urinadi."""
    for attempt in range(1, retries + 1):
        result = os.system(f'termux-sms-send -n {number} "{message}"')
        if result == 0:
            return True
        else:
            print(f"⚠️  {number} raqamiga yuborishda xatolik. Urinish: {attempt}")
            time.sleep(3)
    return False


def log_sent(number, message):
    """Yuborilgan SMSni log faylga yozadi."""
    with open(LOG_FILE, "a", encoding="utf-8") as log:
        log.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {number}: {message}\n")


def remove_sent_number(number):
    """Yuborilgan raqamni fayldan o‘chiradi."""
    with open(NUMBERS_FILE, "r") as f:
        numbers = [line.strip() for line in f if line.strip()]
    numbers = [n for n in numbers if n != number]
    with open(NUMBERS_FILE, "w") as f:
        f.write("\n".join(numbers) + ("\n" if numbers else ""))


def main():
    with open(NUMBERS_FILE, "r") as f:
        numbers = [line.strip() for line in f if line.strip()]

    total = len(numbers)
    print(f"📱 Jami raqamlar: {total}\n")

    for i, num in enumerate(numbers, 1):
        message = chunk_and_tag(MESSAGE_BASE, i)
        print(f"[{i}/{total}] Yuborilmoqda: {num}")

        if send_sms(num, message):
            print(f"✅ Yuborildi: {num}")
            log_sent(num, message)
            remove_sent_number(num)
        else:
            print(f"❌ {num} raqamiga yuborilmadi.")

        time.sleep(DELAY)

    print("\n✅ Barcha SMSlar yuborildi yoki qayta urinildi.")


if __name__ == "__main__":
    main()
