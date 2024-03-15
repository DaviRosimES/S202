import threading
from sensor import Sensor

sensor1 = Sensor("Sensor 1", "Celsius")
sensor2 = Sensor("Sensor 2", "Celsius")
sensor3 = Sensor("Sensor 3", "Celsius")


thread1 = threading.Thread(target=sensor1.generateTemp, args=(2,))
thread2 = threading.Thread(target=sensor2.generateTemp, args=(2,))
thread3 = threading.Thread(target=sensor3.generateTemp, args=(2,))

thread1.start()
thread2.start()
thread3.start()