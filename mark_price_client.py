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
            A dictionary with open, high, low, close (1m candle), timestamp, symbol.
            Example: {'symbol': 'BTCUSDT', 'open': 1.2, 'high': 1.3, 'low': 1.1, 'close': 1.25, 'timestamp': 1670000000}
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

            # Mark-price-kline: [startTime, open, high, low, close] (no volume)
            latest_kline = data["result"]["list"][0]
            kline_ts = int(latest_kline[0]) / 1000
            open_p = float(latest_kline[1])
            high = float(latest_kline[2])
            low = float(latest_kline[3])
            close = float(latest_kline[4])
            volume = float(latest_kline[5]) if len(latest_kline) > 5 else None

            # If mark-price-kline didn't return volume, get it from regular kline (same minute)
            if volume is None:
                volume = self._get_kline_volume(symbol, kline_ts)

            return {
                "symbol": symbol.upper(),
                "open": open_p,
                "high": high,
                "low": low,
                "close": close,
                "volume": volume,
                "timestamp": kline_ts,
                "is_historical": timestamp is not None
            }

        except Exception as e:
            return {"error": str(e)}

    def _get_kline_volume(self, symbol: str, candle_timestamp_sec: float) -> Optional[float]:
        """Fetch trading volume for the same 1m candle from regular kline endpoint."""
        try:
            ts_ms = int(candle_timestamp_sec * 1000)
            resp = requests.get(
                f"{self.BASE_URL}/v5/market/kline",
                params={
                    "category": "linear",
                    "symbol": symbol.upper(),
                    "interval": "1",
                    "start": ts_ms,
                    "end": ts_ms,
                    "limit": 1,
                },
                timeout=10,
            )
            resp.raise_for_status()
            data = resp.json()
            if data.get("retCode") != 0 or not data.get("result", {}).get("list"):
                return None
            # Kline: [startTime, open, high, low, close, volume, turnover]
            row = data["result"]["list"][0]
            return float(row[5]) if len(row) > 5 else None
        except Exception:
            return None

if __name__ == "__main__":
    # Quick test
    client = MarkPriceClient()
    print(f"Fetch BTCUSDT: {client.get_mark_price('BTCUSDT')}")
