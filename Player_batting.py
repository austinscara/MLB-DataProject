from bs4 import BeautifulSoup
import mlb_db_queries as quer
import pprint as pp
class Player_batting(object):
    instances = []

    def __init__(self, player_id, player_alias, html, link):
        self.player_id = player_id
        self.player_alias = player_alias
        self.link  = "'" + link + "'"
        self.html = BeautifulSoup(html,'html5lib').body.find('div', id='all_batting').find_all('tr', {'class': 'full'})
        Player_batting.instances.append(self)
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

    # Creates all Tables
    def parse_tables(self):
        self.batting_standard = {'batting_standard': self.clean_batting_standard(self.capture_player_batting_standard())}
        self.batting_value = {'batting_value': self.clean_batting_value(self.capture_player_batting_value())}
        self.batting_advanced = {'batting_advanced':  self.clean_batting_advanced(self.capture_player_batting_advanced())}
        self.batting_postseason = {'batting_postseason':  self.clean_batting_postseason(self.capture_player_batting_post_season())}
        self.batting_ratio = {'batting_ratio': self.clean_batting_ratio(self.capture_player_batting_ratio())}
        self.batting_win_probability = {'batting_win_probability': self.clean_batting_win_probability(self.capture_player_batting_win_prob())}
        self.batting_baserunning = {'batting_baserunning': self.clean_batting_baserunning(self.capture_player_batting_baserunning())}
        self.batting_situational = {'batting_situational': self.clean_batting_situational(self.capture_player_batting_situational())}
        self.batting_pitches = {'batting_pitches': self.clean_batting_pitches(self.capture_player_batting_pitches())}
        self.cumulative_batting = {'cumulative_batting': self.clean_cumulative_batting(self.capture_player_batting_cumulative())}
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
         batting_data = [[data.text.strip() for data in item.find_all('td')] for item in self.html if item.get('id').startswith('cumulative_batting')]
         return batting_data

    # Cleans tables that were captured used DDL to format
    def clean_batting_standard(self, rows):
        clean_items = []
        for item in rows:
            item[0] = int(item[0][:4])
            item[1] = int(0 if item[1] == '' else 0)
            item[2] = str("'" + item[2] + "'")
            item[3] = str("'" + item[3] + "'")
            item[4] = int(0 if item[4] == '' else 0)
            item[5] = int(0 if item[5] == '' else 0)
            item[6] = int(0 if item[6] == '' else 0)
            item[7] = int(0 if item[7] == '' else 0)
            item[8] = int(0 if item[8] == '' else 0)
            item[9] = int(0 if item[9] == '' else 0)
            item[10] = int(0 if item[10] == '' else 0)
            item[11] = int(0 if item[11] == '' else 0)
            item[12] = int(0 if item[12] == '' else 0)
            item[13] = int(0 if item[13] == '' else 0)
            item[14] = int(0 if item[14] == '' else 0)
            item[15] = int(0 if item[15] == '' else 0)
            item[16] = int(0 if item[16] == '' else 0)
            item[17] = float(0 if item[17] == '' else 0)
            item[18] = float(0 if item[18] == '' else 0)
            item[19] = float(0 if item[19] == '' else 0)
            item[20] = float(0 if item[20] == '' else 0)
            item[21] = int(0 if item[21] == '' else 0)
            item[22] = int(0 if item[22] == '' else 0)
            item[23] = int(0 if item[23] == '' else 0)
            item[24] = int(0 if item[24] == '' else 0)
            item[25] = int(0 if item[25] == '' else 0)
            item[26] = int(0 if item[26] == '' else 0)
            item[27] = int(0 if item[27] == '' else 0)
            item[28] = str("'"+ item[28] + "'")
            item[29] = str("'" + item[29] + "'")
            clean_items.append([self.player_id, self.link] + item)
        return clean_items
    def clean_batting_value(self, rows):
        clean_items = []
        for item in rows:
            item[0] = int(item[0][:4])
            item[1] = int(0 if item[1] == '' else 0)
            item[2] = int(0 if item[2] == '' else 0)
            item[3] = int(0 if item[3] == '' else 0)
            item[4] = int(0 if item[4] == '' else 0)
            item[5] = int(0 if item[5] == '' else 0)
            item[6] = int(0 if item[6] == '' else 0)
            item[7] = int(0 if item[7] == '' else 0)
            item[8] = int(0 if item[8] == '' else 0)
            item[9] = int(0 if item[9] == '' else 0)
            item[10] = int(0 if item[10] == '' else 0)
            item[11] = int(0 if item[11] == '' else 0)
            item[12] = int(0 if item[12] == '' else 0)
            item[13] = int(0 if item[13] == '' else 0)
            item[14] = int(0 if item[14] == '' else 0)
            item[15] = float(0 if item[15] == '' else 0)
            item[16] = float(0 if item[16] == '' else 0)
            item[17] = float(0 if item[17] == '' else 0)
            item[18] = float(0 if item[18] == '' else 0)
            item[19] = float(0 if item[19] == '' else 0)
            item[20] = int(0 if item[20] == '' else 0)
            item[21] = str("'" + item[21] + "'")
            item[22] = str("'" + item[22] + "'")
            item[23] = str("'" + item[23] + "'")
            clean_items.append([self.player_id, self.link] + item)
        return clean_items
    def clean_batting_advanced(self, rows):
        clean_items = []
        for item in rows:
            item[0] = int(item[0][:4])
            item[1] = int(0 if item[1] == '' else 0)
            item[2] = int(0 if item[2] == '' else 0)
            item[3] = int(0 if item[3] == '' else 0)
            item[4] = int(0 if item[4] == '' else 0)
            item[5] = int(0 if item[5] == '' else 0)
            item[6] = int(0 if item[6] == '' else 0)
            item[7] = float(0 if item[7] == '' else 0)
            item[8] = float(0 if item[8] == '' else 0)
            item[9] = float(0 if item[9] == '' else 0)
            item[10] = float(0 if item[10] == '' else 0)
            item[11] = float(0 if item[11] == '' else 0)
            item[12] = float(0 if item[12] == '' else 0)
            item[13] = float(0 if item[13] == '' else 0)
            item[14] = float(0 if item[14] == '' else 0)
            item[15] = float(0 if item[15] == '' else 0)
            item[16] = float(0 if item[16] == '' else 0)
            item[17] = float(0 if item[17] == '' else 0)
            item[18] = float(0 if item[18] == '' else 0)
            item[19] = float(0 if item[19] == '' else 0)
            item[20] = float(0 if item[20] == '' else 0)
            item[21] = float(0 if item[21] == '' else 0)
            item[22] = float(0 if item[22] == '' else 0)
            item[23] = float(0 if item[23] == '' else 0)
            item[24] = float(0 if item[24] == '' else 0)
            item[25] = float(0 if item[25] == '' else 0)
            clean_items.append([self.player_id, self.link] + item)
        return clean_items
    def clean_batting_postseason(self, rows):
        clean_items = []
        for item in rows:
            item[0] = int(item[0][:4])
            item[1] = int(0 if item[1] == '' else 0)
            item[2] = int(0 if item[2] == '' else 0)
            item[3] = int(0 if item[3] == '' else 0)
            item[4] = str("'" + item[4] + "'")
            item[5] = str("'" + item[5] + "'")
            item[6] = str("'" + item[6] + "'")
            item[7] = int(0 if item[7] == '' else 0)
            item[8] = int(0 if item[8] == '' else 0)
            item[9] = int(0 if item[9] == '' else 0)
            item[10] = int(0 if item[10] == '' else 0)
            item[11] = int(0 if item[11] == '' else 0)
            item[12] = int(0 if item[12] == '' else 0)
            item[13] = int(0 if item[13] == '' else 0)
            item[14] = int(0 if item[14] == '' else 0)
            item[15] = int(0 if item[15] == '' else 0)
            item[16] = int(0 if item[16] == '' else 0)
            item[17] = int(0 if item[17] == '' else 0)
            item[18] = int(0 if item[18] == '' else 0)
            item[19] = int(0 if item[19] == '' else 0)
            item[20] = float(0 if item[20] == '' else 0)
            item[21] = float(0 if item[21] == '' else 0)
            item[22] = float(0 if item[22] == '' else 0)
            item[23] = float(0 if item[23] == '' else 0)
            item[24] = int(0 if item[24] == '' else 0)
            item[25] = int(0 if item[25] == '' else 0)
            item[26] = int(0 if item[26] == '' else 0)
            item[27] = int(0 if item[27] == '' else 0)
            item[28] = int(0 if item[28] == '' else 0)
            item[29] = int(0 if item[29] == '' else 0)
            clean_items.append([self.player_id, self.link] + item)
        return clean_items
    def clean_batting_ratio(self, rows):
        clean_items = []
        for item in rows:
            item[0] = int(item[0][:4])
            item[1] = int(0 if item[1] == '' else 0)
            item[2] = str("'" + item[2] + "'")
            item[3] = str("'" + item[3] + "'")
            item[4] = float(0 if item[4] == '' else 0)
            item[5] = float(0 if item[5] == '' else 0)
            item[6] = float(0 if item[6] == '' else 0)
            item[7] = float(0 if item[7] == '' else 0)
            item[8] = float(0 if item[8] == '' else 0)
            item[9] = float(0 if item[9] == '' else 0)
            item[10] = float(0 if item[10] == '' else 0)
            item[11] = float(0 if item[11] == '' else 0)
            item[12] = float(0 if item[12] == '' else 0)
            item[13] = float(0 if item[13] == '' else 0)
            item[14] = float(0 if item[14] == '' else 0)
            item[15] = float(0 if item[15] == '' else 0)
            item[16] = float(0 if item[16] == '' else 0)
            item[17] = float(0 if item[17] == '' else 0)
            item[18] = float(0 if item[18] == '' else 0)
            item[19] = float(0 if item[19] == '' else 0)
            clean_items.append([self.player_id, self.link] + item)
        return clean_items
    def clean_batting_win_probability(self, rows):
        clean_items = []
        for item in rows:
            item[0] = int(item[0][:4])
            item[1] = int(0 if item[1] == '' else 0)
            item[2] = str("'" + item[2] + "'")
            item[3] = str("'" + item[3] + "'")
            item[4] = float(0 if item[4] == '' else 0)
            item[5] = float(0 if item[5] == '' else 0)
            item[6] = int(0 if item[6] == '' else 0)
            item[7] = float(0 if item[7] == '' else 0)
            item[8] = float(0 if item[8] == '' else 0)
            item[9] = float(0 if item[9] == '' else 0)
            item[10] = float(0 if item[10] == '' else 0)
            item[11] = float(0 if item[11] == '' else 0)
            item[12] = float(0 if item[12] == '' else 0)
            item[13] = float(0 if item[13] == '' else 0)
            item[14] = float(0 if item[14] == '' else 0)
            item[15] = float(0 if item[15] == '' else 0)
            item[16] = float(0 if item[16] == '' else 0)
            item[17] = float(0 if item[17] == '' else 0)
            item[18] = int(0 if item[18] == '' else 0)
            clean_items.append([self.player_id, self.link] + item)
        return clean_items
    def clean_batting_baserunning(self, rows):
        clean_items = []
        for item in rows:
            item[0] = int(item[0][:4])
            item[1] = int(0 if item[1] == '' else 0)
            item[2] = str("'" + item[2] + "'")
            item[3] = str("'" + item[3] + "'")
            item[4] = int(0 if item[4] == '' else 0)
            item[5] = int(0 if item[5] == '' else 0)
            item[6] = float(0 if item[6] == '' else 0)
            item[7] = int(0 if item[7] == '' else 0)
            item[8] = int(0 if item[8] == '' else 0)
            item[9] = int(0 if item[9] == '' else 0)
            item[10] = float(0 if item[10] == '' else 0)
            item[11] = int(0 if item[11] == '' else 0)
            item[12] = int(0 if item[12] == '' else 0)
            item[13] = int(0 if item[13] == '' else 0)
            item[14] = int(0 if item[14] == '' else 0)
            item[15] = int(0 if item[15] == '' else 0)
            item[16] = int(0 if item[16] == '' else 0)
            item[17] = int(0 if item[17] == '' else 0)
            item[18] = int(0 if item[18] == '' else 0)
            item[19] = int(0 if item[19] == '' else 0)
            item[20] = int(0 if item[20] == '' else 0)
            item[21] = int(0 if item[21] == '' else 0)
            item[22] = int(0 if item[22] == '' else 0)
            item[23] = int(0 if item[23] == '' else 0)
            item[24] = int(0 if item[24] == '' else 0)
            item[25] = float(0 if item[25] == '' else 0)
            item[26] = int(0 if item[26] == '' else 0)
            item[27] = int(0 if item[27] == '' else 0)
            item[28] = int(0 if item[28] == '' else 0)
            item[29] = int(0 if item[29] == '' else 0)
            item[30] = int(0 if item[30] == '' else 0)
            item[31] = int(0 if item[31] == '' else 0)
            item[32] = int(0 if item[32] == '' else 0)
            item[33] = int(0 if item[33] == '' else 0)
            item[34] = int(0 if item[34] == '' else 0)
            clean_items.append([self.player_id, self.link] + item)
        return clean_items
    def clean_batting_situational(self, rows):
        clean_items = []
        for item in rows:
            item[0] = int(item[0][:4])
            item[1] = int(0 if item[1] == '' else 0)
            item[2] = str("'" + item[2] + "'")
            item[3] = str("'" + item[3] + "'")
            item[4] = int(0 if item[4] == '' else 0)
            item[5] = float(0 if item[5] == '' else 0)
            item[6] = int(0 if item[6] == '' else 0)
            item[7] = int(0 if item[7] == '' else 0)
            item[8] = int(0 if item[8] == '' else 0)
            item[9] = int(0 if item[9] == '' else 0)
            item[10] = int(0 if item[10] == '' else 0)
            item[11] = int(0 if item[11] == '' else 0)
            item[12] = int(0 if item[12] == '' else 0)
            item[13] = float(0 if item[13] == '' else 0)
            item[14] = int(0 if item[14] == '' else 0)
            item[15] = int(0 if item[15] == '' else 0)
            item[16] = int(0 if item[16] == '' else 0)
            item[17] = int(0 if item[17] == '' else 0)
            item[18] = int(0 if item[18] == '' else 0)
            item[19] = int(0 if item[19] == '' else 0)
            item[20] = int(0 if item[20] == '' else 0)
            item[21] = int(0 if item[21] == '' else 0)
            item[22] = int(0 if item[22] == '' else 0)
            item[23] = int(0 if item[23] == '' else 0)
            item[24] = float(0 if item[24] == '' else 0)
            item[25] = int(0 if item[25] == '' else 0)
            item[26] = int(0 if item[26] == '' else 0)
            item[27] = float(0 if item[27] == '' else 0)
            item[28] = int(0 if item[28] == '' else 0)
            item[29] = int(0 if item[29] == '' else 0)
            item[30] = float(0 if item[30] == '' else 0)
            item[31] = int(0 if item[31] == '' else 0)
            item[32] = int(0 if item[32] == '' else 0)
            item[33] = float(0 if item[33] == '' else 0)
            item[34] = int(0 if item[34] == '' else 0)
            item[35] = int(0 if item[35] == '' else 0)
            item[36] = float(0 if item[36] == '' else 0)
            item[37] = int(0 if item[37] == '' else 0)
            item[38] = int(0 if item[38] == '' else 0)
            item[39] = float(0 if item[39] == '' else 0)
            item[40] = int(0 if item[40] == '' else 0)
            clean_items.append([self.player_id, self.link] + item)
        return clean_items
    def clean_batting_pitches(self, rows):
        clean_items = []
        for item in rows:
            item[0] = int(item[0][:4])
            item[1] = int(0 if item[1] == '' else 0)
            item[2] = str("'" + item[2] + "'")
            item[3] = str("'" + item[3] + "'")
            item[4] = int(0 if item[4] == '' else 0)
            item[5] = int(0 if item[5] == '' else 0)
            item[6] = float(0 if item[6] == '' else 0)
            item[7] = int(0 if item[7] == '' else 0)
            item[8] = float(0 if item[8] == '' else 0)
            item[9] = float(0 if item[9] == '' else 0)
            item[10] = float(0 if item[10] == '' else 0)
            item[11] = float(0 if item[11] == '' else 0)
            item[12] = float(0 if item[12] == '' else 0)
            item[13] = float(0 if item[13] == '' else 0)
            item[14] = float(0 if item[14] == '' else 0)
            item[15] = float(0 if item[15] == '' else 0)
            item[16] = float(0 if item[16] == '' else 0)
            item[17] = float(0 if item[17] == '' else 0)
            item[18] = float(0 if item[18] == '' else 0)
            item[19] = int(0 if item[19] == '' else 0)
            item[20] = int(0 if item[20] == '' else 0)
            item[21] = float(0 if item[21] == '' else 0)
            item[22] = int(0 if item[22] == '' else 0)
            item[23] = int(0 if item[23] == '' else 0)
            item[24] = float(0 if item[24] == '' else 0)
            item[25] = int(0 if item[25] == '' else 0)
            item[26] = int(0 if item[26] == '' else 0)
            item[27] = int(0 if item[27] == '' else 0)
            item[28] = int(0 if item[28] == '' else 0)
            item[29] = float(0 if item[29] == '' else 0)
            item[30] = int(0 if item[30] == '' else 0)
            item[31] = int(0 if item[31] == '' else 0)
            item[32] = int(0 if item[32] == '' else 0)
            clean_items.append([self.player_id, self.link] + item)
        return clean_items
    def clean_cumulative_batting(self, rows):
        clean_items = []
        for item in rows:
            item[0] = int(item[0][:4])
            item[1] = int(0 if item[1] == '' else 0)
            item[2] = int(0 if item[2] == '' else 0)
            item[3] = int(0 if item[3] == '' else 0)
            item[4] = int(0 if item[4] == '' else 0)
            item[5] = int(0 if item[5] == '' else 0)
            item[6] = int(0 if item[6] == '' else 0)
            item[7] = int(0 if item[7] == '' else 0)
            item[8] = int(0 if item[8] == '' else 0)
            item[9] = int(0 if item[9] == '' else 0)
            item[10] = int(0 if item[10] == '' else 0)
            item[11] = int(0 if item[11] == '' else 0)
            item[12] = int(0 if item[12] == '' else 0)
            item[13] = int(0 if item[13] == '' else 0)
            item[14] = int(0 if item[14] == '' else 0)
            item[15] = float(0 if item[15] == '' else 0)
            item[16] = float(0 if item[16] == '' else 0)
            item[17] = float(0 if item[17] == '' else 0)
            item[18] = float(0 if item[18] == '' else 0)
            item[19] = int(0 if item[19] == '' else 0)
            item[20] = int(0 if item[20] == '' else 0)
            item[21] = int(0 if item[21] == '' else 0)
            item[22] = int(0 if item[22] == '' else 0)
            item[23] = int(0 if item[23] == '' else 0)
            item[24] = int(0 if item[24] == '' else 0)
            item[25] = int(0 if item[25] == '' else 0)
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
        print(table_data)
        table_key = list(table_data.keys())[0]
        table_values = table_data[list(table_data.keys())[0]]
        conn, cur = quer.start_server()
        for row in table_values:
            query = self.query_constructor(table_key,row)
            cur.execute(query)
        quer.close_server(conn)
        print('Records Inserted Into ' + table_key)
        return None

