import pandas as pd
import requests
from bs4 import BeautifulSoup

def scrape_race_by_id(id):
    print(id)

if __name__ == '__main__':
    upper_bound = 10 # Change to number of races to scrape
    for id in range(upper_bound):
        scrape_race_by_id(id)
