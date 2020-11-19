import pandas as pd
import requests
import re
import time
import math
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import as_completed

URL = "https://www.galopp-statistik.de/DisplayErgebnis.php?id="
NUMBER_OF_RACES = 10 # Change to number of races to scrape
START_ID = 1
RACE_IDS = [x for x in range(START_ID, START_ID+NUMBER_OF_RACES)]
CHUNK_SIZE = 1000

def scrape_race_by_id(id):
    """
    Scrapes one page of the specified id. Extracts all the information
    possible and puts them into a list that is returned.

    id: The ID that is to be loaded.

    return: List of information on each race.
    """
    race_information = []

    # General race information
    date = location = distance = ground_state = prize = category = None

    print(f"Scraping page: {id}")
    request = requests.get(URL + str(id))
    soup = BeautifulSoup(request.content, "lxml")

    # Get header information (date and location)
    header = soup.find("div", class_="renntagKopf")
    if len(header) >= 2:
        date = header.find_all("div", class_="ZeitundOrt")[0]
        location = header.find_all("div", class_="ZeitundOrt")[1]

    # Get distance and prize
    distance_prize = soup.find("div", class_="zoile distance-cash")
    distance_prize = distance_prize.text.split("-")
    if len(distance_prize) >= 2:
        distance = distance_prize[0]
        prize = distance_prize[1]

    # Get category and race class
    category_race = str(soup.find("div", class_="zoile kat-class"))
    category_race = re.findall(r"<b>.*</b>", str(category_race))
    if len(category_race) >= 2:
        category = category_race[0][3:-4]
        race_class = category_race[1][3:-4]
    elif len(category_race) == 1:
        category = category_race[0][3:-4]

    # Get the state of the ground
    ground_state = soup.find("div", class_="rennen-druck").text

    # Put all info into the race information list
    race_information.append(date)
    race_information.append(location)
    race_information.append(distance)
    race_information.append(prize)
    race_information.append(category)
    race_information.append(race_class)
    race_information.append(ground_state)

    # Get all horse entries
    horse_entry = []
    entries = soup.find_all("div", class_="table-result-row")
    for entry in entries:

        # (Re)set horse information
        trainer_name = weight  = category = race_class = None
        placement = horse_name = jockey_name = None

        # Get all information
        placement = entry.find("div", class_="celle place").text
        horse_name = entry.find("div", class_="celle horsename").text
        jockey_trainer = entry.find_all("div", class_="celle trainer-box")
        if len(jockey_trainer) >= 2:
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
    start_time = time.time()
    race_information_list = []

    # Splitting the RACE_IDS into chunks, so it can be saved after each chunk,
    # reducing the memory usage
    for chunk_number in range(math.ceil(len(RACE_IDS)/CHUNK_SIZE)):
        chunk_start = chunk_number*1000
        chunk_end = min(((chunk_number+1)*1000)-1, len(RACE_IDS)-1)
        print(f"Scraping chunks from: {chunk_start} to {chunk_end}")

        # Concurrent scraping for speedups
        # time without:
        # time with 8 threads:
        # time with 16 threads:
        chunk = [x for x in range(chunk_start, chunk_end)]
        with ThreadPoolExecutor(max_workers=min(16, len(chunk))) as executor:
            results = executor.map(scrape_race_by_id, chunk)

        # Save chunk
        for result in results:
            race_information_list.append(result)

        column_names = ["Date",
                        "Location",
                        "Distance",
                        "Prize",
                        "Category",
                        "Class",
                        "Ground_state",
                        "Horses"]

        print(f"Saving chunks from: {chunk_start} to {chunk_end}")
        information_dataframe = pd.DataFrame(data=race_information_list, columns=column_names)
        information_dataframe.to_csv(f"racing_history-{chunk_start}-{chunk_end}.csv", index=False)

    end_time = time.time()
    print(f"Finished scraping {len(RACE_IDS)} pages in: {(end_time - start_time)/60} minutes.")
