import sys
from modules.target.target_receive_smss import ReceiveSMSS
from modules.target.target_mytempsms import MyTempSMS

sys.path.extend(['../'])

class TargetInterface:
    
    def create_instance_receivesmss():
        return ReceiveSMSS()
    
    def create_instance_mytempsms():
        return MyTempSMS()