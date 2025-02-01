import requests
import time
import psycopg2
from psycopg2 import sql
import schedule
# clé API OpenWeatherMap
API_KEY = "7d6b0f67a3d19b1f1307961b12657cf4"
# Connexion à PostgreSQL
conn = psycopg2.connect(
    dbname="données_météorologiques",
    user="postgres",
    password="ismail",
    host="localhost",
    port="5432"
)
cur = conn.cursor()
# Récupérer la liste des gouvernorats avec leurs coordonnées
cur.execute("SELECT nom, latitude, longitude FROM gouvernorats;")
#récupère toutes les lignes et les stocke dans gouvernorats,Chaque gouvernorat sera sous la forme (nom, latitude, longitude)
gouvernorats = cur.fetchall() 

# Fonction pour obtenir les données en temps réel
def get_current_weather(lat,lon):
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    data = response.json()
    return data
# Boucle pour récupérer et insérer les données météo
for gov in gouvernorats:
    nom, lat, lon = gov  # Extraire le nom, la latitude et la longitude

    data = get_current_weather(lat, lon)  # Récupérer les données météo depuis OpenWeatherMap
    
    if "main" in data:  # Vérifier si l'API a bien renvoyé des données météo
        temp = data["main"]["temp"]  # Température en degrés Celsius
        humidité = data["main"]["humidity"]  # Humidité en %
        pression = data["main"]["pressure"]  # Pression atmosphérique en hPa
        vent = data["wind"]["speed"]  # Vitesse du vent en m/s
         # Vérifier si des précipitations existent
        if "rain" in data:
        # Si oui, récupérer la quantité de pluie dans la dernière heure (en mm)
            precipitations = data["rain"].get("1h", 0)  # Valeur de pluie dans les dernières heures, 0 si pas de pluie
        else:
            precipitations = 0  # Pas de pluie
    else:
    # Si aucune donnée météo n'est disponible,  affecter des valeurs par défaut
        temp = None
        humidité = None
        pression = None
        vent = None
        precipitations = None
        ensoleillement = None
    #Insérer les données météo dans PostgreSQL
    cur.execute("""
    INSERT INTO meteo (gouvernorat, temperature, humidite, pression, vent, precipitations, date)
    VALUES (%s, %s, %s, %s, %s, %s, NOW());
""", (nom, temp, humidité, pression, vent, precipitations))
#Insérer les données météo dans PostgreSQL
cur.execute("""
    INSERT INTO meteo (gouvernorat, temperature, humidite, pression, vent, precipitations, date)
    VALUES (%s, %s, %s, %s, %s, %s, NOW());
""", (nom, temp, humidité, pression, vent, precipitations))
conn.commit()  # Sauvegarde les modifications dans la base de données
# Planifier la mise à jour toutes les heures
schedule.every(1).hour.do(get_current_weather)
# Boucle pour exécuter le job à intervalle
while True:
    schedule.run_pending()
    time.sleep(1)
cur.close()  # Ferme le curseur
conn.close()  # Ferme la connexion PostgreSQL


