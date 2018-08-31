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
TABLE="gac_models"

class Gac_models(object):
	""""""
	def __init__(self, model_no=None, atr_1=None, atr_2=None):

		self.model_no=model_no
		self.atr_1=atr_1
		self.atr_2=atr_2


	def get_as_json(self):
		""" Metodo que devuelve el objeto en formato Json """
		return self.__dict__


class Gac_modelsDriver(object):
	""" ItemsDriver implemeta las funcionalidades CRUD para administrar items """

	def __init__(self):

		self.user = USER
		self.password = PASSWORD
		self.host = HOST
		self.database = DATABASE
		self.table = TABLE
		self.connector = mysql.connect(user=self.user, password=self.password, host=self.host, database=self.database)

	def close(self):
		self.connector.close()

	def createGac_models(self, model):
		if model is not None:
			cursor = self.connector.cursor()
			model_json = model.get_as_json()
			fields = []
			formater = []
			values = []
			for key in model_json:
				fields.append(key)
				formater.append("%s")
				values.append(model_json[key])

			add_field = str(tuple(fields)).replace("'", "")
			add_formater = str(tuple(formater)).replace("'", "")
			add_model = ("INSERT INTO "+self.table +" " +add_field + " VALUES " + add_formater)
			data_model = tuple(values)
			cursor.execute(add_model, data_model)
			self.connector.commit()
			cursor.close()
		else:
			raise Exception("Error Creating Model")

	def getGac_models(self, key, value):
		if key is not None and value is not None:
			query = ("SELECT * FROM "+self.table+" WHERE " + str(key) + "=" + str(value))
			cursor = self.connector.cursor()
			cursor.execute(query)
			data = cursor.fetchall()
			for d in data:
				print d
		else:
			raise Exception("Error Getting Model")

	def updateGac_models(self, model, key, value):
		if model is not None:
			cursor = self.connector.cursor()
			model_json = model.get_as_json()
			fields = []
			formater = []
			values = []
			for key in model_json:
				fields.append(key + "=%s")
				values.append(model_json[key])
			update_fields = ""
			for f in fields:
				update_fields += f + ", "

			update_fields = update_fields[:-2]
			update_formater = str(tuple(formater)).replace("'", "")

			update_model = ("UPDATE "+self.table+" SET " + update_fields + "  WHERE " + str(key) + "=" + str(value))
			data_model = tuple(values)
			cursor.execute(update_model, data_model)
			self.connector.commit()
			cursor.close()

		else:
			raise Exception("Error Updating Model")

	def deleteGac_models(self, key, value):
		if key is not None and value is not None:

			query = ("DELETE FROM "+self.table+" WHERE " + str(key) + "=" + str(value))
			cursor = self.connector.cursor()
			cursor.execute(query)
			self.connector.commit()
			cursor.close()
		else:
			raise Exception("Error Deleting Model")


def main():
	model = Gac_models(0001, "a", "b")
	model2 = Gac_models(0002, "a0", "b0")
	model_Gac_models_Driver = Gac_modelsDriver()
	model_Gac_models_Driver.createGac_models(model)
	model_Gac_models_Driver.createGac_models(model2)
	model_Gac_models_Driver.getGac_models("model_no", 0001)
	model_Gac_models_Driver.getGac_models("model_no", 0002)
	model3 = Gac_models(0003, "update1", "update2")
	model_Gac_models_Driver.updateGac_models(model3, "model_no", 1)
	model_Gac_models_Driver.deleteGac_models("model_no", 1)
	model_Gac_models_Driver.deleteGac_models("model_no", 2)
	model_Gac_models_Driver.deleteGac_models("model_no", 3)
	model_Gac_models_Driver.close()

main()



