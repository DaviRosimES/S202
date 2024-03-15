import random # biblioteca para gerar valores aleatórios de temperatura
import time # biblioteca para dar um intervalo em cada amostra do sensor
from pymongo import MongoClient # biblioteca para conectar ao MongoDB
from datetime import datetime # biblioteca para conseguir o timestamp

class Sensor:
    # Construtor
    def __init__(self, nomeSensor, unidadeMedida):
        # Iniciando as variáveis
        self.nomeSensor = nomeSensor
        self.unidadeMedida = unidadeMedida
        self.sensorAlarmado = False
        # Conectando ao MongoDB
        self.client = MongoClient('mongodb://localhost:27017')
        self.db = self.client['bancoiot']
        self.collectionSensorTimeSeries = self.db['sensores_time_series']

    # Gera uma temperatura aleatória em um intervalo dado e já envia os dados para o banco de dados
    def generateTemp(self, intervalo):
        while not self.sensorAlarmado:
            valorSensor = round(random.uniform(30, 40), 2)
            leitura = {
                "nomeSensor": self.nomeSensor,
                "valorSensor": valorSensor,
                "unidadeMedida": self.unidadeMedida,
                "sensorAlarmado": self.sensorAlarmado,
                "timestamp": datetime.now()
            }
            if valorSensor > 38:
                self.sensorAlarmado = True
                leitura["sensorAlarmado"] = True
                print(f"Atenção! Temperatura muito alta! Verificar {self.nomeSensor}!")
            else:
                print(f"{self.nomeSensor} captou {valorSensor} ºC")
            self.collectionSensorTimeSeries.insert_one(leitura)
            time.sleep(intervalo)