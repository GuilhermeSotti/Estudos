import requests
from config import API_KEY_WEATHER, OWM_URL

def fetch_weather(city: str = "São%20Paulo,BR") -> bool:
    """
    Consulta a OpenWeatherMap e retorna True se estiver chovendo.
    """
    params = {
        "q": city,
        "appid": API_KEY_WEATHER,
        "units": "metric"
    }
    resp = requests.get(OWM_URL, params=params, timeout=10)
    data = resp.json()
    weather_main = (data.get("weather") or [{}])[0].get("main", "").lower()
    return "rain" in weather_main
