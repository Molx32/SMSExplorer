import sys
from modules.target.target_receive_smss import ReceiveSMSS
from modules.target.target_mytempsms import MyTempSMS

from modules.data.data__module import Earnrwds, AirIndia

sys.path.extend(['../'])

class TargetInterface:
    
    def create_instance_receivesmss():
        return ReceiveSMSS()
    
    def create_instance_mytempsms():
        return MyTempSMS()

class ModuleInterface:

    def create_instance_mock():
        while 1:
            # Earnrwds()
            AirIndia()