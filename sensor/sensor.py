import random
from datetime import datetime
import time
import pytz
import requests
import threading

CONTROLLER_ADDRESS = "http://controller:5000"

class Sensor():
    def __init__(self, id, address) -> None:
        self.id = id
        self.address = address
    
    def generate_timestamp(self):
        time = datetime.now(tz=pytz.timezone('Europe/Moscow')).replace(tzinfo=None).isoformat(timespec='seconds')
        return time

    def generate_msg(self):
        time = self.generate_timestamp()
        msg = {
            "id": self.id,
            'time': time,
            'payload': random.randint(-100, 100)
        }
        return msg
    
    def start(self):
        is_available = False
        while not(is_available):
            is_available = self.check_server()
            time.sleep(0.5)
        while True:
            try:
                self.send()
                time.sleep(0.002)
            except KeyboardInterrupt:
                print("KeyboardInterrupt")
            except Exception as err:
                print("Sensor error:", err)


    def send(self):
        msg = self.generate_msg()
        resp = requests.post(url=self.address+"/messages", json=msg)

    def check_server(self):
            try:
                req = requests.get(self.address+"/check")
                if (req.status_code == 200 and req.text == "Is alive"):
                    return True
                else:
                    return False
            except:
                return False

def run_sensor(sensor_id, address):
    sensor = Sensor(sensor_id, address)
    sensor.start()
    
if __name__ == "__main__":
    for i in range(8):
        thread = threading.Thread(target=run_sensor, args=(i, CONTROLLER_ADDRESS))
        thread.start()