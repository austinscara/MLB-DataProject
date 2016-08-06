import ipdb

insert_queries = {'player_id': 'INSERT IGNORE INTO player VALUES (id, %s,%s,%s,%s);'
                 ,'team_id': """UPDATE temp
                                LEFT JOIN team on  temp.team_code = team.team_code
                                SET temp.is_update = CASE WHEN (temp.team_link = team.team_link 
                                                           AND temp.team_code = team.team_code 
                                                           AND temp.team_name = team.team_name 
                                                           AND temp.team_league = team.team_league) THEN 0 ELSE  1
                                                           END;

                            INSERT INTO team (team_link, team_code, team_name, team_league) 
                            SELECT  temp.team_link, temp.team_code, temp.team_name, temp.team_league
                            FROM temp
                            ON DUPLICATE KEY UPDATE team.team_league = CASE WHEN team.team_league = temp.team_league THEN  team.team_league ELSE temp.team_league END
                            ; """

                  }


def start_server():
    import pymysql
    connection = pymysql.connect(user='root', password='AJScara13;', host='127.0.0.1', port = 3306,  database='mlb_project1', autocommit=True)
    mssql_cursor = connection.cursor()
    print('connected')
    return connection, mssql_cursor

def execute_query(query, connection=None, mssql_cursor=None,  records=None, is_insert=False, results=False, keep_open=False):
    if not connection:
        connection, mssql_cursor = start_server()
    if is_insert and keep_open and not results:
        for record in records:
            mssql_cursor.execute(query, (*record,))
        print('Records Inserted')
        return connection, mssql_cursor
    elif is_insert and not keep_open and not results:
        for record in records:
            mssql_cursor.execute(query, (*record,))
        close_server(connection)
        print('Records Inserted')
        return None
    elif not is_insert and keep_open and not results:
        mssql_cursor.execute(query)
        print('Query Executed')
        return connection, mssql_cursor
    elif not is_insert and not keep_open and not results:
        mssql_cursor.execute(query)
        close_server(connection)
        print('Query Executed')
        return None
    elif results:
        connection, mssql_cursor = start_server()
        mssql_cursor.execute(query)
        results = mssql_cursor.fetchall()
        close_server(connection)
        return results
    else:
        print('Warning Your Parameters May Not Be Sable')
        return None

def close_server(connection):
    connection.close()
    return print('Commit Successful')

def temp_table_creator(records, headers):
    #records = list
    temp_table = 'CREATE TEMPORARY TABLE {} ('.format("temp")
    temp_table += ', '.join('{} '.format(str(header)) for header in headers)
    temp_table += ', ' + 'is_update INT'
    temp_table += ');'

    connection, mssql_cursor = execute_query(temp_table, keep_open=True)

    insert_string = "INSERT INTO {} VALUES ".format('temp')
    insert_string += "("
    insert_string += "%s,"*len(headers)
    insert_string += "NULL" #as check column
    insert_string += ");"

    connection, mssql_cursor = execute_query(insert_string, connection, mssql_cursor, records=records, is_insert=True, keep_open=True)
    return connection, mssql_cursor


def build_insert(table, record):
    insert_string = "INSERT INTO {} VALUES ".format('temp')
    insert_string += "("
    insert_string += "%s," * len(headers)
    insert_string += "NULL"  # as check column
    insert_string += ");"

    return None