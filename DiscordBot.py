"""
Die restlichen Dateien die importiert werden (requirements txt, config, etc.. sind eigene Files auf meinem lokalen Rechner die ich nicht auf Github hochlade. (private token, api keys, id etc)
Der Code hier ist nur zum showcase da
Es handelt sich um Ausschnitte und  nicht den gesamten Bot.
"""






# ----------------------------------------------------- Imports ------------------------------------------------------#
import json
import discord
import random
from discord.ext import commands
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
import datetime
from geopy.geocoders import Nominatim
from time import sleep
from bearerAuth import *
from datetime import date
import logging

# Importiere API-Schlüssel, Channel ID und Token aus einer Konfigurationsdatei
from config import DISCORD_TOKEN, OPENWEATHERMAP_API_KEY, RIOT_API_KEY, CHANNEL_ID, MY_LAT, MY_LONG

# ------------------------------- Starting stuff + Class -------------------------------------------------------#

global intents
intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix="!", intents=intents)
geolocator = Nominatim(user_agent="geoapiExercises")
logging.basicConfig(filename='bot.log', level=logging.DEBUG)


class MyClient(discord.Client):
    # --------------------------------------------------------------- APIS -------------------------------------------------#

    """
         Überprüft, ob die Internationale Raumstation (ISS) sich in der Nähe eines bestimmten Ortes befindet
         und sendet eine Nachricht mit ihrem Standort.
         Diese Funktion verwendet die Open Notify API,
         um die aktuellen Koordinaten der ISS abzurufen
         und festzustellen,
         ob sie sich in der Nähe eines vordefinierten Ortes befindet.
    """

    async def is_iss_overhead(self):
        response = requests.get(
            url="http://api.open-notify.org/iss-now.json")  # Konvertiert die API-Antwort in ein JSON-Format und speichert sie in der Variable 'data'
        data = response.json()
        longitude = float(data["iss_position"]["longitude"])  # iss longitude
        latitude = float(data["iss_position"]["latitude"])  # iss latitude
        if MY_LAT - 8 <= latitude <= MY_LAT + 8 and MY_LONG - 8 <= longitude <= MY_LONG + 8:  # checkt ob die dynamischen ISS koordinaten in der Nähe meiner statischen Koordinaten sind
            location = geolocator.reverse(str(latitude) + "," + str(
                longitude))  # Verwendet die geopy-Bibliothek, um die dynamischen Koordinaten der ISS in einen lesbaren Standort umzuwandeln
            c = client.get_channel(
                CHANNEL_ID)  # discord library spezifisch, identifikation des Channels wo die Nachricht hin soll.
            if str(location) == "None":  # geopy gibt none aus wenn sich die ISS über Gewässer befindet, Abfangen des Errors
                await c.send(f"Die ISS befindet sich gerade über dem Meer")
                return
            address = location.raw['address']  # Extrahiert Länder- und Stadt aus dem Standort und sendet eine Nachricht
            country = address.get('country', '')
            state = address.get('state', '')
            await c.send(f"Die ISS befindet sich gerade über {country}. Ihr genauer Standort ist {state}")
            sleep(2)

    # Wetter API jeden Morgen um 8
    """
        Ruft Wetterinformationen für einen bestimmten Ort ab und sendet sie in den Discord-Channel.
        Diese Funktion verwendet die OpenWeatherMap-API, um aktuelle Wetterdaten für einen festgelegten Ort abzurufen.
    """

    async def weather(self):
        c = client.get_channel(CHANNEL_ID)
        url = "https://api.openweathermap.org/data/2.5/onecall?lat=%s&lon=%s&appid=%s&units=metric" % (
            # url für die Api Anfrage
            MY_LAT, MY_LONG, OPENWEATHERMAP_API_KEY)
        response = requests.get(url)  # Sende eine Anfrage an die OpenWeatherMap-API
        data = json.loads(response.text)
        current = data["current"]["temp"]  # Extrahiere relevante Wetterdaten aus der API-Antwort
        felt = data["current"]["feels_like"]
        weather = data["current"]["weather"][0]["main"]
        await c.send(
            f"Gerade sind es in Sankt Augustin {current} Grad Celsius. Gefühlt sind es {felt} Grad Celsius.\nDie Wetterumstände heute sind {weather}.")  # Sende die Wetterdaten in den Discord-Channel

    # lor fact API
    """
    Schickt täglich ein Zitat aus Herr der Ringe in die Gruppe 
    """

    async def lor(self):
        c = client.get_channel(CHANNEL_ID)
        response = requests.get('https://the-one-api.dev/v2/quote', auth=BearerAuth(
            'tpPsGKst53V4qYkX5AvH'))  # Sendet eine Anfrage an die API "the-one-api.dev", um ein Zitat aus "Herr der Ringe" zu erhalten
        data = response.json()  # Konvertiert die API-Antwort in ein JSON-Format
        quote = data["docs"][random.randint(1, 900)][
            "dialog"]  # Wählt ein zufälliges Zitat aus den erhaltenen Daten aus (Zahlenbereich: 1 bis 900)
        await c.send(f"Die tägliche Quote aus Herr der Ringe: {quote}")

    """
    Sendet täglich das NASA Picture of the day in die Gruppe
    """


async def nasa():
    c = client.get_channel(CHANNEL_ID)
    datum = date.today()
    logging.debug(datum)
    datum = datum.__str__()
    logging.debug(type(datum))
    url = f"https://api.nasa.gov/planetary/apod?api_key=e8bH0Zzrp1ztbSsICXzevghp27ETOY8FuEbblO9V&date={datum}"  # Erstellt die URL für die NASA API-Anfrage mit dem aktualisierten Datum
    response = requests.get(url)
    data = response.json()
    logging.debug(data)
    potd = data["url"]  # Extrahiert das URL des Bildes des Tages aus den API-Daten
    await c.send(f"NASA Picture of the day: \n {potd}")


async def riot():
    # Design der Discord Nachricht
    embed = discord.Embed(colour=discord.Colour(0xffd000))
    embed.set_thumbnail(url="https://pbs.twimg.com/media/DnSbFTAXoAIVD7X?format=jpg&name=360x360")
    embed.set_author(name="Herman Bot")

    c = client.get_channel(CHANNEL_ID)
    puuid_idc = "8u_Qo8ty7iwMyr-NK479ikhhTESS1VRyBh4iWs8ujU2l2JzJ-flXnAssnrSKwqVEhw5Jd4PCSRkpyw"  # PUUID des Spielers, für den die Daten abgerufen werden sollen
    last10games_id = requests.get(  # Die API-Anfrage, um die IDs der letzten 10 Spiele des Spielers abzurufen
        "https://europe.api.riotgames.com/lol/match/v5/matches/by-puuid/8u_Qo8ty7iwMyr-NK479ikhhTESS1VRyBh4iWs8ujU2l2JzJ-flXnAssnrSKwqVEhw5Jd4PCSRkpyw/ids?type=ranked&start=0&count=10&api_key={RIOT_API_KEY}")
    f = open('lastMatch.txt')
    lines = f.readlines()
    last10games_id_json = last10games_id.json()
    newest_match_so_far = str(lines)  # Konvertiert die zuletzt aufgezeichnete Spiel-ID in einen String
    newMatch = last10games_id_json  # Speichert die JSON-Daten des neuesten Spiels in einer separaten Variable
    newest_match_so_far = newest_match_so_far.split(
        '"')  # Teilt den gespeicherten String bei Anführungszeichen auf, um die Spiel-ID zu isolieren
    logging.debug(newMatch)
    if newest_match_so_far[1] != newMatch[
        0]:  # Überprüft, ob die neueste aufgezeichnete Spiel-ID von der aktuellsten Spiel-ID abweicht
        newLastMatch = list(last10games_id)[0]  # Aktualisiert Sie die zuletzt aufgezeichnete Spiel-ID in der Datei
        with open("lastMatch.txt", mode="w") as data:
            data.write(f"{newLastMatch}")
        matchid = last10games_id_json[0]
        latest_game = requests.get(  # Abrufen der Daten für das neueste Spiel
            f"https://europe.api.riotgames.com/lol/match/v5/matches/{matchid}?api_key={RIOT_API_KEY}")
        latest_game_json = latest_game.json()
        specific_player_id = 0
        counter = -1
        for player in latest_game_json["info"][
            "participants"]:  # Sucht nach der ID des spezifischen Spielers im aktuellen Spiel
            counter += 1
            if player["puuid"] == puuid_idc:
                specific_player_id = counter
                break
            else:
                continue
        kills = latest_game_json["info"]["participants"][specific_player_id][
            "kills"]  # Extrahiert Sie die relevanten Statistiken des Spielers
        tode = latest_game_json["info"]["participants"][specific_player_id]["deaths"]  # durch json iterieren
        assists = latest_game_json["info"]["participants"][specific_player_id]["assists"]
        champion = latest_game_json["info"]["participants"][specific_player_id]["championName"]
        lane = latest_game_json["info"]["participants"][specific_player_id]["lane"]
        lane = lane.lower()
        if latest_game_json["info"]["participants"][specific_player_id][
            "win"]:  # Überprüfen Sie, ob der Spieler das Spiel gewonnen oder verloren hat
            ergebnis = "gewonnen. Sehr gut Jonas"
        else:
            ergebnis = "leider verloren."
        embedmes = f"Jonas hat gerade ein League of Legends Ranked beendet. Er ist mit {champion} auf der {lane} lane {kills}/{tode}/{assists} gegangen und hat das Spiel {ergebnis}."
        embed.add_field(name="Nachricht", value=f"{embedmes}")
        await c.send(embed=embed)
    else:
        return

    # ----------------------------------------------------------------------------- on_ready Method -----------------------------------------------------------------------------#


@client.event
async def on_ready(self):
    logging.debug(datetime.datetime.now())
    scheduler = AsyncIOScheduler()

    # Liste von Aufgaben erstellen
    tasks = [
        (self.schedule_daily_message, CronTrigger(hour=16, minute=57)),  # Damit der Bot eigenständig arbeitet, cronjobs
        (self.riot, CronTrigger(minute="*/1")),
        (self.lor, CronTrigger(hour=14, minute=31)),
        (self.is_iss_overhead, CronTrigger(hour="*/3")),
        (self.weather, CronTrigger(hour=6, minute=0)),
        (self.nasa, CronTrigger(hour=23, minute=30))
    ]

    for task, trigger in tasks:
        scheduler.add_job(task, trigger)

    scheduler.start()

    # ----------------------------------------------------------------------------- Sonstiges -----------------------------------------------------------------------------#

    client = MyClient(intents=intents)
    client.run(DISCORD_TOKEN)
