import requests
import Player_batting as Bat
import re
from pathos.multiprocessing import Pool  # This is a thread-based Pool
from bs4 import BeautifulSoup
import time
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
    time.sleep(4)
    print(player[1] + ' Has been Scanned')
    return player[0], player[1], html, link

def write_bat(batting_html):
    # Creats player_batting objects
    for player in batting_html:
        player_instance = Bat.Player_batting(player[0], player[1], player[2], player[3])
        print(player_instance.link)
        player_instance.parse_html(player_instance.raw_html)
        player_instance.parse_tables()
        try:
            player_instance.write_to_db(player_instance.batting_standard)
        except:
            print('error at test Batting Standard')
            pass
        try:
            player_instance.write_to_db(player_instance.batting_value)
        except:
            print('error at test Batting Value')
            pass
        try:
            player_instance.write_to_db(player_instance.batting_advanced)
        except:
            print('error at test Batting Advanced')
            pass
        try:
            player_instance.write_to_db(player_instance.batting_postseason)
        except:
            print('error at test Batting Postseason')
            pass
        try:
            player_instance.write_to_db(player_instance.batting_allstar)
        except:
            print('error at test Batting Allstar')
            pass
        try:
            player_instance.write_to_db(player_instance.batting_ratio)
        except:
            print('error at test Batting Ratio')
            pass
        try:
            player_instance.write_to_db(player_instance.batting_win_probability)
        except:
            print('error at test Batting win Probablility')
            pass
        try:
            player_instance.write_to_db(player_instance.batting_baserunning)
        except:
            print('error at test Batting Baserunning')
            pass
        try:
            player_instance.write_to_db(player_instance.batting_situational)
        except:
            print('error at test Batting Situational')
            pass
        try:
            player_instance.write_to_db(player_instance.batting_pitches)
        except:
            print('error at test Batting Pitches')
            pass
        try:
            player_instance.write_to_db(player_instance.cumulative_batting)
        except:
            print('error at test Cumulative Batting')
            pass
    return None

def main():
    start_time = time.time()

    # Gets All Active Players
    # player_record = scrape_player(dic.link_dictionary['player_id'] , PLAYER_SITE_LINK_KEY)

    # Inserts Players into database
    # quer.execute_query(quer.insert_queries['player_id'], records=player_record, is_insert=True)

    # Queries for players for table scraping
    query = "SELECT id, player_alias from player;"
    players = quer.execute_query(query, results=True)

    # Multi-Processing for scraping batting tables
    pool = Pool(5)
    batting_html = pool.map(scrape_bat, players)
    print('scanning done')
    write_bat(batting_html)

    print("--- %s seconds ---" % (time.time() - start_time))

if __name__ == "__main__":
    main()