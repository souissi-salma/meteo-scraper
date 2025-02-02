import requests
import time

import schedule
# clé API OpenWeatherMap
API_KEY = "7d6b0f67a3d19b1f1307961b12657cf4"
# Configuration Supabase
SUPABASE_URL = "https://fmbqkfomfypbtrwonkjv.supabase.co"  # URL Supabase
SUPABASE_API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZtYnFrZm9tZnlwYnRyd29ua2p2Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3Mzg0OTkwNTUsImV4cCI6MjA1NDA3NTA1NX0.vp7PKLtTltsCRA5dB0ZQ7jo94jN_mU7Pwt2yuObQAUk"  # clé API
HEADERS = {
    "apikey": SUPABASE_API_KEY,
    "Authorization": f"Bearer {SUPABASE_API_KEY}",
    "Content-Type": "application/json"
}
# Récupérer la liste des gouvernorats depuis Supabase
def get_gouvernorats():
    url = f"{SUPABASE_URL}/rest/v1/gouvernorats"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        return response.json()  # Retourne la liste des gouvernorats
    else:
        print("Erreur lors de la récupération des gouvernorats :", response.text)
        return []

# Fonction pour obtenir les données en temps réel
def get_current_weather(lat,lon):
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    data = response.json()
    return data

# Fonction pour insérer les données météo dans Supabase
def insert_weather_data(nom, temp, humidite, pression, vent, precipitations):
    url = f"{SUPABASE_URL}/rest/v1/meteo"
    data = {
        "gouvernorat": nom,
        "temperature": temp,
        "humidite": humidite,
        "pression": pression,
        "vent": vent,
        "precipitations": precipitations,
        "date": "now()"  # Timestamp actuel dans PostgreSQL
    }
    response = requests.post(url, json=data, headers=HEADERS)
    if response.status_code not in [200, 201]:
        print(f"Erreur insertion {nom} :", response.text)
# Fonction principale
def update_weather_data():
    gouvernorats = get_gouvernorats()
    for gov in gouvernorats:
        nom, lat, lon = gov["nom"], gov["latitude"], gov["longitude"]

        data = get_current_weather(lat, lon)
        if "main" in data:
            temp = data["main"]["temp"]
            humidite = data["main"]["humidity"]
            pression = data["main"]["pressure"]
            vent = data["wind"]["speed"]
            precipitations = data.get("rain", {}).get("1h", 0)  # 0 si pas de pluie
        else:
            temp = humidite = pression = vent = precipitations = None

        insert_weather_data(nom, temp, humidite, pression, vent, precipitations)
# Planifier la mise à jour toutes les heures
schedule.every(1).hour.do(get_current_weather)
# Boucle pour exécuter le job à intervalle
while True:
    schedule.run_pending()
    time.sleep(1)



