from datetime import datetime, timezone, timedelta

from fastmcp import FastMCP

mcp = FastMCP("Travel Assistant MCP Server")


@mcp.tool
def get_weather(city: str) -> dict:
    """Get the current weather for a city.

    Args:
        city: The name of the city (e.g. 'Rome', 'Tokyo').

    Returns:
        A dict with temperature_c, condition, and humidity_pct, or an error if the city is unknown.

    Note:
        Uses mock data — replace with a real API (e.g. OpenWeatherMap) in production.
    """
    weather_data = {
        "rome": {"temperature_c": 22, "condition": "Partly cloudy", "humidity_pct": 65},
        "paris": {"temperature_c": 18, "condition": "Light rain", "humidity_pct": 82},
        "new york": {"temperature_c": 15, "condition": "Sunny", "humidity_pct": 40},
        "london": {"temperature_c": 12, "condition": "Overcast", "humidity_pct": 75},
        "sydney": {"temperature_c": 28, "condition": "Clear", "humidity_pct": 55},
        "tokyo": {"temperature_c": 17, "condition": "Partly cloudy", "humidity_pct": 70},
        "dubai": {"temperature_c": 35, "condition": "Sunny", "humidity_pct": 30},
    }
    data = weather_data.get(city.lower())
    if data is None:
        return {"error": f"Unknown city: {city}"}
    return {"city": city, **data}


@mcp.tool
def get_current_time(city: str) -> dict:
    """Get the current local time and date for a city.

    Args:
        city: The name of the city (e.g. 'Tokyo', 'Paris').

    Returns:
        A dict with local_time, date, and utc_offset, or an error if the city is unknown.
    """
    utc_offsets = {
        "tokyo": 9,
        "paris": 1,
        "new york": -5,
        "london": 0,
        "sydney": 11,
        "dubai": 4,
        "los angeles": -8,
        "rome": 1,
    }
    offset_hours = utc_offsets.get(city.lower())
    if offset_hours is None:
        return {"error": f"Unknown city: {city}"}
    local_time = datetime.now(timezone.utc) + timedelta(hours=offset_hours)
    return {
        "city": city,
        "local_time": local_time.strftime("%H:%M"),
        "date": local_time.strftime("%Y-%m-%d"),
        "utc_offset": f"UTC{offset_hours:+d}",
    }


@mcp.tool
def convert_currency(amount: float, from_currency: str, to_currency: str) -> dict:
    """Convert an amount from one currency to another.

    Args:
        amount: The amount to convert.
        from_currency: Source currency code (e.g. 'USD', 'EUR').
        to_currency: Target currency code (e.g. 'JPY', 'GBP').

    Returns:
        A dict with the original and converted amounts.

    Note:
        Uses approximate fixed rates — replace with a real API in production.
    """
    # Mock rates. Replace with a real API in production.
    rates_to_usd = {
        "USD": 1.0,
        "EUR": 1.17,
        "JPY": 0.0063,
        "GBP": 1.26,
        "AUD": 0.65,
        "CHF": 1.12,
    }
    amount_in_usd = amount * rates_to_usd.get(from_currency.upper(), 1.0)
    converted = round(amount_in_usd / rates_to_usd.get(to_currency.upper(), 1.0), 2)
    return {
        "original": f"{amount} {from_currency.upper()}",
        "converted": f"{converted} {to_currency.upper()}",
    }


if __name__ == "__main__":
    mcp.run()
