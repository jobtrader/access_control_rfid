import pytz
import datetime
from fastapi import FastAPI
from model import get_employee_info_in, insert_inout_transaction, get_employee_info_out
import requests
from config import config
import json


app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/access/rfid/{gate_number}")
def read_item(gate_number: str, id: str = None, type: str = None):
    dt = datetime.datetime.now(pytz.timezone('Asia/Bangkok'))
    print("Request at:", datetime.datetime.now(pytz.timezone('Asia/Bangkok')))
    gate_type = config('config.ini', 'DoorType')
    gate_in = eval(gate_type['in'])
    gate_out = eval(gate_type['out'])
    if gate_number in gate_in:
        permission_info = get_employee_info_in(id)
    elif gate_number in gate_out:
        permission_info = get_employee_info_out(id)
    else:
        print('Wrong gate name')
        return 0
    if permission_info:
        insert_inout_transaction(permission_info, type, "Machine_Area", dt, "Z1-3")
        gate_ip = config('config.ini', 'Gate')
        raw_gate_number = gate_number
        gate_number = gate_number.lower()
        if gate_number in gate_ip:
            gate_ip = config('config.ini', 'Gate')[gate_number]
            url = 'http://{0}/display?type={1}&id={2}&gate={3}'.format(gate_ip, type, id, raw_gate_number)
            response = requests.get(url)
            print('Request to display @ {0}'.format(gate_ip))
            result = json.loads(response.text)
            print(result)
            if result['result'] == 'complete':
                print('Displayed Credential Info of ID = {0} at Gate = {1}'.format(id, gate_number))

            else:
                print('Failed to Display Credential Info of ID = {0} at Gate = {1}'.format(id, gate_number))
        return 1
    return 0