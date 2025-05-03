import os
from dotenv import load_dotenv

load_dotenv()

SERIAL_PORT     = os.getenv("SERIAL_PORT", "CNCA0")
BAUD_RATE       = int(os.getenv("BAUD_RATE", "9600"))

SQL_SERVER      = os.getenv("SQL_SERVER", "localhost,1433")
SQL_DATABASE    = os.getenv("SQL_DATABASE", "FarmTechDB")
SQL_USERNAME    = os.getenv("SQL_USERNAME", "sa")
SQL_PASSWORD    = os.getenv("SQL_PASSWORD", "admin!1234")

API_KEY_WEATHER = os.getenv("OPENWEATHER_API_KEY", "66f8aa7fe075bab3f34048b46f40b64c")
OWM_URL         = "http://api.openweathermap.org/data/2.5/weather"
