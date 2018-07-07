# coding=utf8
# -*- coding: utf8 -*-
# vim: set fileencoding=utf8 :
import unicodedata


import time
import os
import mysql.connector as mysql
from datetime import datetime

USER="root"
PASSWORD="root"
HOST="127.0.0.1"
DATABASE="testGAC"




class hugo(object):
    """"""
    def __init__(self, model_no=None, atr_1=None, atr_2=None):

        self.model_no=model_no
        self.atr_1=atr_1
        self.atr_2=atr_2

    def createFromDB(self):

        atributes=[a for a in dir(self) if not a.startswith('__') and not callable(getattr(self, a))]
        print atributes
        for a in atributes:
            self.a="GGG"

    def get_as_json(self):
        """ Metodo que devuelve el objeto en formato Json """
        return self.__dict__

    def openConnector(self):
        connector=mysql.connect(user=USER,password=PASSWORD,host=HOST,database=DATABASE)
        return connector

    def createModel(self):
        connector=self.openConnector()
        cursor = connector.cursor()
        model_json=self.get_as_json()
        fields=[]
        formater=[]
        values=[]
        for key in model_json:
            fields.append(key)
            formater.append("%s")
            values.append(model_json[key])

        add_field=str(tuple(fields)).replace("'","")
        add_formater=str(tuple(formater)).replace("'","")
        add_model = ("INSERT INTO gac_models "+add_field+" VALUES "+add_formater)
        data_model = tuple(values)
        cursor.execute(add_model, data_model)
        connector.commit()
        cursor.close()

    def getModel(self, key, value):
        if key is not None and value is not None:
            query = ("SELECT * FROM gac_models WHERE " + str(key) + "='" + str(value)+"'")
            connector = self.openConnector()
            cursor = connector.cursor()
            cursor.execute(query)
            data = cursor.fetchall()
            print data

            modelg = hugo(data[0])
            return modelg


        else:
            raise Exception("Error Getting Model")


def main():
    model2 = hugo(6666, "s", "t")
    model2.createFromDB()
    print model2.atr_1
    exit()
    model = hugo(0001,"a","b")
    #model.createModel()
    model.createFromDB()
    exit(1)
    modelgetter=model.getModel("atr_1","a")
    json_model=modelgetter.get_as_json()
    print json_model




 
main()  


    
