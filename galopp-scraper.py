import pandas as pd
import requests
import re
import time
import math
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor

URL = "https://www.galopp-statistik.de/DisplayErgebnis.php?id="
NUMBER_OF_RACES = 9223 # Change to number of races to scrape
START_ID = 1
RACE_IDS = [x for x in range(START_ID, START_ID+NUMBER_OF_RACES)]
CHUNK_SIZE = 2000

def scrape_race_by_id(id):
    """
    Scrapes one page of the specified id. Extracts all the information
    possible and puts them into a list that is returned.

    id: The ID that is to be loaded.

    return: List of information on each race.
    """
    race_information = []

    # General race information
    date = location = distance = ground_state = prize = category = race_class = None

    # Make request
    request = requests.get(URL + str(id))
    soup = BeautifulSoup(request.content, "lxml")

    # Get header information (date and location)
    header = soup.find("div", class_="renntagKopf")
    if len(header) >= 2:
        date = header.find_all("div", class_="ZeitundOrt")[0].text
        location = header.find_all("div", class_="ZeitundOrt")[1].text

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

    # Remove newlines if variable is not null
    if date is not None:
        date = date.replace("\n", "")
    if location is not None:
        location = location.replace("\n", "")
    if distance is not None:
        distance = distance.replace("\n", "")
    if prize is not None:
        prize = prize.replace("\n", "")
    if category is not None:
        category = category.replace("\n", "")
    if race_class is not None:
        race_class = race_class.replace("\n", "")
    if ground_state is not None:
        ground_state = ground_state.replace("\n", "")

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
        trainer_name = weight  = None
        placement = horse_name = jockey_name = None

        # Get all information
        placement = entry.find("div", class_="celle place").text
        horse_name = entry.find("div", class_="celle horsename").text
        jockey_trainer = entry.find_all("div", class_="celle trainer-box")
        if len(jockey_trainer) >= 2:
            jockey = jockey_trainer[0].text
            trainer = jockey_trainer[1].text
        weight = entry.find("div", class_="weight").text

        # Remove newlines if variable is not null
        if placement is not None:
            placement = placement.replace("\n", "")
        if horse_name is not None:
            horse_name = horse_name.replace("\n", "")
        if jockey is not None:
            jockey = jockey.replace("\n", "")
        if trainer is not None:
            trainer = trainer.replace("\n", "")
        if weight is not None:
            weight = weight.replace("\n", "")

        # Put it into a horse entry and add it to the race information
        horse_entry.append(placement)
        horse_entry.append(horse_name)
        horse_entry.append(jockey)
        horse_entry.append(trainer)
        horse_entry.append(weight)
    race_information.append(horse_entry)

    return race_information

def scrape():
    start_time = time.time()

    # Splitting the RACE_IDS into chunks, so it can be saved after each chunk,
    # reducing the memory usage
    #
    # Add START_ID at the end, for the shift if already some has been loaded!
    for chunk_number in range(math.ceil(len(RACE_IDS)/CHUNK_SIZE)):
        race_information_list = []
        chunk_start = (chunk_number*CHUNK_SIZE)+START_ID
        chunk_end = min(((chunk_number+1)*CHUNK_SIZE)-1, len(RACE_IDS))+START_ID
        print(f"Scraping chunks from: {chunk_start} to {chunk_end}")
        print(chunk_start, chunk_end)
        # Concurrent scraping for speedups
        # time with 16 threads: ~11 min.
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
            information_dataframe.to_csv(f"csvs/racing_history-{chunk_start}-{chunk_end}.csv", index=False)
            del results # Make (some) space

    end_time = time.time()
    print(f"Finished scraping {len(RACE_IDS)} pages in: {(end_time - start_time)/60} minutes.")


if __name__ == "__main__":
    scrape()
