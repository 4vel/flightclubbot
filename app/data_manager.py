import logging
import pandas as pd
from config import DATAFILE_PATH

logging.basicConfig(level=logging.INFO)

fpth = DATAFILE_PATH

class DataManager:

    def __init__(self):
        self.destination_data = {}
        self.fpth = fpth

    def get_destination_data(self):
        df = pd.read_excel(self.fpth)
        self.destination_data = df.to_dict('records')
        return self.destination_data
