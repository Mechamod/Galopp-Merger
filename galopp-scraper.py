import pandas as pd
import requests
import re
from bs4 import BeautifulSoup

URL = "https://www.galopp-statistik.de/DisplayErgebnis.php?id="

def scrape_race_by_id(id):
    id = 9100 # DELETE ME
    race_information = []

    # General race information
    date = location = distance = ground_state = prize = None

    print(f"Scraping page: {id}")
    request = requests.get(URL + str(id))
    soup = BeautifulSoup(request.content, "lxml")

    # Get header information (date and location)
    header = soup.find("div", class_="renntagKopf")
    date = header.find_all("div", class_="ZeitundOrt")[0]
    location = header.find_all("div", class_="ZeitundOrt")[1]

    # Get distance and prize
    distance_prize = soup.find("div", class_="zoile distance-cash")
    distance_prize = distance_prize.text.split("-")
    distance = distance_prize[0]
    prize = distance_prize[1]

    # Get category and race class
    category_race = str(soup.find("div", class_="zoile kat-class"))
    category_race = re.findall(r"<b>.*</b>", str(category_race))
    category = category_race[0][3:-4]
    race_class = category_race[1][3:-4]

    # Get the state of the ground
    ground_state = soup.find("div", class_="rennen-druck").text

    # Put all info into the race information list
    race_information.append(header)
    race_information.append(date)
    race_information.append(location)
    race_information.append(distance)
    race_information.append(prize)
    race_information.append(category)
    race_information.append(race_class)
    race_information.append(ground_state)

    # Get all horse entries
    entries = soup.find_all("div", class_="table-result-row")
    for entry in entries:
        horse_entry = []

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

        # Put it into a horse entry and add it to the race information
        horse_entry.append(placement)
        horse_entry.append(horse_name)
        horse_entry.append(jockey)
        horse_entry.append(trainer)
        horse_entry.append(weight)
        race_information.append(horse_entry)

    return race_information

if __name__ == "__main__":
    upper_bound = 1 # Change to number of races to scrape
    for id in range(upper_bound):
        info = scrape_race_by_id(id)
        print(info)
