import pandas as pd
import requests
import re
from bs4 import BeautifulSoup

URL = "https://www.galopp-statistik.de/DisplayErgebnis.php?id="

def scrape_race_by_id(id):
    id = 9100

    # General race information
    date = location = distance = ground_state = prize = None

    print("Scraping page: {id}")
    request = requests.get(URL + str(id))
    soup = BeautifulSoup(request.content, "lxml")

    # Get header information (date and location)
    header = soup.find("div", class_="renntagKopf")
    date = header.find_all("div", class_="ZeitundOrt")[0]
    location = header.find_all("div", class_="ZeitundOrt")[1]

    # Get distance and prize
    distance = soup.find("div", class_="zoile distance-cash")
    distance_prize = distance.text.split("-")
    distance = distance_prize[0]
    prize = distance_prize[1]

    # Get category and race class
    tmp = str(soup.find("div", class_="zoile kat-class"))
    category_race = re.findall(r"<b>.*</b>", str(tmp))
    category = category_race[0][3:-4]
    race_class = category_race[1][3:-4]

    # Get the state of the ground
    ground_state = soup.find("div", class_="rennen-druck").text

    # Get all horse entries
    entries = soup.find_all("div", class_="table-result-row")
    for entry in entries:

        # (Re)set horse information
        trainer_name = weight  = category = race_class = None
        placement = horse_name = jockey_name = None

        # Get all information
        placement = entry.find("div", class_="celle place").text
        horse_name = entry.find("div", class_="celle horsename").text
        jockey_trainer = entry.find_all("div", class_="celle trainer-box")
        jockey = jockey_trainer[0].text
        trainer = jockey_trainer[1].text
        weight = entry.find("div", class_="weight").text


if __name__ == "__main__":
    upper_bound = 1 # Change to number of races to scrape
    for id in range(upper_bound):
        scrape_race_by_id(id)
