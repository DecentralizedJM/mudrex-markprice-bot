# Mudrex Mark Price Bot 📊

A Telegram bot that fetches **real-time and historical mark prices** for USDT perpetual trading pairs.

## Features

- 🔴 **Live Prices** - Get current mark prices instantly
- 📅 **Historical Prices** - Query mark prices at any past timestamp
- ⏰ **Flexible Time Formats** - Supports Unix timestamps and human-readable dates
- 💬 **Telegram Integration** - Easy-to-use bot commands

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
   Edit `.env` and add your Telegram bot token:
   ```
   TELEGRAM_BOT_TOKEN=your_bot_token_here
   ```

4. **Run the bot**
   ```bash
   python3 bot.py
   ```

## Deploy on Railway

The bot runs as a **worker** (no HTTP server). To deploy:

1. **Install Railway CLI** (optional): [railway.app](https://railway.app) → use the dashboard or `npm i -g @railway/cli` and `railway login`.

2. **Create a new project** on [Railway](https://railway.app):
   - **New Project** → **Deploy from GitHub repo** (connect your GitHub and select this repo), or **Empty Project** and then **Deploy from GitHub**.
   - Railway will detect Python from `requirements.txt` and use the **Procfile** to run `python bot.py` as a worker.

3. **Set environment variable** in the Railway project:
   - Open your service → **Variables** → **Add Variable**
   - Name: `TELEGRAM_BOT_TOKEN`
   - Value: your Telegram bot token from [@BotFather](https://t.me/botfather)

4. **Deploy**: Pushes to your connected branch will auto-deploy. Or trigger a deploy from the dashboard.

5. **Process type**: Ensure the service is run as a **worker** (Railway uses the `worker` line from the Procfile). If your plan only shows "Web", set the **Start Command** in **Settings** to `python bot.py` so it runs as the main process.

Your bot will stay running and respond to `/start` and `/mark <symbol> [timestamp]` in Telegram.

## Project Structure

```
├── bot.py                 # Main Telegram bot
├── mark_price_client.py   # API client for fetching prices
├── requirements.txt       # Python dependencies
├── .env.example           # Environment template
└── README.md              # Documentation
```

## Example Output

```
BTCUSDT Mark Price
Price: 42150.50
Time: 20/01/26 12:00:00
Type: Live
```

## License

MIT License - see [LICENSE](LICENSE) for details.
