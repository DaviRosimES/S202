import random
import time
from pymongo import MongoClient

class Sensor:
    def __init__(self, nomeSensor, unidadeMedida):
        #Iniciando as variáveis
        self.nomeSensor = nomeSensor
        self.unidadeMedida = unidadeMedida
        self.sensorAlarmado = False
        #Conectando ao MongoDB
        self.client = MongoClient('mongodb://localhost:27017')
        self.db = self.client['bancoiot']
        self.sensores = self.db['sensores']

    def generateTemp(self, intervalo):
        while not self.sensorAlarmado:
            valorSensor = round(random.uniform(30, 40), 2)
            if valorSensor > 38:
                self.sensorAlarmado = True
                self.sensores.update_one(
                    {"nomeSensor": self.nomeSensor},
                    {"$set": {"valorSensor": valorSensor, "unidadeMedida": self.unidadeMedida, "sensorAlarmado": True}}
                )
                print(f"Atenção! Temperatura muito alta! Verificar {self.nomeSensor}!")
            else:
                self.sensores.update_one(
                    {"nomeSensor": self.nomeSensor},
                    {"$set": {"valorSensor": valorSensor, "unidadeMedida": self.unidadeMedida, "sensorAlarmado": False}}
                )
                print(f"{self.nomeSensor} captou {valorSensor} ºC")
            time.sleep(intervalo)