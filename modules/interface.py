import sys
from modules.target.target_receive_smss import ReceiveSMSS

sys.path.extend(['../'])

class TargetInterface:
    
    def create_instance_receivesmss():
        return ReceiveSMSS()
    
