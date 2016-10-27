from bs4 import BeautifulSoup
import mlb_db_queries as quer
import pickle


class Player_batting(object):
    instances = []

    def __init__(self, player_id, player_alias, raw_html, link):
        self.player_id = player_id
        self.player_alias = player_alias
        self.link  = "'" + link + "'"
        self.raw_html = raw_html
        self.html = None
        self.cumulative_html = None
        self.batting_standard = None
        self.batting_value = None
        self.batting_advanced = None
        self.batting_postseason = None
        self.batting_allstar = None
        self.batting_ratio = None
        self.batting_win_probability = None
        self.batting_baserunning = None
        self.batting_situational = None
        self.batting_pitches = None
        self.cumulative_batting = None
        Player_batting.instances.append(self)

    def parse_html(self, data):
        #TODO make function that converts processed html to html
        self.html = BeautifulSoup(data, 'html5lib').body.find('div', id='all_batting').find_all('tr', {'class': 'full'})
        self.cumulative_html = BeautifulSoup(data, 'html5lib').body.find('div', id='all_batting').find('table', id='cumulative_batting').find('tbody').find_all('tr')
        return None

    # Creates all Tables
    def parse_tables(self):
        self.batting_standard = {'batting_standard': self.clean_batting_standard(self.capture_player_batting_standard())}
        self.batting_value = {'batting_value': self.clean_batting_value(self.capture_player_batting_value())}
        self.batting_advanced = {'batting_advanced':  self.clean_batting_advanced(self.capture_player_batting_advanced())}
        # self.batting_postseason = {'batting_postseason':  self.clean_batting_postseason(self.capture_player_batting_post_season())}
        self.batting_ratio = {'batting_ratio': self.clean_batting_ratio(self.capture_player_batting_ratio())}
        self.batting_win_probability = {'batting_win_prob': self.clean_batting_win_probability(self.capture_player_batting_win_prob())}
        self.batting_baserunning = {'batting_baserunning': self.clean_batting_baserunning(self.capture_player_batting_baserunning())}
        self.batting_situational = {'batting_situational': self.clean_batting_situational(self.capture_player_batting_situational())}
        self.batting_pitches = {'batting_pitches': self.clean_batting_pitches(self.capture_player_batting_pitches())}
        self.cumulative_batting = {'batting_cumulative': self.clean_cumulative_batting(self.capture_player_batting_cumulative())}
        return None

    # Capture Tables from self.html
    def capture_player_batting_standard(self):
        batting_data = [[data.text.strip() for data in item.find_all('td')] for item in self.html if item.get('id').startswith('batting_standard')]
        return batting_data
    def capture_player_batting_value(self):
         batting_data = [[data.text.strip() for data in item.find_all('td')] for item in self.html if item.get('id').startswith('batting_value')]
         return batting_data
    def capture_player_batting_advanced(self):
         batting_data = [[data.text.strip() for data in item.find_all('td')] for item in self.html if item.get('id').startswith('batting_advanced')]
         return batting_data
    def capture_player_batting_post_season(self):
         batting_data = [[data.text.strip() for data in item.find_all('td')] for item in self.html if item.get('id').startswith('batting_postseason')]
         return batting_data
    def capture_player_batting_ratio(self):
         batting_data = [[data.text.strip() for data in item.find_all('td')] for item in self.html if item.get('id').startswith('batting_ratio')]
         return batting_data
    def capture_player_batting_win_prob(self):
         batting_data = [[data.text.strip() for data in item.find_all('td')] for item in self.html if item.get('id').startswith('batting_win_probability')]
         return batting_data
    def capture_player_batting_baserunning(self):
         batting_data = [[data.text.strip() for data in item.find_all('td')] for item in self.html if item.get('id').startswith('batting_baserunning')]
         return batting_data
    def capture_player_batting_situational(self):
         batting_data = [[data.text.strip() for data in item.find_all('td')] for item in self.html if item.get('id').startswith('batting_situational')]
         return batting_data
    def capture_player_batting_pitches(self):
         batting_data = [[data.text.strip() for data in item.find_all('td')] for item in self.html if item.get('id').startswith('batting_pitches')]
         return batting_data
    def capture_player_batting_cumulative(self):
         dirty_rows = [data.find_all('td') for data in self.cumulative_html]
         clean_rows = [[item.text.strip() for item in row] for row in dirty_rows]
         batting_data = clean_rows
         return batting_data


         # Cleans tables that were captured used DDL to format

    def clean_batting_standard(self, rows):
        clean_items = []
        for item in rows:
            item[0] = int(item[0][:4])
            item[1] = int(0 if item[1] == ('' or '0.0' or '-0.0' or '0.0%') else item[1])
            item[2] = str("'" + item[2] + "'")
            item[3] = str("'" + item[3] + "'")
            item[4] = int(0 if item[4] == ('' or '0.0' or '-0.0' or '0.0%') else item[4])
            item[5] = int(0 if item[5] == ('' or '0.0' or '-0.0' or '0.0%') else item[5])
            item[6] = int(0 if item[6] == ('' or '0.0' or '-0.0' or '0.0%') else item[6])
            item[7] = int(0 if item[7] == ('' or '0.0' or '-0.0' or '0.0%') else item[7])
            item[8] = int(0 if item[8] == ('' or '0.0' or '-0.0' or '0.0%') else item[8])
            item[9] = int(0 if item[9] == ('' or '0.0' or '-0.0' or '0.0%') else item[9])
            item[10] = int(0 if item[10] == ('' or '0.0' or '-0.0' or '0.0%') else item[10])
            item[11] = int(0 if item[11] == ('' or '0.0' or '-0.0' or '0.0%') else item[11])
            item[12] = int(0 if item[12] == ('' or '0.0' or '-0.0' or '0.0%') else item[12])
            item[13] = int(0 if item[13] == ('' or '0.0' or '-0.0' or '0.0%') else item[13])
            item[14] = int(0 if item[14] == ('' or '0.0' or '-0.0' or '0.0%') else item[14])
            item[15] = int(0 if item[15] == ('' or '0.0' or '-0.0' or '0.0%') else item[15])
            item[16] = int(0 if item[16] == ('' or '0.0' or '-0.0' or '0.0%') else item[16])
            item[17] = float(0 if item[17] == ('') else item[17])
            item[18] = float(0 if item[18] == ('') else item[18])
            item[19] = float(0 if item[19] == ('') else item[19])
            item[20] = float(0 if item[20] == ('') else item[20])
            item[21] = int(0 if item[21] == ('') else item[21])
            item[22] = int(0 if item[22] == ('' or '0.0' or '-0.0' or '0.0%') else item[22])
            item[23] = int(0 if item[23] == ('' or '0.0' or '-0.0' or '0.0%') else item[23])
            item[24] = int(0 if item[24] == ('' or '0.0' or '-0.0' or '0.0%') else item[24])
            item[25] = int(0 if item[25] == ('' or '0.0' or '-0.0' or '0.0%') else item[25])
            item[26] = int(0 if item[26] == ('' or '0.0' or '-0.0' or '0.0%') else item[26])
            item[27] = int(0 if item[27] == ('' or '0.0' or '-0.0' or '0.0%') else item[27])
            item[28] = str("'" + item[28] + "'")
            item[29] = str("'" + item[29] + "'")
            clean_items.append([self.player_id, self.link] + item)
        return clean_items
    def clean_batting_value(self, rows):
        clean_items = []
        for item in rows:
            item[0] = int(item[0][:4])
            item[1] = int(0 if item[1] == ('' or '0.0' or '-0.0' or '0.0%') else item[1])
            item[2] = str("'" + item[2] + "'")
            item[3] = str("'" + item[3] + "'")
            item[4] = int(0 if item[4] == ('' or '0.0' or '-0.0' or '0.0%') else item[4])
            item[5] = int(0 if item[5] == ('' or '0.0' or '-0.0' or '0.0%') else item[5])
            item[6] = int(0 if item[6] == ('' or '0.0' or '-0.0' or '0.0%') else item[6])
            item[7] = int(0 if item[7] == ('' or '0.0' or '-0.0' or '0.0%') else item[7])
            item[8] = int(0 if item[8] == ('' or '0.0' or '-0.0' or '0.0%') else item[8])
            item[9] = int(0 if item[9] == ('' or '0.0' or '-0.0' or '0.0%') else item[9])
            item[10] = int(0 if item[10] == ('' or '0.0' or '-0.0' or '0.0%') else item[10])
            item[11] = int(0 if item[11] == ('' or '0.0' or '-0.0' or '0.0%') else item[11])
            item[12] = float(0 if item[12] == ('' or '0.0' or '-0.0' or '0.0%')  else item[12])
            item[13] = int(0 if item[13] == ('' or '0.0' or '-0.0' or '0.0%') else item[13])
            item[14] = int(0 if item[14] == ('' or '0.0' or '-0.0' or '0.0%') else item[14])
            item[15] = float(0 if item[15] == ('') else item[15])
            item[16] = float(0 if item[16] == ('') else item[16])
            item[17] = float(0 if item[17] == ('') else item[17])
            item[18] = float(0 if item[18] == ('') else item[18])
            item[19] = float(0 if item[19] == ('') else item[19])
            item[20] = int(0 if item[20] == ('' or '0.0' or '-0.0' or '0.0%') else item[20])
            item[21] = str("'" + item[21] + "'")
            item[22] = str("'" + item[22] + "'")
            item[23] = str("'" + item[23] + "'")
            clean_items.append([self.player_id, self.link] + item)
        return clean_items
    def clean_batting_advanced(self, rows):
        clean_items = []
        for item in rows:
            item[0] = int(item[0][:4])
            item[1] = int(0 if item[1] == ('' or '0.0' or '-0.0' or '0.0%') else item[1])
            item[2] = str("'" + item[2] + "'")
            item[3] = str("'" + item[3] + "'")
            item[4] = int(0 if item[4] == ('' or '0.0' or '-0.0' or '0.0%') else item[4])
            item[5] = int(0 if item[5] == ('' or '0.0' or '-0.0' or '0.0%') else item[5])
            item[6] = int(0 if item[6] == ('' or '0.0' or '-0.0' or '0.0%') else item[6])
            item[7] = float(0 if item[7] == ('') else item[7])
            item[8] = int(0 if item[8] == ('' or '0.0' or '-0.0' or '0.0%') else item[8])
            item[9] = float(0 if item[9] == ('') else item[9])
            item[10] = float(0 if item[10] == ('') else item[10])
            item[11] = float(0 if item[11] == ('') else item[11])
            item[12] = float(0 if item[12] == ('') else item[12])
            item[13] = float(0 if item[13] == ('') else item[13])
            item[14] = float(0 if item[14] == ('') else item[14])
            item[15] = float(0 if item[15] == ('') else item[15])
            item[16] = float(0 if item[16] == ('') else item[16])
            item[17] = float(0 if item[17] == ('') else item[17])
            item[18] = int(0 if item[18] == ('' or '0.0' or '-0.0' or '0.0%') else item[18])
            item[19] = float(0 if item[19] == ('') else item[19])
            item[20] = float(0 if item[20] == ('') else item[20])
            item[21] = float(0 if item[21] == ('') else item[21])
            item[22] = float(0 if item[22] == ('') else item[22])
            item[23] = float(0 if item[23] == ('') else item[23])
            item[24] = float(0 if item[24] == ('') else item[24])
            item[25] = float(0 if item[25] == ('') else item[25])
            clean_items.append([self.player_id, self.link] + item)
        return clean_items
    #TODO: Need to fix the casting of this table
    def clean_batting_postseason(self, rows):
        clean_items = []
        # print(rows)
        for item in rows:
            item[0] = int(item[0][:4])
            item[1] = int(0 if item[1] == '' or '0.0' or '-0.0' or '0.0%' else item[1])
            item[2] = str("'" + item[2] + "'")
            item[3] = str("'" + item[3] + "'")
            item[4] = str("'" + item[4] + "'")
            item[5] = str("'" + item[5] + "'")
            item[6] = str("'" + item[6] + "'")
            item[7] = int(0 if item[7] == ('' or '0.0' or '-0.0' or '0.0%') else item[7])
            item[8] = int(0 if item[8] == ('' or '0.0' or '-0.0' or '0.0%') else item[8])
            item[9] = int(0 if item[9] == ('' or '0.0' or '-0.0' or '0.0%') else item[9])
            item[10] = int(0 if item[10] == ('' or '0.0' or '-0.0' or '0.0%') else item[10])
            item[11] = int(0 if item[11] == ('' or '0.0' or '-0.0' or '0.0%') else item[11])
            item[12] = int(0 if item[12] == ('' or '0.0' or '-0.0' or '0.0%') else item[12])
            item[13] = int(0 if item[13] == ('' or '0.0' or '-0.0' or '0.0%') else item[13])
            item[14] = int(0 if item[14] ==('' or '0.0' or '-0.0' or '0.0%')  else item[14])
            item[15] = int(0 if item[15] == ('' or '0.0' or '-0.0' or '0.0%') else item[15])
            item[16] = int(0 if item[16] == ('' or '0.0' or '-0.0' or '0.0%') else item[16])
            item[17] = int(0 if item[17] == ('' or '0.0' or '-0.0' or '0.0%') else item[17])
            item[18] = int(0 if item[18] == ('' or '0.0' or '-0.0' or '0.0%') else item[18])
            item[19] = int(0 if item[19] == ('' or '0.0' or '-0.0' or '0.0%') else item[19])
            item[20] = float(0 if item[20] == '' else item[20][:-1])
            item[21] = float(0 if item[21] == '' else item[21][:-1])
            item[22] = float(0 if item[22] == '' else item[22][:-1])
            item[23] = float(0 if item[23] == '' else item[23][:-1])
            item[24] = int(0 if item[24] == ('' or '0.0' or '-0.0' or '0.0%') else item[24])
            item[25] = int(0 if item[25] == ('' or '0.0' or '-0.0' or '0.0%') else item[25])
            item[26] = int(0 if item[26] == ('' or '0.0' or '-0.0' or '0.0%') else item[26])
            item[27] = int(0 if item[27] == ('' or '0.0' or '-0.0' or '0.0%') else item[27])
            item[28] = int(0 if item[28] ==('' or '0.0' or '-0.0' or '0.0%')  else item[28])
            item[29] = int(0 if item[29] == ('' or '0.0' or '-0.0' or '0.0%') else item[29])
            # print(item)
            clean_items.append([self.player_id, self.link] + item)
        return clean_items
    def clean_batting_ratio(self, rows):
        clean_items = []
        for item in rows:
            item[0] = int(item[0][:4])
            item[1] = int(0 if item[1] == ('' or '0.0' or '-0.0' or '0.0%') else item[1])
            item[2] = str("'" + item[2] + "'")
            item[3] = str("'" + item[3] + "'")
            item[4] = int(0 if item[4] == ('' or '0.0' or '-0.0' or '0.0%') else item[4])
            item[5] = float(0 if item[5] == '' else item[5][:-1])
            item[6] = float(0 if item[6] == '' else item[6][:-1])
            item[7] = float(0 if item[7] == '' else item[7][:-1])
            item[8] = float(0 if item[8] == '' else item[8][:-1])
            item[9] = float(0 if item[9] == '' else item[9][:-1])
            item[10] = float(0 if item[10] == '' else item[10])
            item[11] = float(0 if item[11] == '' else item[11])
            item[12] = float(0 if item[12] == '' else item[12])
            item[13] = float(0 if item[13] == '' else item[13])
            item[14] = float(0 if item[14] == '' else item[14])
            item[15] = float(0 if item[15] == '' else item[15])
            item[16] = float(0 if item[16] == '' else item[16][:-1])
            item[17] = float(0 if item[17] == '' else item[17][:-1])
            item[18] = float(0 if item[18] == '' else item[18][:-1])
            item[19] = float(0 if item[19] == '' else item[19][:-1])
            clean_items.append([self.player_id, self.link] + item)
        return clean_items
    def clean_batting_win_probability(self, rows):
        clean_items = []
        for item in rows:
            item[0] = int(item[0][:4])
            item[1] = int(0 if item[1] == ('' or '0.0' or '-0.0' or '0.0%') else item[1])
            item[2] = str("'" + item[2] + "'")
            item[3] = str("'" + item[3] + "'")
            item[4] = float(0 if item[4] == '' else item[4])
            item[5] = float(0 if item[5] == '' else item[5])
            item[6] = int(0 if item[6] == '' else item[6])
            item[7] = float(0 if item[7] == '' else item[7])
            item[8] = float(0 if item[8] == '' else item[8])
            item[9] = float(0 if item[9] == '' else item[9])
            item[10] = float(0 if item[10] == '' else item[10])
            item[11] = float(0 if item[11] == '' else item[11])
            item[12] = float(0 if item[12] == '' else item[12])
            item[13] = float(0 if item[13] == '' else item[13])
            item[14] = float(0 if item[14] == '' else item[14])
            item[15] = float(0 if item[15] == '' else item[15])
            item[16] = float(0 if item[16] == '' else item[16])
            item[17] = float(0 if item[17] == '' else item[17])
            item[18] = int(0 if item[18] == ('' or '0.0' or '-0.0' or '0.0%') else item[18])
            clean_items.append([self.player_id, self.link] + item)
        return clean_items
    def clean_batting_baserunning(self, rows):
        clean_items = []
        for item in rows:
            item[0] = int(item[0][:4])
            item[1] = int(0 if item[1] == ('' or '0.0' or '-0.0' or '0.0%') else item[1])
            item[2] = str("'" + item[2] + "'")
            item[3] = str("'" + item[3] + "'")
            item[4] = int(0 if item[4] == ('' or '0.0' or '-0.0' or '0.0%') else item[4])
            item[5] = int(0 if item[5] == ('' or '0.0' or '-0.0' or '0.0%') else item[5])
            item[6] = float(0 if item[6] == '' else item[6][:-1])
            item[7] = int(0 if item[7] == ('' or '0.0' or '-0.0' or '0.0%') else item[7])
            item[8] = int(0 if item[8] == ('' or '0.0' or '-0.0' or '0.0%') else item[8])
            item[9] = int(0 if item[9] == ('' or '0.0' or '-0.0' or '0.0%') else item[9])
            item[10] = float(0 if item[10] == '' else item[10][:-1])
            item[11] = int(0 if item[11] == ('' or '0.0' or '-0.0' or '0.0%') else item[11])
            item[12] = int(0 if item[12] == ('' or '0.0' or '-0.0' or '0.0%') else item[12])
            item[13] = int(0 if item[13] == ('' or '0.0' or '-0.0' or '0.0%') else item[13])
            item[14] = int(0 if item[14] == ('' or '0.0' or '-0.0' or '0.0%') else item[14])
            item[15] = int(0 if item[15] == ('' or '0.0' or '-0.0' or '0.0%') else item[15])
            item[16] = int(0 if item[16] == ('' or '0.0' or '-0.0' or '0.0%') else item[16])
            item[17] = int(0 if item[17] == ('' or '0.0' or '-0.0' or '0.0%') else item[17])
            item[18] = int(0 if item[18] == ('' or '0.0' or '-0.0' or '0.0%') else item[18])
            item[19] = int(0 if item[19] == ('' or '0.0' or '-0.0' or '0.0%') else item[19])
            item[20] = int(0 if item[20] == ('' or '0.0' or '-0.0' or '0.0%') else item[20])
            item[21] = int(0 if item[21] == ('' or '0.0' or '-0.0' or '0.0%') else item[21])
            item[22] = int(0 if item[22] == ('' or '0.0' or '-0.0' or '0.0%') else item[22])
            item[23] = int(0 if item[23] == ('' or '0.0' or '-0.0' or '0.0%') else item[23])
            item[24] = int(0 if item[24] == ('' or '0.0' or '-0.0' or '0.0%') else item[24])
            item[25] = float(0 if item[25] == ''  else item[25][:-1])
            item[26] = int(0 if item[26] == ('' or '0.0' or '-0.0' or '0.0%') else item[26])
            item[27] = int(0 if item[27] == ('' or '0.0' or '-0.0' or '0.0%') else item[27])
            item[28] = int(0 if item[28] == ('' or '0.0' or '-0.0' or '0.0%') else item[28])
            item[29] = int(0 if item[29] == ('' or '0.0' or '-0.0' or '0.0%') else item[29])
            item[30] = int(0 if item[30] == ('' or '0.0' or '-0.0' or '0.0%') else item[30])
            item[31] = int(0 if item[31] == ('' or '0.0' or '-0.0' or '0.0%') else item[31])
            item[32] = int(0 if item[32] == ('' or '0.0' or '-0.0' or '0.0%') else item[32])
            item[33] = int(0 if item[33] == ('' or '0.0' or '-0.0' or '0.0%') else item[33])
            item[34] = int(0 if item[34] == ('' or '0.0' or '-0.0' or '0.0%') else item[34])
            clean_items.append([self.player_id, self.link] + item)
        return clean_items
    def clean_batting_situational(self, rows):
        clean_items = []
        for item in rows:
            item[0] = int(item[0][:4])
            item[1] = int(0 if item[1] == ('' or '0.0' or '-0.0' or '0.0%') else item[1])
            item[2] = str("'" + item[2] + "'")
            item[3] = str("'" + item[3] + "'")
            item[4] = int(0 if item[4] == ('' or '0.0' or '-0.0' or '0.0%') else item[4])
            item[5] = float(0 if item[5] == '' else item[5][:-1])
            item[6] = int(0 if item[6] == ('' or '0.0' or '-0.0' or '0.0%') else item[6])
            item[7] = int(0 if item[7] == ('' or '0.0' or '-0.0' or '0.0%') else item[7])
            item[8] = int(0 if item[8] == ('' or '0.0' or '-0.0' or '0.0%') else item[8])
            item[9] = int(0 if item[9] == ('' or '0.0' or '-0.0' or '0.0%') else item[9])
            item[10] = int(0 if item[10] == ('' or '0.0' or '-0.0' or '0.0%') else item[10])
            item[11] = int(0 if item[11] == ('' or '0.0' or '-0.0' or '0.0%') else item[11])
            item[12] = int(0 if item[12] == ('' or '0.0' or '-0.0' or '0.0%') else item[12])
            item[13] = float(0 if item[13] == '' else item[13])
            item[14] = int(0 if item[14] == ('' or '0.0' or '-0.0' or '0.0%') else item[14])
            item[15] = int(0 if item[15] == ('' or '0.0' or '-0.0' or '0.0%') else item[15])
            item[16] = int(0 if item[16] == ('' or '0.0' or '-0.0' or '0.0%') else item[16])
            item[17] = int(0 if item[17] == ('' or '0.0' or '-0.0' or '0.0%') else item[17])
            item[18] = int(0 if item[18] == ('' or '0.0' or '-0.0' or '0.0%') else item[18])
            item[19] = int(0 if item[19] == ('' or '0.0' or '-0.0' or '0.0%') else item[19])
            item[20] = int(0 if item[20] == ('' or '0.0' or '-0.0' or '0.0%') else item[20])
            item[21] = int(0 if item[21] == ('' or '0.0' or '-0.0' or '0.0%') else item[21])
            item[22] = int(0 if item[22] == ('' or '0.0' or '-0.0' or '0.0%') else item[22])
            item[23] = int(0 if item[23] == ('' or '0.0' or '-0.0' or '0.0%') else item[23])
            item[24] = float(0 if item[24] == '' else item[24][:-1])
            item[25] = int(0 if item[25] == ('' or '0.0' or '-0.0' or '0.0%') else item[25])
            item[26] = int(0 if item[26] == ('' or '0.0' or '-0.0' or '0.0%') else item[26])
            item[27] = float(0 if item[27] == '' or '0.0' or '-0.0' or '0.0%' else item[27])
            item[28] = int(0 if item[28] == ('' or '0.0' or '-0.0' or '0.0%') else item[28])
            item[29] = int(0 if item[29] == ('' or '0.0' or '-0.0' or '0.0%') else item[29])
            item[30] = float(0 if item[30] == '' else item[30][:-1])
            item[31] = int(0 if item[31] == ('' or '0.0' or '-0.0' or '0.0%') else item[31])
            item[32] = int(0 if item[32] == ('' or '0.0' or '-0.0' or '0.0%') else item[32])
            item[33] = float(0 if item[33] == '' else item[33][:-1])
            item[34] = int(0 if item[34] == ('' or '0.0' or '-0.0' or '0.0%') else item[34])
            item[35] = int(0 if item[35] == ('' or '0.0' or '-0.0' or '0.0%') else item[35])
            item[36] = float(0 if item[36] == '' else item[36][:-1])
            item[37] = int(0 if item[37] == ('' or '0.0' or '-0.0' or '0.0%') else item[37])
            item[38] = int(0 if item[38] == ('' or '0.0' or '-0.0' or '0.0%') else item[38])
            item[39] = float(0 if item[39] == '' else item[39][:-1])
            item[40] = int(0 if item[40] == ('' or '0.0' or '-0.0' or '0.0%') else item[40])
            clean_items.append([self.player_id, self.link] + item)
        return clean_items
    def clean_batting_pitches(self, rows):
        clean_items = []
        for item in rows:
            item[0] = int(item[0][:4])
            item[1] = int(0 if item[1] == '' or '0.0' or '-0.0' or '0.0%' else item[1])
            item[2] = str("'" + item[2] + "'")
            item[3] = str("'" + item[3] + "'")
            item[4] = int(0 if item[4] == ('' or '0.0' or '-0.0' or '0.0%') else item[4])
            item[5] = int(0 if item[5] == ('' or '0.0' or '-0.0' or '0.0%') else item[5])
            item[6] = float(0 if item[6] == '' else item[6][:-1])
            item[7] = int(0 if item[7] == ('' or '0.0' or '-0.0' or '0.0%') else item[7])
            item[8] = float(0 if item[8] == '' else item[8][:-1])
            item[9] = float(0 if item[9] == '' else item[9][:-1])
            item[10] = float(0 if item[10] == '' else item[10][:-1])
            item[11] = float(0 if item[11] == '' else item[11][:-1])
            item[12] = float(0 if item[12] == '' else item[12][:-1])
            item[13] = float(0 if item[13] == '' else item[13][:-1])
            item[14] = float(0 if item[14] == '' else item[14][:-1])
            item[15] = float(0 if item[15] == '' else item[15][:-1])
            item[16] = float(0 if item[16] == '' else item[16][:-1])
            item[17] = float(0 if item[17] == '' else item[17][:-1])
            item[18] = float(0 if item[18] == '' else item[18][:-1])
            item[19] = int(0 if item[19] == ('' or '0.0' or '-0.0' or '0.0%') else item[19])
            item[20] = int(0 if item[20] == ('' or '0.0' or '-0.0' or '0.0%') else item[20])
            item[21] = float(0 if item[21] == '' else item[21][:-1])
            item[22] = int(0 if item[22] == ('' or '0.0' or '-0.0' or '0.0%') else item[22])
            item[23] = int(0 if item[23] == ('' or '0.0' or '-0.0' or '0.0%') else item[23])
            item[24] = float(0 if item[24] == '' else item[24][:-1])
            item[25] = int(0 if item[25] == ('' or '0.0' or '-0.0' or '0.0%') else item[25])
            item[26] = int(0 if item[26] == ('' or '0.0' or '-0.0' or '0.0%') else item[26])
            item[27] = int(0 if item[27] == ('' or '0.0' or '-0.0' or '0.0%') else item[27])
            item[28] = int(0 if item[28] == ('' or '0.0' or '-0.0' or '0.0%') else item[28])
            item[29] = float(0 if item[29] == '' else item[29][:-1])
            item[30] = int(0 if item[30] == ('' or '0.0' or '-0.0' or '0.0%') else item[30])
            item[31] = int(0 if item[31] == ('' or '0.0' or '-0.0' or '0.0%') else item[31])
            item[32] = int(0 if item[32] == ('' or '0.0' or '-0.0' or '0.0%') else item[32])
            clean_items.append([self.player_id, self.link] + item)
        return clean_items
    def clean_cumulative_batting(self, rows):
        clean_items = []
        for item in rows:
            item[0] = int(item[0][:4])
            item[1] = int(0 if item[1] == ('' or '0.0' or '-0.0' or '0.0%') else item[1])
            item[2] = int(0 if item[2] == ('' or '0.0' or '-0.0' or '0.0%') else item[2])
            item[3] = int(0 if item[3] == ('' or '0.0' or '-0.0' or '0.0%') else item[3])
            item[4] = int(0 if item[4] == ('' or '0.0' or '-0.0' or '0.0%') else item[4])
            item[5] = int(0 if item[5] == ('' or '0.0' or '-0.0' or '0.0%') else item[5])
            item[6] = int(0 if item[6] == ('' or '0.0' or '-0.0' or '0.0%') else item[6])
            item[7] = int(0 if item[7] == ('' or '0.0' or '-0.0' or '0.0%') else item[7])
            item[8] = int(0 if item[8] == ('' or '0.0' or '-0.0' or '0.0%') else item[8])
            item[9] = int(0 if item[9] == ('' or '0.0' or '-0.0' or '0.0%') else item[9])
            item[10] = int(0 if item[10] == ('' or '0.0' or '-0.0' or '0.0%') else item[10])
            item[11] = int(0 if item[11] == ('' or '0.0' or '-0.0' or '0.0%') else item[11])
            item[12] = int(0 if item[12] == ('' or '0.0' or '-0.0' or '0.0%') else item[12])
            item[13] = int(0 if item[13] == ('' or '0.0' or '-0.0' or '0.0%') else item[13])
            item[14] = int(0 if item[14] == ('' or '0.0' or '-0.0' or '0.0%') else item[14])
            item[15] = float(0 if item[15] == '' else item[15][:-1])
            item[16] = float(0 if item[16] == '' else item[16][:-1])
            item[17] = float(0 if item[17] == '' else item[17][:-1])
            item[18] = float(0 if item[18] == '' else item[18][:-1])
            item[19] = int(0 if item[19] == ('' or '0.0' or '-0.0' or '0.0%') else item[19])
            item[20] = int(0 if item[20] == ('' or '0.0' or '-0.0' or '0.0%') else item[20])
            item[21] = int(0 if item[21] == ('' or '0.0' or '-0.0' or '0.0%') else item[21])
            item[22] = int(0 if item[22] == ('' or '0.0' or '-0.0' or '0.0%') else item[22])
            item[23] = int(0 if item[23] == ('' or '0.0' or '-0.0' or '0.0%') else item[23])
            item[24] = int(0 if item[24] == ('' or '0.0' or '-0.0' or '0.0%') else item[24])
            item[25] = int(0 if item[25] == ('' or '0.0' or '-0.0' or '0.0%') else item[25])
            clean_items.append([self.player_id, self.link] + item)
        return clean_items

    def query_constructor(self, table_name, row):
        query = "INSERT INTO {} VALUES ".format(table_name)
        query += "("
        query += "{},"*len(row)
        query = query[:-1]
        query += ");"
        return query.format(*tuple(row))

    def write_to_db(self, table_data):
        table_key = list(table_data.keys())[0]
        table_values = table_data[list(table_data.keys())[0]]
        conn, cur = quer.start_server()
        for row in table_values:
            query = self.query_constructor(table_key,row)
            cur.execute(query)
        quer.close_server(conn)
        print('Records Inserted Into ' + table_key)
        return None

