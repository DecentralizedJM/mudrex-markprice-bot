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
