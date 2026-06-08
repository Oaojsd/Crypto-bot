import json
import urllib.request
from urllib.error import HTTPError, URLError

from config.settings import settings


class MarketData:
    def __init__(self):
        self.base_url = "https://api.binance.com"

    def fetch_ohlcv(self, limit=500, timeframe=None):
        symbol = settings.SYMBOL.replace("/", "")

        selected_timeframe = timeframe

        if selected_timeframe is None:
            selected_timeframe = settings.TIMEFRAME

        url = (
            f"{self.base_url}/api/v3/klines"
            f"?symbol={symbol}"
            f"&interval={selected_timeframe}"
            f"&limit={limit}"
        )

        try:
            with urllib.request.urlopen(url, timeout=10) as response:
                data = json.loads(response.read().decode("utf-8"))

        except HTTPError as error:
            raise Exception(f"Erro HTTP ao buscar dados: {error.code}")

        except URLError as error:
            raise Exception(f"Erro de conexão ao buscar dados: {error.reason}")

        candles = []

        for item in data:
            candles.append({
                "timestamp": item[0],
                "open": float(item[1]),
                "high": float(item[2]),
                "low": float(item[3]),
                "close": float(item[4]),
                "volume": float(item[5]),
            })

        return candles