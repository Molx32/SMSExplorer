from modules.data.data__module import *

from modules.data.data__module import AirIndia
from modules.data.data__module import Earnrwds
from modules.data.data__module import Moj
from modules.data.data__module import Superprof
from modules.data.data__module import Konto
from modules.data.data__module import SuitsMeCard
from modules.data.data__module import Booksy
from modules.data.data__module import Lilly
from modules.data.data__module import Rwdsuk
from modules.data.data__module import StickerMule
# from modules.data.data__module import Instagram
# from modules.data.data__module import Ukrwds

class DataInterface:

    def create_data_fetcher():
        while 1:
            try:
                AirIndia()
                # Instagram()
                Earnrwds()
                # Ukrwds() -- Need to execute JS
                Moj()
                Superprof()
                Konto()
                SuitsMeCard()
                Booksy()
                Lilly()
                Rwdsuk()
                StickerMule()
            except Exception as e:
                raise e
