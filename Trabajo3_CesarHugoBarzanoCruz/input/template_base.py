# coding=utf8
# -*- coding: utf8 -*-
# vim: set fileencoding=utf8 :
import unicodedata


import time
import os
import mysql.connector as mysql
from datetime import datetime




class Model(object):
    """"""

    def __init__(self, model_no=None,atr_1=None,atr_2=None):
        self.model_no = model_no
        self.atr_1=atr_1
        self.atr_2=atr_2

    def get_as_json(self):
        """ Metodo que devuelve el objeto en formato Json """
        return self.__dict__

class ModelDriver(object):
    """ ItemsDriver implemeta las funcionalidades CRUD para administrar items """

    def __init__(self,user=None,password=None,host=None,database=None):
        # inizializar 
        # acceso a la base de datos
		# mysql.connector.connect(user='joe', database='test')
        self.user=user
        self.password=password
        self.host=host
        self.database=database
        self.connector=mysql.connect(user=self.user,password=self.password,host=self.host,database=self.database)
   
    def close(self):
        self.connector.close()

    def createModel(self, model):
        if model is not None:
             cursor = self.connector.cursor()
             model_json=model.get_as_json()
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
             self.connector.commit()
             cursor.close()
        else:
            raise Exception("Error Creating Model")

    def getModel(self,key,value):
        if key is not None and value is not None:
            query = ("SELECT * FROM gac_models WHERE "+str(key)+"="+str(value))
            cursor=self.connector.cursor()
            cursor.execute(query)
            data=cursor.fetchall()
            for d in data:
                print d
        else:
            raise Exception("Error Getting Model")


    def updateModel(self, model,key,value):
        if model is not None:
		    cursor = self.connector.cursor()
		    model_json=model.get_as_json()
		    fields=[]
		    formater=[]
		    values=[]
		    for key in model_json:
			    fields.append(key+"=%s")
			    values.append(model_json[key])
		    update_fields=""
		    for f in fields:
			    update_fields+=f+", "

		    update_fields = update_fields[:-2]
		    update_formater=str(tuple(formater)).replace("'","")
		
		    update_model = ("UPDATE gac_models SET "+update_fields+"  WHERE "+str(key)+"="+str(value))
		    data_model = tuple(values)
		    cursor.execute(update_model, data_model)
		    self.connector.commit()
		    cursor.close()
            
        else:
            raise Exception("Error Updating Model")


    def deleteModel(self,key,value):
	    if key is not None and value is not None:
		
		    query = ("DELETE FROM gac_models WHERE "+str(key)+"="+str(value))
		    cursor=self.connector.cursor()
		    cursor.execute(query)
		    self.connector.commit()
		    cursor.close()
	    else:
	        raise Exception("Error Deleting Model")




def main():

	model = Model(0001,"a","b")
	model2 = Model(0002,"a0","b0")
	modelDriver=ModelDriver("root","root","localhost","testGAC")
	modelDriver.createModel(model)
	modelDriver.createModel(model2)
	modelDriver.getModel("model_no",0001)
	modelDriver.getModel("model_no",0002)
	model3 = Model(0003,"update1","update2")
	modelDriver.updateModel(model3,"model_no",1)
	modelDriver.deleteModel("model_no",2)
	modelDriver.close()
 
main()  


    
