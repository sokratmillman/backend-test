from flask import Flask, request
from utils import read_history, update_history
import time
from datetime import datetime
import threading
import socket
import sys
import pytz
import json
import logging

app = Flask(__name__)
log = logging.getLogger('werkzeug')
log.setLevel(logging.WARNING)

@app.route("/check")
def indicate_live():
    return "Is alive"

@app.route("/messages", methods = ["POST"])
def message():
    global curr_payload
    global curr_number_of_requests
    curr_payload = curr_payload + request.json['payload']
    curr_number_of_requests += 1
    return "Hello!"

@app.route("/history", methods=["GET"])
def history():
    unsuccess = True
    while unsuccess:
        try:
            history_str = read_history()
            unsuccess = False
        except:
            pass
    return history_str

def execute_each_five_secs():
    global curr_number_of_requests
    global curr_payload
    IP = "manipulator"
    PORT = 32007
    tz=pytz.timezone("Europe/Moscow")
    time_start = datetime.now(tz=tz).time().isoformat('seconds')
    time_end = ''

    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((IP, PORT))
        first_msg = client.recv(1024).decode("utf-8")
        new_port = int(first_msg)
        new_address = (IP, new_port)
        client.close()

        new_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        new_client.connect(new_address)
        while True:
            date = datetime.now(tz=tz).replace(tzinfo=None).isoformat(timespec='seconds')
            status = "down"
            if (curr_payload/max(curr_number_of_requests, 1) > 0):
                status = "up"
            
            curr_payload = 0
            curr_number_of_requests = 0

            message = {
                'datetime': date,
                'status': status
            }

            new_client.send(json.dumps(message).encode("utf-8"))
            new_client.recv(1024).decode("utf-8")

            time_end = datetime.now(tz=tz).time().isoformat('seconds')
            update_history(time_start, time_end, status)
            time_start = time_end
            time.sleep(5)

    except Exception as err:
        print("Controller error:", err)

if __name__=='__main__':
    curr_payload = 0
    curr_number_of_requests = 0
    history_thread = threading.Thread(target=execute_each_five_secs)
    history_thread.start()
    app.run(host="0.0.0.0", port=5000)