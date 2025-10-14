import time
import os

MESSAGE = "Yandex Haydovchilarni taklif qilamiz Komisya 2%. 25000 bonus beriladi.Pul yechsh foyzsz t/g bot bn -20000gacha limit   qiberamz....Blok bo'lsangiz. Har qanday Avtomoblni  Yandexga ulaymiz Yandexga oid har qanday turdagi muamolar bo'yicha  Yordamlashamz  ish jarayonzda @RAYYONAA2023+998978650526"
DELAY = 2  # секунд
NUMBERS_FILE = "numbers.txt"

def send_sms(number):
    os.system(f'termux-sms-send -n {number} "{MESSAGE}"')

def main():
    with open(NUMBERS_FILE, 'r') as f:
        numbers = [line.strip() for line in f if line.strip()]

    for i, num in enumerate(numbers, 1):
        print(f"[{i}] Юбориляпти: {num}")
        send_sms(num)
        time.sleep(DELAY)

if __name__ == "__main__":
    main()
