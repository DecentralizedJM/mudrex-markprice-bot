import os
import logging
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
from mark_price_client import MarkPriceClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

mark_price_client = MarkPriceClient()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="I'm a Mark Price Bot. Use /mark <symbol> [timestamp] to get prices."
    )

async def mark(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    if not args:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Asset is missed. Usage: /mark <symbol> [timestamp] (e.g., /mark BTCUSDT)"
        )
        return

    symbol = args[0].upper()
    
    # Simple check for likely incomplete symbols (e.g. "BTC" instead of "BTCUSDT")
    if len(symbol) < 5 or "USDT" not in symbol:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"Invalid format for '{symbol}'. Please use the full symbol format, e.g., BTCUSDT."
        )
        return

    timestamp = None
    
    if len(args) > 1:
        # Join remaining args to handle cases like "24/12/22 14:30" which might be split
        input_time = " ".join(args[1:])
        
        try:
            # Try parsing as Unix timestamp
            timestamp = int(input_time)
        except ValueError:
            # Try various date string formats
            formats = ["%d/%m/%y %H:%M", "%d/%m/%y"]
            dt = None
            for fmt in formats:
                try:
                    dt = datetime.strptime(input_time, fmt)
                    break
                except ValueError:
                    continue
            
            if dt:
                timestamp = int(dt.timestamp())
            else:
                await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text="Invalid timestamp format. Use Unix timestamp, 'DD/MM/YY HH:MM', or 'DD/MM/YY'."
                )
                return

    try:
        data = mark_price_client.get_mark_price(symbol, timestamp)
        
        if "error" in data:
            error_msg = data['error']
            if "invalid" in error_msg.lower() or "symbol" in error_msg.lower():
                 await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text=f"Error: {error_msg}. Please check the symbol format (e.g., BTCUSDT)."
                )
            else:
                await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text=f"Error: {error_msg}"
                )
        else:
            time_str = "Live" if not data['is_historical'] else "Historical"
            ts = data['timestamp']
            fmt = "%d/%m/%y %H:%M:%S"
            dt_ist = datetime.fromtimestamp(ts, tz=ZoneInfo("Asia/Kolkata")).strftime(fmt)
            dt_utc = datetime.fromtimestamp(ts, tz=timezone.utc).strftime(fmt)

            vol_str = f"Volume: `{data['volume']}`" if data.get('volume') is not None else "Volume: —"
            msg = (
                f"*{data['symbol']} Mark Price* _(1m candle)_\n"
                f"Open: `{data['open']}`\n"
                f"High: `{data['high']}`\n"
                f"Low: `{data['low']}`\n"
                f"Close: `{data['close']}`\n"
                f"{vol_str}\n"
                f"Time (IST): `{dt_ist}`\n"
                f"Time (UTC / Railway): `{dt_utc}`\n"
                f"Type: {time_str}\n"
                f"_Bybit linear mark-price._"
            )
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=msg,
                parse_mode='Markdown'
            )

    except Exception as e:
        logging.error(f"Error handling /mark command: {e}")
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="An internal error occurred."
        )

if __name__ == '__main__':
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        print("Error: TELEGRAM_BOT_TOKEN not found in environment variables.")
        exit(1)

    # Long timeouts for Railway: outbound to api.telegram.org (bootstrap + set_webhook) can be slow
    application = (
        ApplicationBuilder()
        .token(token)
        .connect_timeout(90.0)
        .read_timeout(90.0)
        .write_timeout(90.0)
        .get_updates_connect_timeout(90.0)
        .get_updates_read_timeout(90.0)
        .get_updates_write_timeout(90.0)
        .build()
    )

    start_handler = CommandHandler('start', start)
    mark_handler = CommandHandler('mark', mark)

    application.add_handler(start_handler)
    application.add_handler(mark_handler)

    webhook_base = os.getenv("WEBHOOK_BASE_URL", "").strip().rstrip("/")
    if webhook_base:
        if not webhook_base.startswith(("http://", "https://")):
            webhook_base = f"https://{webhook_base}"
        # Webhook mode: Telegram pushes to us. No outbound connection to Telegram needed.
        port = int(os.getenv("PORT", "8080"))
        url_path = "webhook"
        webhook_url = f"{webhook_base}/{url_path}"
        print(f"Starting webhook: listen 0.0.0.0:{port}, url={webhook_url}")
        application.run_webhook(
            listen="0.0.0.0",
            port=port,
            url_path=url_path,
            webhook_url=webhook_url,
            bootstrap_retries=15,
        )
    else:
        print("Bot is polling...")
        application.run_polling(bootstrap_retries=5)
