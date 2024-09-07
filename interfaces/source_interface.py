from modules.sources.receive_smss import ReceiveSMSS
from modules.sources.mytempsms import MyTempSMS

class TargetInterface:
    
    def create_instance_receivesmss():
        return ReceiveSMSS()
    
    def create_instance_mytempsms():
        return MyTempSMS()