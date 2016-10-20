import requests
import Player_batting as Bat
import re
from pathos.multiprocessing import Pool  # This is a thread-based Pool
from bs4 import BeautifulSoup
import time
import mlb_site_dictionary as dic
import mlb_db_queries as quer

PLAYER_SITE_LINK_KEY = ('a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z')

def scrape_player(player_site, page_key):
    complete_player_list = []
    final_player_list = []
    for key in page_key:
        print('Scanning {}'.format(key))
        page_num_html = setup_scraper(player_site.format(key))
        player_data = page_num_html.find_all('pre')
        dirty_active_player_list = [player.find_all('b') for player in player_data if player.find_all('b')]
        clean_list = flatten(dirty_active_player_list)
        for player in clean_list:
            complete_player_list.append(player)
        for player in clean_list:
            link = 'http://www.baseball-reference.com' + re.findall(r'"([^"]*)"', str(player))[0]
            player_alias = link.split('/')[-1].split('.')[0]
            full_name = re.findall(r'">[^*]*?<', str(player))[0][2:-1]
            if len(full_name.split()) >= 2:
                fn = full_name.split()[0]
                ln = ' '.join(full_name.split()[1:])
            else:
                fn = None
                ln = full_name
            final_player_list.append((link, player_alias, fn, ln))
    return final_player_list

def setup_scraper(link_dictionary):
    raw_html = requests.get(link_dictionary).content
    time.sleep(3)
    return BeautifulSoup(raw_html, 'html5lib').body

def flatten(dirty_list):
    clean_list = []
    for sub_list in dirty_list:
        if not isinstance(sub_list, list):
            clean_list.append(sub_list)
        else:
            clean_list.extend(flatten(sub_list))
    return clean_list

def scrape_bat(player):
    from bs4 import BeautifulSoup
    import time
    import requests
    import mlb_site_dictionary as dic
    link = dic.link_dictionary['player_batting'].format(player[1][0], player[1])
    html = str(BeautifulSoup(requests.get(link).content, 'html5lib').body)
    time.sleep(3)
    print(player[1] + ' Has been Scanned')
    return player[0], player[1], html, link

start_time = time.time()

# Gets All Active Players
player_record = scrape_player(dic.link_dictionary['player_id'] , PLAYER_SITE_LINK_KEY)

# Inserts Players into database
quer.execute_query(quer.insert_queries['player_id'], records=player_record, is_insert=True)

# Queries for players for table scraping
players = quer.execute_query(query, results=True)

# Multi-Processing for scraping batting tables
pool = Pool(6)
batting_html = pool.map(scrape_bat, players)

# Creats player_batting objects
for player in batting_html:
    Bat.Player_batting(player[0],player[1],player[2], player[3])

# Builds out player batting tables and loads them into database
for player in Bat.Player_batting.instances:
    player.parse_tables()
    try:
        player.write_to_db(player.batting_standard)
        player.write_to_db(player.batting_value)
        player.write_to_db(player.batting_advanced)
        player.write_to_db(player.batting_postseason)
        player.write_to_db(player.batting_allstar)
        player.write_to_db(player.batting_ratio)
        player.write_to_db(player.batting_win_probability)
        player.write_to_db(player.batting_baserunning)
        player.write_to_db(player.batting_situational)
        player.write_to_db(player.batting_pitches)
        player.write_to_db(player.cumulative_batting)
    except AttributeError:
        pass

print("--- %s seconds ---" % (time.time() - start_time))