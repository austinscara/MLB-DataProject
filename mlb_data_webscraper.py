import requests
import itertools
import html5lib
import re
import pymysql
from multiprocessing.dummy import Pool  # This is a thread-based Pool
from multiprocessing import cpu_count
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import os
import csv

import mlb_site_dictionary as dic
import mlb_db_queries as quer

import ipdb

PLAYER_SITE_LINK_KEY = ('a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z')

def player_id_scraper(player_site, page_key):
    complete_player_list = []
    final_player_list = []
    for key in page_key:
        print('Scanning {}'.format(key))
        page_num_html = setup_scraper(player_site.format(key))
        player_data = page_num_html.find_all('pre')
        dirty_player_list = [player.find_all('a') for player in player_data]
        clean_list = (flatten(dirty_player_list))
        for player in clean_list:
            complete_player_list.append(player)

        for player in clean_list:
            link = 'http://www.baseball-reference.com' + re.findall(r'"([^"]*)"', str(player))[0]
            player_alias = link.split('/')[-1].split('.')[0]
            fn =  re.findall(r'>([^"]*)<', str(player))[0].split()[0]
            try:
                ln = re.findall(r'>([^"]*)<', str(player))[0].split()[1]
            except IndexError:
                ln = fn
                fn = None

            final_player_list.append((link, player_alias, fn, ln))
    return final_player_list

def scrape_team_code(all_team_site):
    final_team_list = []
    all_team_html = setup_scraper(all_team_site.format(''))
    league_type = {'active':'MLB', 'defunct':'Earlier Francises', 'na':'National Association'}
    for status in league_type:
        franchise = all_team_html.find('table', {'id': status})
        raw_active_team = franchise.find_all('td', {'class', 'franchise_names'})
        for team in raw_active_team:
            team_link = 'http://www.baseball-reference.com' + re.findall(r'/teams/...', str(team))[0]
            team_code = team.find('a')['href'][-4:-1]
            team_name = team.get_text().replace("'", "")
            team_league = league_type[status]
            final_team_list.append((team_link, team_code, team_name, team_league))
    return final_team_list

def flatten(dirty_list):
        clean_list = []
        for sub_list in dirty_list:
            if not isinstance(sub_list, list):
                clean_list.append(sub_list)
            else:
                clean_list.extend(flatten(sub_list))
        return clean_list

def setup_scraper(link_dictionary):
    raw_html = requests.get(link_dictionary).content
    time.sleep(3)
    return BeautifulSoup(raw_html, 'html5lib').body

def scrape_player_batting(batting_site):
    # html table : id
    chrome_profile = Options()
    download_location = {"download.default_directory": r"C:\Users\Austi\Documents\MLB DataProject\MLB_Data_CSV_Files"}
    chrome_profile.add_experimental_option("prefs", download_location)
    chrome_profile.add_argument("user-data-dir=C:/Users/Austi/AppData/Local/Google/Chrome/User Data/Default")

    batting_tables = {
          'player_batting_standard': "sr_download_data('batting_standard'); try {ga('send', 'event', 'Tool', 'Action', 'Export');} catch (err) {}"
        , 'player_batting_value': "sr_download_data('batting_value'); try {ga('send', 'event', 'Tool', 'Action', 'Export');} catch (err) {}"
        , 'player_batting_advanced': "sr_download_data('batting_advanced'); try {ga('send', 'event', 'Tool', 'Action', 'Export');} catch (err) {}"
        , 'player_batting_post_season': "sr_download_data('batting_postseason'); try {ga('send', 'event', 'Tool', 'Action', 'Export');} catch (err) {}"
        , 'player_batting_star': "sr_download_data('batting_allstar'); try {ga('send', 'event', 'Tool', 'Action', 'Export');} catch (err) {}"
        , 'player_batting_ratio': "sr_download_data('batting_ratio'); try {ga('send', 'event', 'Tool', 'Action', 'Export');} catch (err) {}"
        , 'player_batting_win_prob': "sr_download_data('batting_win_probability'); try {ga('send', 'event', 'Tool', 'Action', 'Export');} catch (err) {}"
        , 'player_batting_baserunning': "sr_download_data('batting_baserunning'); try {ga('send', 'event', 'Tool', 'Action', 'Export');} catch (err) {}"
        , 'player_batting_situational': "sr_download_data('batting_situational'); try {ga('send', 'event', 'Tool', 'Action', 'Export');} catch (err) {}"
        , 'player_batting_pitches': "sr_download_data('batting_pitches'); try {ga('send', 'event', 'Tool', 'Action', 'Export');} catch (err) {}"
        , 'player_batting_cumulative': "sr_download_data('cumulative_batting'); try {ga('send', 'event', 'Tool', 'Action', 'Export');} catch (err) {}"}

    query = 'SELECT id, player_alias FROM player WHERE id in (8344, 15977, 17443);'
    players = quer.execute_query(query, results=True)
    print(players)

    scrape_link_list = {pl[0] : batting_site.format(pl[1][0],pl[1]) for pl in players}
    print(scrape_link_list)

    for ids in scrape_link_list:
        driver = webdriver.Chrome(r"C:\Users\Austi\Documents\MLB DataProject\chromedriver\chromedriver.exe", chrome_options=chrome_profile)
        driver.implicitly_wait(10)
        driver.get(scrape_link_list[ids])
        for tbl in batting_tables:
            print(tbl)
            try:
                driver.execute_script(batting_tables[tbl])
            except:
                print(tbl + ' Not Available for ' + scrape_link_list[ids])
        time.sleep(2)
        driver.quit()
    return None


def read_csv(fl):
    with open(fl, encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile, delimiter=",")
        row_data = []
        for row in reader:
            row_data.append(row)
    return row_data

def write_csv(fl, data):
    with open(r'C:\Users\Austi\Documents\MLB DataProject\MLB_Data_CSV_Files\\' + fl, 'w', newline='', encoding='utf-8') as write_file:
        writer = csv.writer(write_file)
        for row in data:
            writer.writerow(row)
    return None

def clean_cells(data):
    for cell in data:
        cell[0] = ''.join(num for num in cell[0] if num.isdigit())
    for row in data:
        for cell in row:
            if '%' in cell:
                row[row.index(cell)] = str(float(cell.strip('%'))/100)
        else:
            pass
    return data

def clean_player_batting():
    csv_dir = r'C:\Users\Austi\Documents\MLB DataProject\MLB_Data_CSV_Files\\'
    for batting_file in os.listdir(csv_dir):
        raw_row = read_csv(csv_dir + batting_file)
        print(batting_file)

        first_row = []
        last_row = []

        raw_row = [row for row in raw_row if row and row[0] != '']

        for row in raw_row:
            if row and row[0] == 'Year':
                first_row.append(raw_row.index(row) + 1)
            else:
                pass

        for row in raw_row:
            if row and ('Yrs' in row[0] or 'Yr' in row[0] or 'Seasons' in row[0] or 'Season' in row[0]):
                last_row.append(raw_row.index(row))
            else:
                pass

        if not last_row:
            last_row.append(raw_row.index(raw_row[-1]) + 1)

        clean_rows = clean_cells(raw_row[first_row[0]:last_row[0]])
        write_csv(batting_file, clean_rows)
    return None



# quer.execute_query(quer.insert_queries['player_id'], records=player_id_scraper(dic.link_dictionary['player_id'], PLAYER_SITE_LINK_KEY), is_insert=True)
# connection, mssql_cursor = quer.temp_table_creator(scrape_team_code(dic.link_dictionary['team_id']), dic.data_type_dict['team_id'])
# quer.execute_query(quer.insert_queries['team_id'], connection, mssql_cursor)

# scrape_player_batting(dic.link_dictionary['player_batting'])
clean_player_batting()
# prep_player_batting

#TODO: load batting data in to database

