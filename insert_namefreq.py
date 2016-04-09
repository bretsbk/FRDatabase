import requests
import pyodbc
import time
from create_db_table import create_namefreq_db, create_namefreq_tables

# http://stackoverflow.com/questions/1803628/raw-list-of-person-names
# Col0: Name | Col1: Relative Frequency (%) | Col2: Cumulative Frequency (%) | Col3: Rank
name_first_male = 'http://www2.census.gov/topics/genealogy/1990surnames/dist.male.first'
name_first_female = 'http://www2.census.gov/topics/genealogy/1990surnames/dist.female.first'
name_last_all = 'http://www2.census.gov/topics/genealogy/1990surnames/dist.all.last'

def namefreq_insert(name_url):
    name_req = requests.get(name_url)
    name_str = name_req.content.decode('utf-8').split('\n') #decodes requests from byte to string, splits string on '\n'

    name_list = []
    name_all = []
    name_dict = {}
    name_int = 0

    if name_url == name_first_male:
        table_name = 'dbo.NameFirstMale'
    elif name_url == name_first_female:
        table_name = 'dbo.NameFirstFemale'
    elif name_url == name_last_all:
        table_name = 'dbo.NameLast'

    for name in name_str[:-1]:
        name_list.append(name.split(None,3))
    #print(name_list)

    for list in name_list:
        name_all.append(list[0])
    #print(name_all)

    for fname in name_all:
        name_dict[fname] = name_list[name_int]
        name_int += 1
    #print(name_dict)

    dbcon_str_setup = 'DRIVER={SQL Server};SERVER=HAL-9000\SQLEXPRESS;DATABASE=NameFreq'
    db_con_db = pyodbc.connect(dbcon_str_setup)
    concurs = db_con_db.cursor()
    for namekey in name_all:
        sql_insert = """
            INSERT INTO """ + table_name + """ (name, rel_freq, cum_freq, rank)
            VALUES ('""" + name_dict[namekey][0] + """',""" + name_dict[namekey][1] + """,""" + name_dict[namekey][2] + """,""" + name_dict[namekey][3] + """);
            """
        concurs.execute(sql_insert)
        concurs.commit()
    concurs.close()

create_namefreq_db()
time.sleep(5)
create_namefreq_db()
time.sleep(5)
create_namefreq_tables()
time.sleep(10)
create_namefreq_tables()
time.sleep(10)
namefreq_insert(name_first_male)
time.sleep(5)
namefreq_insert(name_first_female)
time.sleep(5)
namefreq_insert(name_last_all)