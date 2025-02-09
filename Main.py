import ctypes
import string
import os
import time
import requests
import numpy

USE_WEBHOOK = True

def check_internet():
    try:
        requests.get("https://github.com/h0mmerk1ng", timeout=5)
        return True
    except requests.exceptions.RequestException:
        return False

if not check_internet():
    input("You are not connected to the internet. Press Enter to exit.")
    exit()

class NitroGen:
    def __init__(self):
        self.codes_file = "Codes.txt"
        self.generated_codes_file = "GeneratedCodes.txt"
        self.generated_codes = set()
        
        if os.path.exists(self.generated_codes_file):
            with open(self.generated_codes_file, "r") as f:
                self.generated_codes = set(f.read().splitlines())

    def main(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        if os.name == "nt":
            ctypes.windll.kernel32.SetConsoleTitleW("Nitro Generator and Checker")
        else:
            print(f'\33]0;Nitro Generator and Checker\a', end='', flush=True)
        
        self.slowType("Made by: h0mmerk1ng", .02)
        time.sleep(1)
        
        self.slowType("\nKaç Kod Üretileceğini Girin [Sınırsız Üretim İçin 0 Yazın]:", .02, newLine=False)
        try:
            num = int(input(''))
        except ValueError:
            input("Hatalı giriş! Bir sayı girin. Enter'a basarak çıkabilirsiniz.")
            exit()
        
        if num == 0:
            self.slowType("\nKaç Doğru Kod Bulunduğunda Durdurulsun?:", .02, newLine=False)
            try:
                stop_limit = int(input(''))
            except ValueError:
                input("Hatalı giriş! Bir sayı girin. Enter'a basarak çıkabilirsiniz.")
                exit()
        else:
            stop_limit = None
        
        if USE_WEBHOOK:
            self.slowType("Discord webhook'unu girin veya boş bırakın: ", .02, newLine=False)
            webhook_url = input('').strip()
            webhook = webhook_url if webhook_url else None
        else:
            webhook = None

        valid_codes = []
        invalid_count = 0
        generated_count = 0
        chars = string.ascii_letters + string.digits

        if num == 0:
            num = 99999999
        
        while True:
            batch = numpy.random.choice(list(chars), size=[num, 16])
            for s in batch:
                code = ''.join(s)
                if code in self.generated_codes:
                    continue
                self.generated_codes.add(code)
                generated_count += 1
                
                with open(self.generated_codes_file, "a") as f:
                    f.write(code + "\n")
                
                url = f"https://discord.gift/{code}"
                if self.quickChecker(code, webhook):
                    valid_codes.append(url)
                    with open(self.codes_file, "a") as f:
                        f.write(url + "\n")
                    if webhook:
                        self.send_webhook(webhook, url)
                else:
                    invalid_count += 1
                
                os.system('cls' if os.name == 'nt' else 'clear')
                print(f"\nOluşturulan: {generated_count}  Hatalı: {invalid_count}  Başarılı: {len(valid_codes)}")
                print(f"Code: {code}")
                
                if stop_limit and len(valid_codes) >= stop_limit:
                    print(f"\n{stop_limit} doğru kod bulundu. Üretim durduruluyor...")
                    return
    
    def slowType(self, text: str, speed: float, newLine=True):
        for i in text:
            print(i, end="", flush=True)
            time.sleep(speed)
        if newLine:
            print()
    
    def quickChecker(self, nitro: str, webhook=None):
        url = f"https://discordapp.com/api/v9/entitlements/gift-codes/{nitro}?with_application=false&with_subscription_plan=true"
        response = requests.get(url)
        
        if response.status_code == 200:
            print(f" \033[92mBaşarılı | {nitro}\033[0m ", flush=True)
            return True
        else:
            print(f" \033[91mHatalı | {nitro}\033[0m ", flush=True)
            return False
        
    def send_webhook(self, webhook_url, message):
        try:
            requests.post(webhook_url, json={"content": f"Oluşturulan Promo Kodu: {message}"})
        except:
            print("Webhook gönderimi başarısız!")

if __name__ == '__main__':
    Gen = NitroGen()
    Gen.main()
