import time
import os
import random
from datetime import datetime, timedelta

# 10 xil variantdagi xabarlar
MESSAGES = [
    """💸 +25 000 so'm bonus!
Ulaning — bonus sizniki. Komissiya atigi 2%.
🚗 Yandex haydovchilarini taklif qilamiz!
Pulni Telegram bot orqali 100% yeching.
Yandexdagi muammolarga yordam beramiz.
Har qanday mashinani Yandexga ulaymiz.
🛡 Sug'urta 40% chegirmada!
📩 Telegram: @Yandex20212025 | ☎️ +998903350526""",

    """🎁 Hisobingizda +25 000 so'm!
Yandexga ulaning — bonus sizniki.
💰 Komissiya — atigi 2%.
Pulni Telegram bot orqali yeching.
Yandexdagi muammolarga yordam beramiz.
🚘 Har qanday avtomobilni ulanadi.
🛡 Sug'urta 40% chegirmada!
📞 @Yandex20212025 | +998903350526""",

    """🔥 25 000 so'm bonus oling!
Ulansangiz, bonus sizga.
Komissiya — 2% xolos.
Pulni Telegram botdan 100% yeching.
🧰 Yandexdagi muammolarga yordam beramiz.
🚗 Har qanday mashinani ulaymiz.
Sug'urta — 40% chegirma bilan!
📲 @Yandex20212025 | +998903350526""",

    """💰 Yandex haydovchilariga sovg'a — 25 000 so'm!
Ulaning va bonusni oling.
Komissiya atigi 2%.
Pulni Telegram bot orqali yeching.
Yandex muammolariga yordam beramiz.
🚘 Har qanday mashinani ulanadi.
🛡 Sug'urta 40% arzon.
📩 @Yandex20212025 | +998903350526""",

    """🚖 +25 000 so'm bonus hisobingizda!
Ulaning — sizniki.
Komissiya — faqat 2%.
Pulni Telegram bot orqali 100% yeching.
Yandexdagi har qanday muammoga yordam beramiz.
Har qanday mashinani Yandexga ulaymiz.
🛡 Sug'urta — 40% chegirma.
📞 @Yandex20212025 | +998903350526""",

    """🎯 Yandex haydovchilari uchun bonus!
💸 +25 000 so'm hisobingizda.
Komissiya 2% dan oshmaydi.
Pulni Telegram bot orqali oson yeching.
🚗 Mashinangizni Yandexga ulaymiz.
🧩 Muammolarga yordam beramiz.
Sug'urta 40% chegirmada!
📲 @Yandex20212025 | +998903350526""",

    """💵 Hisobingizga +25 000 so'm tushadi!
Yandexga ulanib bonus oling.
Komissiya — 2%.
Pulni Telegram bot orqali 100% yeching.
Yandex muammolarini hal qilamiz.
Har qanday avtomobilni ulaymiz.
🛡 Sug'urta 40% arzon.
📩 @Yandex20212025 | +998903350526""",

    """🚗 Yandex haydovchilari uchun maxsus taklif!
💰 +25 000 so'm bonus sizga.
Komissiya atigi 2%.
Pulni Telegram bot orqali yeching.
Yandexdagi muammolarga yordam beramiz.
Har qanday mashinani ulaymiz.
🛡 Sug'urta 40% chegirmada.
📞 @Yandex20212025 | +998903350526""",

    """🔥 25 000 so'm bonus oling!
Ulaning — bonus sizniki.
Komissiya — 2% xolos.
Pulni Telegram bot orqali 100% yeching.
🚘 Yandexdagi muammolarga yordam beramiz.
Har qanday avtomobilni ulaymiz.
🛡 Sug'urta 40% arzon.
📲 @Yandex20212025 | +998903350526""",

    """💸 Yandex bilan boshlang — +25 000 so'm bonus!
Ulaning va oling. Komissiya — 2%.
Pulni Telegram bot orqali oson yeching.
🧩 Yandexga oid muammolarga yordam beramiz.
🚗 Har qanday mashinani ulanadi.
🛡 Sug'urta 40% chegirma bilan!
📩 @Yandex20212025 | +998903350526"""
]

TOTAL_USERS = 200           # Jami foydalanuvchilar soni
TOTAL_DURATION = 10 * 3600  # 10 soat (sekundlarda)
MIN_DELAY = 3 * 60          # 3 daqiqa (sekundlarda)
MAX_DELAY = 4 * 60          # 4 daqiqa (sekundlarda)
NUMBERS_FILE = "numbers.txt"
LOG_FILE = "sent_log.txt"


def prepare_message(text, index):
    """Matnni SMS uchun tayyorlaydi (bo'linmasdan)."""
    return f"{text} ({index})"


def send_sms(number, message, retries=2):
    """Termux orqali SMS yuborish, xatolik bo'lsa qayta urinadi."""
    for attempt in range(1, retries + 1):
        result = os.system(f'termux-sms-send -n {number} "{message}"')
        if result == 0:
            return True
        else:
            print(f"⚠️  {number} raqamiga yuborishda xatolik. Urinish: {attempt}")
            time.sleep(3)
    return False


def log_sent(number, message, message_type):
    """Yuborilgan SMSni log faylga yozadi."""
    with open(LOG_FILE, "a", encoding="utf-8") as log:
        log.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {number} (Variant {message_type + 1}): {message}\n")


def remove_sent_number(number):
    """Yuborilgan raqamni fayldan o'chiradi."""
    with open(NUMBERS_FILE, "r") as f:
        numbers = [line.strip() for line in f if line.strip()]
    numbers = [n for n in numbers if n != number]
    with open(NUMBERS_FILE, "w") as f:
        f.write("\n".join(numbers) + ("\n" if numbers else ""))


def calculate_dynamic_delay(remaining_users, remaining_time):
    """Qolgan vaqt va foydalanuvchilar asosida dinamik kechikishni hisoblaydi."""
    if remaining_users <= 0:
        return MIN_DELAY
    
    # Har bir SMS uchun o'rtacha vaqt
    avg_delay_per_sms = remaining_time / remaining_users
    
    # 3-4 daqiqa oralig'ida bo'lishini ta'minlaymiz
    if avg_delay_per_sms < MIN_DELAY:
        return MIN_DELAY
    elif avg_delay_per_sms > MAX_DELAY:
        return MAX_DELAY
    else:
        return avg_delay_per_sms


def main():
    with open(NUMBERS_FILE, "r") as f:
        numbers = [line.strip() for line in f if line.strip()]

    total_numbers = len(numbers)
    
    if total_numbers < TOTAL_USERS:
        print(f"⚠️  Diqqat: Faylda {total_numbers} ta raqam mavjud, {TOTAL_USERS} ta kerak")
        return

    # Faqat birinchi 200 ta raqamni olamiz
    numbers = numbers[:TOTAL_USERS]
    total = len(numbers)
    
    print(f"📱 Jami raqamlar: {total}")
    print(f"📝 Xabar variantlari: {len(MESSAGES)} ta")
    print(f"⏰ Davomiylik: 10 soat")
    print(f"⏱️  Kechikish: 3-4 daqiqa oralig'ida")
    print(f"🚀 Boshlanadi...\n")

    start_time = datetime.now()
    end_time = start_time + timedelta(seconds=TOTAL_DURATION)

    for i, num in enumerate(numbers, 1):
        current_time = datetime.now()
        
        # Agar vaqt tugagan bo'lsa, to'xtatamiz
        if current_time >= end_time:
            print(f"⏰ Vaqt tugadi! {i-1}/{total} ta SMS yuborildi.")
            break

        # Qolgan vaqt va foydalanuvchilar
        remaining_time = (end_time - current_time).total_seconds()
        remaining_users = total - i + 1
        
        # Dinamik kechikishni hisoblash
        delay = calculate_dynamic_delay(remaining_users, remaining_time)
        # Tasodifiy kechikish (3-4 daqiqa oralig'ida)
        random_delay = random.uniform(MIN_DELAY, MAX_DELAY)
        
        # Har bir raqam uchun tasodifiy xabar tanlash
        message_type = random.randint(0, len(MESSAGES) - 1)
        message_base = MESSAGES[message_type]
        message = prepare_message(message_base, i)
        
        print(f"[{i}/{total}] Yuborilmoqda: {num}")
        print(f"📨 Xabar varianti: {message_type + 1}")
        print(f"📄 Xabar uzunligi: {len(message)} belgi")
        print(f"⏱️  Kechikish: {random_delay/60:.1f} daqiqa")
        print(f"🕐 Qolgan vaqt: {remaining_time/3600:.1f} soat")

        if send_sms(num, message):
            print(f"✅ Yuborildi: {num} (Variant {message_type + 1})")
            log_sent(num, message, message_type)
            remove_sent_number(num)
        else:
            print(f"❌ {num} raqamiga yuborilmadi.")

        print("-" * 50)
        
        # Keyingi SMS dan oldin kutish
        if i < total:  # Oxirgi SMS dan keyin kutmaymiz
            time.sleep(random_delay)

    total_time = (datetime.now() - start_time).total_seconds()
    print(f"\n✅ Yakunlandi!")
    print(f"📊 Yuborilgan SMS: {total} ta")
    print(f"⏰ Sarflangan vaqt: {total_time/3600:.1f} soat")
    print(f"📈 O'rtacha tezlik: {total_time/total/60:.1f} daqiqa/SMS")


if __name__ == "__main__":
    main()

