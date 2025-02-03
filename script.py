import requests
import pandas as pd
import datetime
import os

# Clé API OpenWeatherMap
API_KEY = "TA_CLE_API"

# Liste des régions avec leurs coordonnées
regions = {
    "Tunis": (36.8002068, 10.1857757),
    "Ariana": (36.968573500000005, 10.121985506329507),
    "Ben Arous": (36.63064825, 10.210082703817534),
    "Manouba": (36.7624363, 9.833619078262766),
    "Nabeul": (36.4512897, 10.7355915),
    "Zaghouan": (36.3319504, 10.045299971877625),
    "Bizerte": (37.2720905, 9.8708565),
    "Beja": (36.7236755, 9.185382),
    "Jendouba": (36.67797255, 8.752646965460535),
    "Kef": (36.03576425, 8.72493808761197),
    "Siliana": (35.9715323, 9.3577128756367),
    "Kasserine": (35.1687646, 8.8365654),
    "Sidi Bouzid": (34.881181, 9.526359847182345),
    "Kairouan": (35.6710101, 10.10062),
    "Kébili": (33.33877015, 8.703290964584628),
    "Tozeur": (33.9239001, 8.1370639),
    "Gabès": (33.8878082, 10.10044),
    "Medenine": (32.981998700000005, 11.287025364730832),
    "Tataouine": (31.7317009, 9.770219749624271),
    "Mahdia": (35.503642, 11.0682429),
    "Monastir": (35.7707582, 10.8280511),
    "Sousse": (35.8288284, 10.6405254),
    "Sfax": (34.7394361, 10.7604024),
    "Gafsa": (34.4224374, 8.7843862)
}

# Dossier de stockage des fichiers CSV
DATA_DIR = "data"

# Vérifier si le dossier existe, sinon le créer
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

# Liste pour stocker toutes les données des villes
all_weather_data = []

# Date et heure actuelles (pour nommer le fichier)
current_time = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

# Fonction pour récupérer les données météo d'une ville
def get_weather_data(city, lat, lon):
    URL = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"

    try:
        response = requests.get(URL)
        data = response.json()

        if response.status_code == 200:
            # Extraire les infos utiles
            weather_data = {
                "city": city,
                "temperature": data["main"]["temp"],
                "humidity": data["main"]["humidity"],
                "pressure": data["main"]["pressure"],
                "wind": data["wind"]["speed"],
                "precipitation": data.get("rain", {}).get("1h", 0),  # Précipitation en mm (0 si non disponible)
                "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }

            # Ajouter aux données globales
            all_weather_data.append(weather_data)

        else:
            print(f"Erreur lors de la récupération des données météo pour {city}: {data}")

    except Exception as e:
        print(f"Erreur pour {city}:", e)

# Récupérer les données pour chaque ville
for city, (lat, lon) in regions.items():
    get_weather_data(city, lat, lon)

# Créer un DataFrame Pandas contenant toutes les villes
df = pd.DataFrame(all_weather_data)

# Nom du fichier basé sur l'heure actuelle
filename = f"{DATA_DIR}/weather_{current_time}.csv"

# Sauvegarde dans un fichier CSV unique
df.to_csv(filename, index=False, encoding='utf-8')

print(f"Données météo enregistrées dans {filename}")
