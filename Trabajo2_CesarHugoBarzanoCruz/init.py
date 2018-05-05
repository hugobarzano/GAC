import sqlite3
import mysql.connector
import psycopg2




#sqlite3 initial
sqlite3_conn = sqlite3.connect('./testGAC.db')
sqlite3_cursor = sqlite3_conn.cursor()
sqlite3_cursor.execute('''CREATE TABLE gac_models (atr_1 text, atr_2 text)''')
sqlite3_cursor.execute("INSERT INTO gac_models VALUES ('atribute_1','atribute_2')")
sqlite3_cursor.execute("INSERT INTO gac_models VALUES ('atribute_3','atribute_4')")
sqlite3_conn.commit()
sqlite3_conn.close()


#mysql initial

config_mysql = {
  'user': 'root',
  'password': '',
  'host': '127.0.0.1',
  'database': '',
}

mysql_gac_model = (
    "CREATE TABLE `gac_models` ("
    "  `model_no` int(11) NOT NULL AUTO_INCREMENT,"
    "  `atr_1` varchar(14) NOT NULL,"
    "  `atr_2` varchar(14) NOT NULL,"
    "  PRIMARY KEY (`model_no`)"
    ") ENGINE=InnoDB")


mysql_conn = mysql.connector.connect(**config_mysql)
mysql_cursor = mysql_conn.cursor()
mysql_cursor.execute("CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format('testGAC'))
mysql_conn.database = 'testGAC'
mysql_cursor.execute(mysql_gac_model)



add_mysql_model = ("INSERT INTO gac_models (atr_1, atr_2) VALUES (%s, %s)")
data_mysql_model = ('atribute_1', 'atribute_2')
mysql_cursor.execute(add_mysql_model, data_mysql_model)
mysql_cursor.execute(add_mysql_model, data_mysql_model)
mysql_conn.commit()
mysql_cursor.close()
mysql_conn.close()



#Postgres initial
config_postgres="host='localhost' dbname='testgac' user='postgres' password='123456'"
postgres_conn = psycopg2.connect(config_postgres)
postgres_cursor = postgres_conn.cursor()

postgres_gac_model = (
        """
        CREATE TABLE gac_models (
            model_no SERIAL PRIMARY KEY,
            atr_1 VARCHAR(14) NOT NULL,
            atr_2 VARCHAR(14) NOT NULL
        )
        """)
postgres_cursor.execute(postgres_gac_model)

add_postgres_model=("INSERT INTO gac_models (atr_1,atr_2) VALUES(%s,%s)")
data_postgres_model=('atribute_1','atribute_2')

postgres_cursor.execute(add_postgres_model,data_postgres_model)
postgres_conn.commit()
postgres_conn.close()
