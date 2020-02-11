from config import config
import pyodbc






def get_employee_info(rfid):
    connection_info = config('config.ini', 'Database')
    driver = connection_info['driver']
    server_name = connection_info['server_name']
    database = connection_info['database_name']
    uid = connection_info['uid']
    password = connection_info['password']
    statement = "SELECT RFID.ID_RFID, Contractor.IDCard, Contractor.contractno, Contractor.FirstName, Contractor.LastName, Permission.Sub_Zone_Name, Permission.Date_exp FROM dbo.RFID AS RFID INNER JOIN dbo.Contractor AS Contractor ON RFID.IDCard = Contractor.IDCard INNER JOIN dbo.Permission AS Permission ON RFID.ID_RFID = Permission.ID_RFID WHERE (RFID.ID_RFID LIKE '%{0}%') AND  Permission.Sub_Zone_Name = 'Machine_Area'  AND Permission.Date_exp between  GETDATE() and  Permission.Date_exp".format(rfid)
    conn = pyodbc.connect('DRIVER={0};SERVER={1};DATABASE={2};UID={3};PWD={4}'.format(driver, server_name, database,
                                                                uid, password))
    cursor = conn.cursor()
    cursor.execute(statement)
    return cursor.fetchone()



def insert_inout_transaction(emp_info, type, door, dt, place_work):
    connection_info = config('config.ini', 'Database')
    driver = connection_info['driver']
    server_name = connection_info['server_name']
    database = connection_info['database_name']
    uid = connection_info['uid']
    password = connection_info['password']
    statement = "INSERT INTO dbo.inouttran(RFIDNO, TYPE, DOOR, IDCard, contractno, COMPUTERDATE, FirstName, LastName, PLACEWORK) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)"
    conn = pyodbc.connect('DRIVER={0};SERVER={1};DATABASE={2};UID={3};PWD={4}'.format(driver, server_name, database,
                                                                                      uid, password))
    cursor = conn.cursor()
    cursor.execute(statement, emp_info[0], type, door, emp_info[1], emp_info[2], dt, emp_info[3], emp_info[4], place_work)
    conn.commit()

if __name__ == '__main__':
    # pass
    # print(get_permission_info(5167))
    print(get_employee_info('142F'))
    # insert_inout_transaction(('6700379F93', '3471200157410', 'Pieceworkตามการจ้างงาน', 'สมพร', 'ทองแกม', 'shutdown_TL', datetime.datetime(2019, 12, 25, 23, 59, 59)), "IN", "Machine_Area",datetime.datetime.now(pytz.timezone('Asia/Bangkok')), "Z1-3")
