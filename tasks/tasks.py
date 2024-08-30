import time

def init_database():
    for i in range(1,100):
        print("init_database - " + str(i))
        time.sleep(1)
    return 1

def run_sms_collector():
    for i in range(1,100):
        print("run_sms_collector - " + str(i))
        time.sleep(1)
    return 1

def run_data_collector():
    for i in range(1,100):
        print("run_data_collector - " + str(i))
        time.sleep(1)
    return 1
