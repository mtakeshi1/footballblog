import requests
from bs4 import BeautifulSoup
import os
import time


sleep_time = 10

def fetch_player(url):
    print('starting fetch player for ' + url)
    soup = BeautifulSoup(requests.get(url).text, 'html.parser')
    time.sleep(sleep_time)
    complete = [a['href'] for a in soup.find_all('a') if a.text == 'View Complete Scouting Report']
    print('complete scout: ' + str(complete))
    if len(complete) == 0:
        return ''
    page = requests.get('https://fbref.com' + complete[0])
    time.sleep(sleep_time)
    soup = BeautifulSoup(page.text, 'html.parser')
    attribs = [row.contents[0].text.strip() + ',' + row.contents[1]['csk'] +',' +row.contents[2]['csk'] for table in soup.find_all('table') for row in table.find_all('tr') if len(row.contents) == 3 and row.contents[0].text.strip() != '']
    
    return '\n'.join(attribs)

def fetch_players_for(name, url):
    page = requests.get(url)
    time.sleep(sleep_time)
    soup = BeautifulSoup(page.text, 'html.parser')
    rows = soup.find_all('th', {'class':'left', 'scope':'row', 'data-stat':'player'})
    players = set([c for c in rows if c.has_attr('csk') and len(c.contents) == 1 and c.contents[0].has_attr('href') ])
    print('players found: ' + str(len(players)))
    if len(players) < 10:
        return
    player_files = ['player,url,position\n']
    folder = 'players/' + name
    if not os.path.exists(folder):
        os.makedirs(folder)
    for player in players:
        player_csv = fetch_player('https://fbref.com' + player.contents[0]['href'])
        if player_csv == '':
            continue
        player_name = player.contents[0].text
        file_name = folder + '/' + player_name.replace(' ', '_').replace(',', '_').lower() + '.csv'
        position = [c.text.replace(',', '') for c in player.parent.find_all('td', {'data-stat':'position'})][0]
        with open(file_name, 'w') as player_file:
            player_file.write(player_csv)
        player_files.append(player_name + ',' + file_name + ',' + position +'\n')
    print('\n'.join(player_files))
    with open(folder + '/players.csv', 'w') as player_list:
        player_list.writelines(player_files)


if __name__ == '__main__':
    for line in open('_data/teams.csv', 'r').readlines()[1:]:
        team, url = line.split(',')
        print('downloading: {}'.format(team))
        fetch_players_for(team, url)
