import requests
from bs4 import BeautifulSoup
import os
from datetime import datetime, date, time, timezone
import time


def fetch_from(url):
    user_agent = {'User-agent': 'Mozilla/5.0'}
    page = requests.get(url, headers=user_agent)
    soup = BeautifulSoup(page.text, 'html.parser')
    rows = soup.find_all('th', {'class':'left', 'scope':'row', 'data-stat':'player'})
    return set([c for c in rows if c.has_attr('csk') and len(c.contents) == 1 and c.contents[0].has_attr('href') ])


if __name__ == '__main__':
    players = fetch_from('https://fbref.com/en/squads/bf4acd28/Corinthians-Stats')
    sl = 1
    while True:
        print('{} : {}'.format(str(datetime.now()), str(len(players))))
        players = fetch_from('https://fbref.com/en/squads/bf4acd28/Corinthians-Stats')
        if len(players) == 0:
            time.sleep(60)
