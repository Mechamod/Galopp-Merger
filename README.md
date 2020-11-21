# Galopp-Merger
### Horse ranker based on the history of the webpage galopp-statistik.de
Galopp-Merger is a project divided into multiple scripts for each step of the machine learning process (See the _Notes_ folder for a comprehensive explanation of the whole project)

### Project workflow
Roughly it follows the following steps:
- Scrape data from galopp-statistik.de
- Clean data
- Train a model that ranks horses in a way that the order of winners can be determined
- Improvement ideas (Only theoretically)

### Contents
The contents of this repository are organized as...:

  - galopp-scraper.py: Scrapes the races in a given range of id's and saves them into multiple csv files (Why? See the _Notes_ folder)
  - galopp-merger.py: Merges the different csv files into one
  - Notes/Notes.md: My plans and notes of developing this script

### Installation

The script requires Python3 to run.
Install additional dependencies from the requirements.txt file and run the various scripts in order as needed.

```sh
$ pip3 install -r requirements.txt
$ python3 [script].py
```

### Donations

BTC: 1DixZsj9HdRMCD16co1BbhXfJoaUrEptcE   
ETH: 0xf5d23ad5b592a6f078ca18aa5eecc55edb1ce532  
<a href="https://paypal.me/Mechamod">
  <img src="https://raw.githubusercontent.com/stefan-niedermann/paypal-donate-button/master/paypal-donate-button.png" alt="Donate with PayPal" width="170"/>
</a>

[//]: # (These are reference links used in the body)
   [BeautifulSoup]: <https://www.crummy.com/software/BeautifulSoup/>
