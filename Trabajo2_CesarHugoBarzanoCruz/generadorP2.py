#!/usr/bin/python


__author__ = 'Hugo Barzano'
__date__ = '2017/2018'
__version__ = 'v1.0'
__credits__ = 'GAC'
__file__ = 'generatorP2.py'


import sys
import os
import getopt
import time
import mysql.connector
import json
import psycopg2
import sqlite3
import lxml.etree as et
import csv
import io



#INPUT and OUTPUT DATA FOLDER
OUTPUT_FOLDER="./output/"
INPUT_FOLDER="./input/"

"""Generator configuration file: Databases interfaces definition"""
GENERATOR_CONFIG=INPUT_FOLDER+"GENERATOR_CONFIG.json"
def data2xml(data, name='data'):
    root = et.Element(name)
    return et.tostring(buildxml(root, data))

def buildxml(root, data):
    if isinstance(data, dict):
        for key, value in data.iteritems():
            sub = et.SubElement(root, key)
            buildxml(sub, value)
    elif isinstance(data, tuple) or isinstance(data, list):
        for value in data:
            sub = et.SubElement(root, 'i')
            buildxml(sub, value)
    elif isinstance(data, basestring):
        root.text = data
    else:
        root.text = str(data)
    return root


def buildCsv(data,sgbd):
    with open(OUTPUT_FOLDER+"GAC_"+sgbd+"_"+time.strftime("%Y%m%d_%H%M%S")+".csv", "w") as output:
        writer = csv.writer(output, lineterminator='\n')
        writer.writerows(data)
    print "Writing output file in"+OUTPUT_FOLDER+"GAC_"+sgbd+"_"+time.strftime("%Y%m%d_%H%M%S")+".csv"


def buildHtml(data,sgbd):
    html_table_1="""<table style="width:100%">"""
    html_table_2=""
    for tupla in data:
        html_table_2="<tr>"
        for t in tupla:
            html_table_2=html_table_2+"<td>"+str(t)+"</td>"
        html_table_2=html_table_2+"</tr>"
    html_table=html_table_1+html_table_2+"</table>"
    html_doc="""<!DOCTYPE html>
    <html>
    <head>
    <title>"""+sgbd+"""</title>
    </head>
    <body>
    <h1>"""+sgbd+"""</h1><hr><br>"""+html_table+"""</body></html> """
    return html_doc


def writeOutput(output_file,output_string):
    """Function to write output files.
         :param output_file: output file path
         :param output_string: string to write in the output file"""
    print "Writing output file in "+output_file
    try:
        with open(output_file, 'w') as f:
    	       f.write(output_string)
    except EnvironmentError:
        print("Oops! Error writing output file...")
        exit()

def configurePostgres(config_json):
    config_str="host='"+config_json["host"]+"' dbname='"+config_json["database"]+"' user='"+config_json["user"]+"' password='"+config_json["password"]+"'"
    return config_str



def main(argv):
    """Main method to execute the generator.
                :param argv: value from 0 to n-1 to ident"""
    table=None
    where=None
    debug=False

    # process arguments
    try:
        opts, args = getopt.getopt(argv, "hvt:w:d", ["help", "version", "table=","where=","debug"])
    except getopt.GetoptError as err:
        print str(err)
        usage()
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
            sys.exit()
        elif opt in ("-v", "--version"):
            version()
            sys.exit()
        elif opt in ("-t", "--table"):
            table = arg
        elif opt in ("-w","--where"):
            where=arg
        elif opt in ("-d", "--debug"):
            debug = True
            print "Debug: TRUE"
        else:
            usage()
            sys.exit()

    print "GAC: P2"
    with open(GENERATOR_CONFIG) as config_file:
        SGBD_config = json.load(config_file)

    if where==None:
        query = ("SELECT * FROM "+table)
    else:
        query = ("SELECT * FROM "+table+ " WHERE "+where)
    connector=None
    cursor=None
    data=None
    for SGBD in SGBD_config:
        if "mysql" in SGBD:
            print "Mysql: "+ SGBD
            try:
                connector = mysql.connector.connect(**SGBD_config[SGBD])
            except mysql.connector.Error as err:
                print(err)
                continue
        elif "postgres" in SGBD:
            print "Postgres"+ SGBD
            try:
                connector = psycopg2.connect(configurePostgres(SGBD_config[SGBD]))
            except psycopg2.OperationalError as err:
                print (err)
                continue
        elif "sqlite3" in SGBD:
            print "Sqlite3: "+SGBD_config[SGBD]["db_path"]
            try:
                connector=sqlite3.connect(SGBD_config[SGBD]["db_path"])
            except Exception as err:
                print "no sql3"
                print (err)
                continue
        else:
            print SGBD+" Not SGBD supported"

        cursor = connector.cursor()
        cursor.execute(query)
        data=cursor.fetchall()
        if data != None:
            """XML FILE"""
            xml_data=data2xml(data2xml(data, name='data'))
            writeOutput(OUTPUT_FOLDER+"GAC_"+SGBD+"_"+time.strftime("%Y%m%d_%H%M%S")+".xml",xml_data)

            """CSV FILE"""
            buildCsv(data,SGBD)

            """HTML FILE"""
            jsonObj = json.dumps(data)
            writeOutput(OUTPUT_FOLDER+"GAC_"+SGBD+"_"+time.strftime("%Y%m%d_%H%M%S")+".json",jsonObj)

            """HTML FILE"""
            html_doc=buildHtml(data,SGBD)
            writeOutput(OUTPUT_FOLDER+"GAC_"+SGBD+"_"+time.strftime("%Y%m%d_%H%M%S")+".html",html_doc)
        else:
            print "No data"
    #isinstance(object, classinfo)




# --------------------------------------------------------------------------------------------------
# Main exec
# --------------------------------------------------------------------------------------------------



def usage():
    """Method to display generator usage. """
    print """
Usage: python generador.py [options]

Options
-v, --version			Show the version of this script
-h, --help			Show this help.
-i <path>, --input <path>    	Input file
-o <path>, --output <path>     	Output file
-d,         --debug         	Debug Mode
"""

def version():
    """Function to display software version"""
    print "version 1.0"






if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(sys.argv[1:])
    else:
        usage()
        sys.exit()
