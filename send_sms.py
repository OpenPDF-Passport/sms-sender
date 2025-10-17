import time
import os
import random

MESSAGE_BASE = (
    "Yandex Haydovchilarni taklif qilamiz Komisya 2%. 25000 bonus beriladi."
    " Pul yechsh foyzsz t/g bot bn -20000gacha limit qiberamz...."
    " Blok bo'lsangiz. Har qanday Avtomoblni Yandexga ulaymiz."
    " Yandexga oid har qanday turdagi muamolar bo'yicha Yordamlashamz."
    " Ish jarayoningizda @RAYYONAA2023, +998978650526"
)
DELAY = 5  # soniya
NUMBERS_FILE = "numbers.txt"

def send_sms(number, message):
    os.system(f'termux-sms-send -n {number} "{message}"')

def main():
    with open(NUMBERS_FILE, 'r') as f:
        numbers = [line.strip() for line in f if line.strip()]

    for i, num in enumerate(numbers, 1):
        # 1–9 oralig‘ida tasodifiy raqam
        rand_num = random.randint(1, 9)
        # Har bir xabarni ozgina o‘zgartirish
        message = f"{MESSAGE_BASE} ({rand_num})"
        print(f"[{i}] Yuborilmoqda: {num} | Xabar raqami: ({rand_num})")
        send_sms(num, message)
        time.sleep(DELAY)

if __name__ == "__main__":
    main()

