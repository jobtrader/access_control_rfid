import pytz
import datetime
from fastapi import FastAPI
from model import get_employee_info, insert_inout_transaction

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/access/rfid/{gate_number}")
def read_item(gate_number: str, id: str = None, type: str = None):
    permission_info = get_employee_info(id)
    dt = datetime.datetime.now(pytz.timezone('Asia/Bangkok'))
    print("Request at:", datetime.datetime.now(pytz.timezone('Asia/Bangkok')))
    if permission_info:
        insert_inout_transaction(permission_info, type, "Machine_Area", dt, "Z1-3")
        return 1
    return 0