import time
import os
import random

# Qisqa, e’tiborli SMS matni
MESSAGE_BASE = "+25 000 soʻm hisobingizda! Ulansangiz — bonus sizniki. Atigi 2% komissiya! Yandex haydovchilarini taklif qilamiz. Pulni Telegram boti orqali 100% yeching. Har qanday avtomobilni Yandex’ga ulaymiz. Batafsil: @RAYYONAA2023, +998978650526"

CHUNK_SIZE = 58  # har 58 ta belgidan keyin (raqam) bo'lishi kerak
DELAY = 5        # SMSlar orasidagi kutish vaqti (soniya)
NUMBERS_FILE = "numbers.txt"

def chunk_and_tag(text, chunk_size=CHUNK_SIZE):
    """Matnni har 58 belgidan bo‘lib, oxiriga (1–9) raqam qo‘shadi."""
    parts = []
    for i in range(0, len(text), chunk_size):
        part = text[i:i + chunk_size]
        tag = f" ({random.randint(1,9)})"
        parts.append(part + tag)
    return "".join(parts)

def send_sms(number, message):
    """Termux orqali SMS yuborish"""
    os.system(f'termux-sms-send -n {number} "{message}"')

def main():
    # Fayldan raqamlarni o‘qish
    with open(NUMBERS_FILE, 'r') as f:
        numbers = [line.strip() for line in f if line.strip()]

    for i, num in enumerate(numbers, 1):
        message = chunk_and_tag(MESSAGE_BASE)
        print(f"[{i}] Yuborilmoqda: {num} | Uzunlik: {len(message)} belgi")
        send_sms(num, message)
        time.sleep(DELAY)

if __name__ == "__main__":
    main()
