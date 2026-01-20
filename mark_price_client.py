import requests
import time
from typing import Optional, Dict, Any

class MarkPriceClient:
    """Client to fetch mark prices from exchange API."""
    BASE_URL = "https://api.bybit.com"

    def __init__(self):
        pass

    def get_mark_price(self, symbol: str, timestamp: Optional[int] = None) -> Dict[str, Any]:
        """
        Fetches the mark price for a given symbol.
        If timestamp is provided, fetches the closest candle to that timestamp.
        Otherwise, fetches the latest candle.
        
        Args:
            symbol: The trading pair symbol (e.g., 'BTCUSDT')
            timestamp: Optional timestamp in seconds (Unix epoch).
            
        Returns:
            A dictionary containing price and timestamp information.
            Example: {'price': 12345.67, 'timestamp': 1670000000, 'symbol': 'BTCUSDT'}
        """
        endpoint = "/v5/market/mark-price-kline"
        
        # Default interval is 1 minute for granular data
        params = {
            "category": "linear",
            "symbol": symbol.upper(),
            "interval": "1",
            "limit": 1
        }

        if timestamp:
            # API expects milliseconds
            ts_ms = int(timestamp * 1000)
            params["start"] = ts_ms
            params["end"] = ts_ms
        else:
            # For live price, we don't set start/end, just get the latest 1.
            pass

        try:
            response = requests.get(f"{self.BASE_URL}{endpoint}", params=params)
            response.raise_for_status()
            data = response.json()

            if data["retCode"] != 0:
                raise Exception(f"API Error: {data['retMsg']}")

            if not data["result"]["list"]:
                return {"error": "No data found for this symbol/timestamp"}

            # Kline format: [startTime, open, high, low, close]
            # We use 'close' as the mark price for that minute.
            latest_kline = data["result"]["list"][0]
            price = float(latest_kline[4])
            kline_ts = int(latest_kline[0]) / 1000

            return {
                "symbol": symbol.upper(),
                "price": price,
                "timestamp": kline_ts,
                "is_historical": timestamp is not None
            }

        except Exception as e:
            return {"error": str(e)}

if __name__ == "__main__":
    # Quick test
    client = MarkPriceClient()
    print(f"Fetch BTCUSDT: {client.get_mark_price('BTCUSDT')}")
