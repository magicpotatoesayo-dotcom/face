# -*- coding: utf-8 -*-

import requests
import random
import time
import os
import sys
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler

# ══════════════════════════════════════════════════════════════
#   🎨 الألوان
# ══════════════════════════════════════════════════════════════
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
CYAN = '\033[96m'
WHITE = '\033[1;97m'
RESET = '\033[0m'
BOLD = '\033[1m'

# ══════════════════════════════════════════════════════════════
#   ⚙️ الإعدادات
# ══════════════════════════════════════════════════════════════
CUSTOM_IMAGE = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQRCAq2eMxJrJjF7NhN9xvACUqpXJSU47xoHg&s"


# ══════════════════════════════════════════════════════════════
#   🩺 Health check server (for Render Web Service)
# ══════════════════════════════════════════════════════════════
class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(b'{"status":"alive"}')

    def log_message(self, format, *args):
        pass


def start_health_server():
    port = int(os.environ.get('PORT', 10000))
    server = HTTPServer(('0.0.0.0', port), HealthHandler)
    server.serve_forever()


# ══════════════════════════════════════════════════════════════
#   🎭 صورة Anonymous
# ══════════════════════════════════════════════════════════════
def show_mask():
    mask = r"""
⣿⣿⣿⣿⣿⣿⡿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⠟⠡⠶⣎⠤⠤⠤⡸⣫⡝⠛⠏⠹⠩⠍⠫⢝⡶⢄⡈⠙⣿⣿⣿
⣿⣿⣿⡏⠀⠀⠊⠀⠀⠀⠀⠑⠂⠓⠁⠀⠀⠀⠀⠀⠈⠚⠄⡄⢸⣿⣿
⣿⡿⠋⡀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡀⠀⠀⠀⠀⠀⠀⠀⠂⠀⢻⣿
⡿⠁⡜⠀⠉⠐⠀⠀⠀⠀⠠⣤⣾⣿⣅⣤⠀⠀⠀⣀⠤⠒⠒⠲⠄⠊⢿
⡇⢰⠀⠀⠀⠀⠀⣀⡐⠒⠀⠒⠈⠻⠟⠃⠀⠂⠀⢀⡀⡀⠄⠀⠀⠀⠘⡔⢸
⣿⡌⢆⠀⠀⠀⠀⠙⠺⣶⣤⣾⣶⢠⣿⣦⣿⣏⠏⠁⠀⠀⠀⠀⢀⠇⣼
⣿⣿⣮⡑⠠⠠⠀⠀⠀⠀⠁⠀⠀⠄⠰⠐⠄⠲⠈⠀⠀⠀⠀⠀⠠⠀⠬⣳⣿
⣿⣿⣿⣷⡄⠐⠑⢆⡄⠀⠁⠰⠤⣤⢠⢠⢀⡤⠊⠀⠀⣠⠄⠀⠠⣼⣿⣿
⣿⣿⣿⣿⣿⣆⠑⢄⢘⡆⢠⢠⢠⢤⣤⣤⣤⢠⠆⢢⡿⡇⠀⣰⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣇⠐⡷⡘⣄⠀⠘⠿⠘⠛⠙⠀⡰⢞⡤⢀⣼⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣷⡉⣷⢙⢦⣀⣀⣀⣀⣀⡔⢣⠏⢀⣾⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣄⠿⣵⡿⠿⠛⠛⣓⣷⠎⠊⣾⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣙⣿⣷⣶⣿⣿⠋⣠⣾⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣯⣭⣿⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
"""
    print(f"\033[1;31m{mask}\033[0m")


def print_slow(text, delay=0.02, color=GREEN):
    for ch in text:
        sys.stdout.write(f"{color}{ch}{RESET}")
        sys.stdout.flush()
        time.sleep(delay)
    print()


def show_intro():
    os.system('clear' if os.name == 'posix' else 'cls')
    show_mask()
    print()
    print(f"{YELLOW}              ⚡ TWITTER HUNTER ⚡{RESET}")
    print(f"{GREEN}                    المالك @o1_rt2 علش {RESET}")
    print()
    print_slow("   [+] جاري تهيئة النظام ...", 0.03)
    time.sleep(0.4)
    print_slow("   [+] الاتصال بالسيرفر ...", 0.03)
    time.sleep(0.4)
    print_slow("   [+] تحميل الأدوات ...", 0.03)
    time.sleep(0.4)
    print_slow("   [+] تشغيل الأداة ...", 0.03)
    time.sleep(0.8)
    print()


# ══════════════════════════════════════════════════════════════
#   📤 إرسال تيليجرام
# ══════════════════════════════════════════════════════════════
def send_message(token, chat_id, text):
    try:
        requests.post(
            f"https://api.telegram.org/bot{token}/sendMessage",
            json={"chat_id": chat_id, "text": text, "parse_mode": "HTML"},
            timeout=15
        )
    except:
        pass


def send_photo(token, chat_id, photo_url, caption=""):
    try:
        requests.post(
            f"https://api.telegram.org/bot{token}/sendPhoto",
            json={
                "chat_id": chat_id,
                "photo": photo_url,
                "caption": caption,
                "parse_mode": "HTML"
            },
            timeout=20
        )
    except:
        pass


# ══════════════════════════════════════════════════════════════
#   🎬 رسالة الترحيب
# ══════════════════════════════════════════════════════════════
def send_welcome(token, chat_id):
    welcome = """
<b>⚡ مرحباً بك ⚡</b>

───────────────────────
<b>⏳ وسيبدأ الصيد بعد قليل...</b>
"""
    send_photo(token, chat_id, CUSTOM_IMAGE, welcome)


# ══════════════════════════════════════════════════════════════
#   🎯 إرسال صيد
# ══════════════════════════════════════════════════════════════
def send_hit(token, chat_id, email, count_ok, count_bad):
    hit_text = f"""
<b>🎯 تم صيد حساب من علش @o1_rt2!</b>

───────────────────────
📧 <b>الإيميل:</b> <code>{email}</code>
📱 <b>النوع:</b> Twitter (X)
🆔 <b>الحالة:</b> مسجل ✓
───────────────────────
✅ <b>OK:</b> {count_ok}
❌ <b>BAD:</b> {count_bad}
───────────────────────
@o1_rt2 https://t.me/alu185 
https://t.me/usgu2 """
    send_photo(token, chat_id, CUSTOM_IMAGE, hit_text)


# ══════════════════════════════════════════════════════════════
#   🚀 الأداة الرئيسية
# ══════════════════════════════════════════════════════════════
def main():
    show_intro()

    print(f"{CYAN}{'═' * 55}{RESET}")
    print(f"{WHITE}{BOLD}       ⚡ إعدادات الأداة ⚡{RESET}")
    print(f"{CYAN}{'═' * 55}{RESET}")
    print()

    # Pull from environment first, fall back to input for local runs
    token = os.environ.get('BOT_TOKEN', '').strip()
    if not token:
        try:
            token = input(f"{YELLOW}[?] أدخل توكن البوت: {WHITE}").strip()
        except EOFError:
            token = ''
    if not token:
        print(f"{RED}[!] التوكن مطلوب!{RESET}")
        sys.exit(1)

    chat_id = os.environ.get('CHAT_ID', '').strip()
    if not chat_id:
        try:
            chat_id = input(f"{YELLOW}[?] أدخل آيدي الدردشة: {WHITE}").strip()
        except EOFError:
            chat_id = ''
    if not chat_id:
        print(f"{RED}[!] الآيدي مطلوب!{RESET}")
        sys.exit(1)

    print()
    print(f"{CYAN}{'═' * 55}{RESET}")
    print(f"{GREEN}[+] جاري إرسال رسالة الترحيب...{RESET}")

    send_welcome(token, chat_id)
    print(f"{GREEN}[+] تم الإرسال بنجاح!{RESET}")
    time.sleep(1.5)

    print()
    print(f"{CYAN}{'═' * 55}{RESET}")
    print(f"{GREEN}[+] بدء صيد تويتر (Twitter/X)...{RESET}")
    print(f"{CYAN}{'═' * 55}{RESET}")
    print()

    ok = 0
    bad = 0
    oo = ""
    aa = '@yopmail.com'

    def gen_random():
        nonlocal oo
        uu = 'qwertyuiopasdfghjklzxcvbnm'
        vv = ''.join(random.choices(uu, k=3))
        oo = vv

    while True:
        try:
            gen_random()
            email = oo + aa

            url = "https://api.x.com/i/users/email_available.json"
            params = {"email": email}
            headers = {
                "accept": "*/*",
                "origin": "https://x.com",
                "referer": "https://x.com/",
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            }

            re = requests.get(url, params=params, headers=headers, timeout=20)

            if '"taken":true' in re.text:
                ok += 1
                print(f'{RED}bad: {bad}{RESET} | {GREEN}ok: {ok}{RESET}  {GREEN}:{email}{RESET}')

                with open('R.ok.txt', 'a', encoding='utf-8') as tle:
                    tle.write(f'{email}\n')

                send_hit(token, chat_id, email, ok, bad)

            else:
                bad += 1
                print(f'{RED}bad: {bad}{RESET} | {GREEN}ok: {ok}{RESET}  {RED}:{email}{RESET}')

            time.sleep(0.3)

        except KeyboardInterrupt:
            print(f"\n{RED}[!] تم الإيقاف{RESET}")
            break
        except Exception:
            time.sleep(2)
            continue


if __name__ == '__main__':
    # Start the health check server thread for Render
    threading.Thread(target=start_health_server, daemon=True).start()
    main()
