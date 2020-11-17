import pandas as pd
import requests
from bs4 import BeautifulSoup

URL = "https://www.galopp-statistik.de/DisplayErgebnis.php?id="

def scrape_race_by_id(id):
    id = 9100

    # Information to be scraped
    date = location = distance = placement = horse_name = jockey_name = None
    trainer_name = weight = prize = ground_state = category = race_class = None

    print("Scraping page: {id}")
    request = requests.get(URL + str(id))
    soup = BeautifulSoup(request.content, "lxml")

    # Get header information (date and location)
    header = soup.find("div", class_="renntagKopf")
    date = header.find_all("div", class_="ZeitundOrt")[0]
    location = header.find_all("div", class_="ZeitundOrt")[1]

    # Get distance and prize
    distance = soup.find("div", class_='zoile distance-cash')
    distance_prize = distance.text.split("-")
    distance = distance_prize[0]
    prize = distance_prize[1]

    # Get category
    tmp = soup.find("div", class_="zoile kat-class")
    print(tmp)



if __name__ == "__main__":
    upper_bound = 1 # Change to number of races to scrape
    for id in range(upper_bound):
        scrape_race_by_id(id)
