import requests

def get_weather(city: str) -> str:
    """Fetch the current weather of a city"""
    url = f"https://wttr.in/{city}?format=3"
    try:
        response = requests.get(url, timeout=5)
        return response.text
    except Exception as e:
        return f"Error: could not fetch weather for '{city}': {e}"