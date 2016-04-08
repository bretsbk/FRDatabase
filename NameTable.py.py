import requests
import pyodbc

# http://stackoverflow.com/questions/1803628/raw-list-of-person-names
# Col0: Name | Col1: Relative Frequency (%) | Col2: Cumulative Frequency (%) | Col3: Rank
name_first_male = 'http://www2.census.gov/topics/genealogy/1990surnames/dist.male.first'
name_first_female = 'http://www2.census.gov/topics/genealogy/1990surnames/dist.female.first'
name_last_all = 'http://www2.census.gov/topics/genealogy/1990surnames/dist.all.last'

def create_namefreq_db():
    dbcon_str_setup = 'DRIVER={SQL Server};SERVER=SFS03599'
    query_impltrans_off = 'SET IMPLICIT_TRANSACTIONS OFF;'
    query_createdb_create = 'CREATE DATABASE NameFreq;'
    db_con_db = pyodbc.connect(dbcon_str_setup)
    concurs = db_con_db.cursor()
    concurs.execute(query_impltrans_off)
    concurs.execute(query_createdb_create)
    concurs.close()

def create_namefreq_tables():
    dbcon_str_name = 'Driver={SQL Server};Server=SFS03599;DATABASE=NameFreq'
    query_impltrans_off = 'SET IMPLICIT_TRANSACTIONS OFF'
    query_createtables = """
        CREATE TABLE NameFirstMale (
            id INT IDENTITY(00001,1) PRIMARY KEY,
            name NVARCHAR,
            rel_freq DECIMAL(4,3) NOT NULL,
            cum_freq DECIMAL(5,3) NOT NULL,
            rank INT NOT NULL
            );

        CREATE TABLE NameFirstFemale (
            id INT IDENTITY(00001,1) PRIMARY KEY,
            name NVARCHAR,
            rel_freq DECIMAL(4,3) NOT NULL,
            cum_freq DECIMAL(5,3) NOT NULL,
            rank INT NOT NULL
            );

        CREATE TABLE NameLast (
            id INT IDENTITY(00001,1) PRIMARY KEY,
            name NVARCHAR,
            rel_freq DECIMAL(4,3) NOT NULL,
            cum_freq DECIMAL(5,3) NOT NULL,
            rank INT NOT NULL
            );
        """
    db_con_table = pyodbc.connect(dbcon_str_name)
    concurs = db_con_table.cursor()
    concurs.execute(query_impltrans_off)
    concurs.execute(query_createtables)
    concurs.close()

def name_freq_dict(name_url):
    name_req = requests.get(name_url)
    name_str = name_req.content.decode('utf-8').split('\n') #decodes requests from byte to string, splits string on '\n'

    name_list = []
    for name in name_str[:-1]:
        name_list.append(name.split(None,3))

    name_all = []
    for list in name_list:
        name_all.append(list[0])

    name_dict = {}
    name_int = 0
    for fname in name_all:
        name_dict[fname] = name_list[name_int]
        name_int += 1
    print(name_dict)
    print(name_list)
    
    sql_insert = 'INSERT INTO '
    for name in name_list:
        print(name[0])