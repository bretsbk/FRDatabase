import pyodbc

def create_namefreq_db():
    dbcon_str_setup = 'DRIVER={SQL Server};SERVER=HAL-9000\SQLEXPRESS'
    query_impltrans_off = 'SET IMPLICIT_TRANSACTIONS OFF;'
    query_createdb_create = 'CREATE DATABASE NameFreq;'
    db_con_db = pyodbc.connect(dbcon_str_setup)
    concurs = db_con_db.cursor()
    concurs.execute(query_impltrans_off)
    concurs.execute(query_createdb_create)
    concurs.close()

def create_namefreq_tables():
    dbcon_str_name = 'Driver={SQL Server};Server=HAL-9000\SQLEXPRESS;DATABASE=NameFreq'
    query_impltrans_off = 'SET IMPLICIT_TRANSACTIONS OFF'
    query_createtables = """
        CREATE TABLE NameFirstMale (
            id INT IDENTITY(00001,1) PRIMARY KEY,
            name NVARCHAR (15) NOT NULL,
            rel_freq DECIMAL(9,5) NOT NULL,
            cum_freq DECIMAL(9,5) NOT NULL,
            rank INT NOT NULL
            );

        CREATE TABLE NameFirstFemale (
            id INT IDENTITY(00001,1) PRIMARY KEY,
            name NVARCHAR (15) NOT NULL,
            rel_freq DECIMAL(9,5) NOT NULL,
            cum_freq DECIMAL(9,5) NOT NULL,
            rank INT NOT NULL
            );

        CREATE TABLE NameLast (
            id INT IDENTITY(00001,1) PRIMARY KEY,
            name NVARCHAR (15) NOT NULL,
            rel_freq DECIMAL(9,5) NOT NULL,
            cum_freq DECIMAL(9,5) NOT NULL,
            rank INT NOT NULL
            );
        """
    db_con_table = pyodbc.connect(dbcon_str_name)
    concurs = db_con_table.cursor()
    concurs.execute(query_impltrans_off)
    concurs.execute(query_createtables)
    concurs.close()