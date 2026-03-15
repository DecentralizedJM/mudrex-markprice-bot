# Mudrex Mark Price Bot 📊

A Telegram bot that fetches **real-time and historical mark prices** for USDT perpetual trading pairs (Bybit linear).

## Features

- 🔴 **Live prices** – Current 1‑minute mark-price candle (OHLC + volume)
- 📅 **Historical prices** – Mark price for any past minute
- 📊 **OHLC + volume** – Open, High, Low, Close (mark price) and trading volume for that minute
- 🕐 **Dual time display** – Time shown in **IST** and **UTC** (Railway/server time)
- ⏰ **Flexible time formats** – Unix timestamp or `DD/MM/YY` / `DD/MM/YY HH:MM`
- 💬 **Telegram** – `/start` and `/mark` commands; webhook mode for Railway

## Commands

| Command | Description | Example |
|---------|-------------|---------|
| `/start` | Display help message | `/start` |
| `/mark <symbol>` | Get live mark price | `/mark BTCUSDT` |
| `/mark <symbol> <timestamp>` | Get historical mark price | `/mark ETHUSDT 20/01/26 12:00` |

### Timestamp Formats

- Unix timestamp: `1705747200`
- Date with time: `DD/MM/YY HH:MM` (e.g., `20/01/26 12:00`)
- Date only: `DD/MM/YY` (e.g., `20/01/26`)

## Setup

### Prerequisites

- Python 3.8+
- Telegram Bot Token (get from [@BotFather](https://t.me/botfather))

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/DecentralizedJM/mudrex-markprice-bot.git
   cd mudrex-markprice-bot
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment**
   ```bash
   cp .env.example .env
   ```
   Edit `.env`:
   - `TELEGRAM_BOT_TOKEN` – required (from [@BotFather](https://t.me/botfather))
   - `WEBHOOK_BASE_URL` – optional; only for webhook mode (e.g. on Railway). Omit for local polling.

4. **Run the bot**
   ```bash
   python3 bot.py
   ```
   Without `WEBHOOK_BASE_URL` it runs in **polling** mode (fine for local). With `WEBHOOK_BASE_URL` it runs in **webhook** mode (needed on Railway).

## Deploy on Railway (webhook mode)

The bot uses **webhook mode** on Railway so Telegram pushes updates to your app (no outbound connection to Telegram = no timeouts).

1. **Create a project** on [Railway](https://railway.app): **New Project** → **Deploy from GitHub repo** (select this repo). Railway will use the Procfile and run the app as a **web** service.

2. **Get your public URL**: In the Railway dashboard, open your service → **Settings** → **Networking** → **Generate Domain** (or use the default). Copy the URL (e.g. `https://mudrex-markprice-bot-production.up.railway.app`).

3. **Set environment variables** (service → **Variables**):
   - `TELEGRAM_BOT_TOKEN` = your bot token from [@BotFather](https://t.me/botfather)
   - `WEBHOOK_BASE_URL` = your Railway public URL from step 2 (e.g. `https://your-app.up.railway.app`) — **no trailing slash**

4. **Deploy**: Push to your branch or trigger a deploy. The bot will listen on `PORT`, register the webhook with Telegram, and receive updates at `/webhook`.

Without `WEBHOOK_BASE_URL` the bot falls back to polling (works locally; on Railway polling often times out).

## Project Structure

```
├── bot.py                 # Telegram bot (polling or webhook)
├── mark_price_client.py   # Bybit API: mark-price kline + kline for volume
├── requirements.txt       # Python dependencies (PTB with webhooks extra)
├── Procfile               # web: python bot.py (Railway)
├── runtime.txt            # Python version
├── .env.example           # TELEGRAM_BOT_TOKEN, optional WEBHOOK_BASE_URL
└── README.md              # This file
```

## Example Output

```
BTCUSDT Mark Price (1m candle)
Open: 97500.50
High: 97580.20
Low: 97490.10
Close: 97545.30
Volume: 1234.56
Time (IST): 15/03/26 20:02:00
Time (UTC / Railway): 15/03/26 14:32:00
Type: Live
Bybit linear mark-price.
```

- **OHLC** from Bybit mark-price kline; **Volume** from Bybit regular kline (same minute).
- **IST** = Indian Standard Time; **UTC** = server/Railway time.

## License

MIT License - see [LICENSE](LICENSE) for details.
