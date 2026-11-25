import os, asyncio, yfinance as yf
from telegram import Bot
from flask import Flask
import threading

TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
bot = Bot(token=TOKEN)

app = Flask(__name__)
@app.route('/')
def home():
    return "Bot is running!"

PAIRS = {
    "XAUUSD - ذهب": "GC=F",
    "EURUSD": "EURUSD=X",
    "GBPUSD": "GBPUSD=X"
}

async def check_pair(name, symbol):
    try:
        df = yf.download(symbol, period="3d", interval="15m", progress=False)
        if len(df) < 25:
            return
        close = float(df['Close'].iloc[-1])
        low = float(df['Low'].iloc[-2])
        high = float(df['High'].iloc[-2])
        prev_low = float(df['Low'].iloc[-3])
        prev_high = float(df['High'].iloc[-3])
        msg = None
        if close > high and low > prev_low:
            msg = f"🚀 كسر صاعد {name}\nالسعر: {close:.4f}\nدخول شراء"
        elif close < low and high < prev_high:
            msg = f"🔻 كسر هابط {name}\nالسعر: {close:.4f}\nدخول بيع"
        if msg:
            await bot.send_message(chat_id=CHAT_ID, text=msg)
    except Exception as e:
        print(e)

async def loop():
    while True:
        for name, sym in PAIRS.items():
            await check_pair(name, sym)
        await asyncio.sleep(60)

def run_bot():
    asyncio.run(loop())

if __name__ == "__main__":
    threading.Thread(target=run_bot, daemon=True).start()
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
