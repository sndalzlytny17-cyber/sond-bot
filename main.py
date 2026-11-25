import os, asyncio, yfinance as yf
from telegram import Bot

TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

bot = Bot(token=TOKEN)

PAIRS = {
    "XAUUSD - ذهب": "GC=F",
    "EURUSD": "EURUSD=X",
    "GBPUSD": "GBPUSD=X"
}

async def check_pair(name, symbol):
    try:
        df = yf.download(symbol, period="1d", interval="15m", progress=False)
        if len(df) < 25:
            return
        close = float(df['Close'].iloc[-1].iloc[0] if hasattr(df['Close'].iloc[-1], 'iloc') else df['Close'].iloc[-1])
        low = float(df['Low'].iloc[-2])
        high = float(df['High'].iloc[-2])
        prev_low = float(df['Low'].iloc[-25:-2].min())
        prev_high = float(df['High'].iloc[-25:-2].max())

        if low <= prev_low and close > prev_low:
            msg = f"🔥 اشارة ICT - {name}\n\n✅ شراء من: {close:.2f}\n🛑 ستوب: {prev_low:.2f}\n🎯 هدف: {close + (close-prev_low)*2:.2f}\n\nالسبب: سحب سيولة من القاع + رجوع"
            await bot.send_message(chat_id=CHAT_ID, text=msg)
        elif high >= prev_high and close < prev_high:
            msg = f"🔥 اشارة ICT - {name}\n\n✅ بيع من: {close:.2f}\n🛑 ستوب: {prev_high:.2f}\n🎯 هدف: {close - (prev_high-close)*2:.2f}\n\nالسبب: سحب سيولة من القمة + رجوع"
            await bot.send_message(chat_id=CHAT_ID, text=msg)
    except Exception as e:
        print(f"Error {name}: {e}")

async def main():
    await bot.send_message(chat_id=CHAT_ID, text="✅ البوت اشتغل! نراقب في الذهب + EURUSD + GBPUSD بنظام ICT")
    while True:
        for name, sym in PAIRS.items():
            await check_pair(name, sym)
        await asyncio.sleep(900)

asyncio.run(main())
