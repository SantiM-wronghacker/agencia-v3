from tools.base import BaseTool, ToolResult, tool

_YAHOO_URL = "https://query1.finance.yahoo.com/v8/finance/chart/{ticker}"
_COINGECKO_URL = "https://api.coingecko.com/api/v3/simple/price"
_EXCHANGE_URL = "https://api.exchangerate-api.com/v4/latest/{currency}"


@tool
class MarketDataTool(BaseTool):
    name = "market_data"
    description = (
        "Obtiene datos financieros del mercado. "
        "Úsala para consultar precios de acciones, "
        "criptomonedas y tipos de cambio."
    )

    def run(self, action: str = "", **kwargs) -> ToolResult:
        if action == "get_stock":
            return self._get_stock(**kwargs)
        if action == "get_crypto":
            return self._get_crypto(**kwargs)
        if action == "get_exchange_rate":
            return self._get_exchange_rate(**kwargs)
        if action == "get_indicators":
            return self._get_indicators(**kwargs)
        return self._error(f"Acción '{action}' no soportada")

    def _get_stock(self, ticker: str = "") -> ToolResult:
        import httpx

        try:
            r = httpx.get(
                _YAHOO_URL.format(ticker=ticker.upper()),
                params={"interval": "1d", "range": "5d"},
                headers={"User-Agent": "Mozilla/5.0"},
                timeout=15,
            )
            r.raise_for_status()
            data = r.json()
            meta = data["chart"]["result"][0]["meta"]
            precio = meta.get("regularMarketPrice", 0)
            prev_close = meta.get("previousClose") or meta.get("chartPreviousClose", precio)
            cambio_pct = ((precio - prev_close) / prev_close * 100) if prev_close else 0
            volumen = meta.get("regularMarketVolume", 0)
            low_52 = meta.get("fiftyTwoWeekLow", 0)
            high_52 = meta.get("fiftyTwoWeekHigh", 0)
            currency = meta.get("currency", "USD")
            return self._success(
                f"{ticker.upper()}: ${precio:.2f} {currency} ({cambio_pct:+.2f}%)\n"
                f"Volumen: {volumen:,}\n"
                f"Rango 52s: ${low_52:.2f} - ${high_52:.2f}",
                raw_data={
                    "ticker": ticker.upper(), "price": precio,
                    "change_pct": cambio_pct, "volume": volumen,
                },
            )
        except Exception as e:
            return self._error(f"Error obteniendo datos de {ticker}: {e}")

    def _get_crypto(self, symbol: str = "") -> ToolResult:
        import httpx

        try:
            r = httpx.get(
                _COINGECKO_URL,
                params={
                    "ids": symbol.lower(),
                    "vs_currencies": "usd,mxn",
                    "include_24hr_change": "true",
                },
                timeout=15,
            )
            r.raise_for_status()
            data = r.json()
            coin = data.get(symbol.lower(), {})
            if not coin:
                return self._error(f"Criptomoneda '{symbol}' no encontrada en CoinGecko")
            usd = coin.get("usd", 0)
            mxn = coin.get("mxn", 0)
            change = coin.get("usd_24h_change", 0)
            return self._success(
                f"{symbol.upper()}: ${usd:,.2f} USD ({change:+.2f}% 24h)\n"
                f"En MXN: ${mxn:,.2f}",
                raw_data={"symbol": symbol, "usd": usd, "mxn": mxn,
                          "change_24h": change},
            )
        except Exception as e:
            return self._error(f"Error obteniendo datos de {symbol}: {e}")

    def _get_exchange_rate(
        self, from_currency: str = "USD", to_currency: str = "MXN"
    ) -> ToolResult:
        import httpx

        try:
            r = httpx.get(
                _EXCHANGE_URL.format(currency=from_currency.upper()),
                timeout=15,
            )
            r.raise_for_status()
            data = r.json()
            rates = data.get("rates", {})
            rate = rates.get(to_currency.upper())
            if rate is None:
                return self._error(
                    f"Moneda '{to_currency}' no encontrada. "
                    f"Disponibles: {', '.join(list(rates.keys())[:10])}"
                )
            return self._success(
                f"1 {from_currency.upper()} = {rate:.4f} {to_currency.upper()}",
                raw_data={
                    "from": from_currency.upper(),
                    "to": to_currency.upper(),
                    "rate": rate,
                },
            )
        except Exception as e:
            return self._error(f"Error obteniendo tipo de cambio: {e}")

    def _get_indicators(self, country: str = "MX") -> ToolResult:
        if country.upper() == "MX":
            # Delegate to BanxicoTool for Mexican indicators
            try:
                from tools.intelligence.banxico import BanxicoTool
                bt = BanxicoTool()
                result = bt.run(action="get_all")
                return result
            except Exception as e:
                return self._error(f"Error obteniendo indicadores MX: {e}")
        # World Bank API for other countries
        import httpx

        try:
            indicators = {
                "NY.GDP.MKTP.CD": "PIB (USD)",
                "FP.CPI.TOTL.ZG": "Inflación (%)",
                "SL.UEM.TOTL.ZS": "Desempleo (%)",
            }
            lines = [f"Indicadores macroeconómicos — {country.upper()}:"]
            for ind_code, ind_name in indicators.items():
                try:
                    r = httpx.get(
                        f"https://api.worldbank.org/v2/country/{country}/indicator/{ind_code}",
                        params={"format": "json", "mrv": 1},
                        timeout=10,
                    )
                    r.raise_for_status()
                    data = r.json()
                    if len(data) > 1 and data[1]:
                        valor = data[1][0].get("value")
                        year = data[1][0].get("date", "")
                        lines.append(f"  {ind_name}: {valor} ({year})")
                except Exception:
                    lines.append(f"  {ind_name}: N/D")
            return self._success("\n".join(lines))
        except Exception as e:
            return self._error(f"Error obteniendo indicadores de {country}: {e}")
