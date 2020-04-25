from bursa.table import _Table
from utils.dataframe import Dataframe
import pandas as pd

table_dict_list = [
    {'colname': 'No', 'index': 0, 'cat' : 'text'},
    {'colname': 'Date', 'index': 1, 'cat' : 'text'},
    {'colname': 'Company', 'index': 2, 'cat' : 'text'},
    {'colname': 'Title', 'index': 3, 'cat' : 'text'},
    {'colname': 'ID', 'index': 3, 'cat' : 'link'}
]

class Announcement(_Table):
    def __init__(self, symbol, retry_count=3, pause=0.1, timeout=30, session=None, freq=None):
        super().__init__(symbol, retry_count=retry_count, pause=pause, timeout=timeout, session=session, freq=freq)
        self.url = "https://www.bursamalaysia.com/market_information/announcements/company_announcement?"
        self.params_list = []

    def _get_announcement_table(self, cat, sub_type, format):
        self.raw_df = pd.DataFrame(columns=Dataframe(format).get_column_name())
        try:
            for x in range(30):
                params = {'cat': cat ,'sub_type' : sub_type , 'company' : self.symbol , 'per_page' : 50 , 'page' : x}
                self.params_list.append(params)

            for param in self.params_list:
                df = self.get_table(self.url, param , format, "table-announcements")
                self.raw_df = pd.concat([self.raw_df, df], ignore_index=True)
                
                if(len(df) < 50):
                    break;
                
            return self.raw_df
        
        finally:
            self.close()

    def get_financial_result(self):
        cat = "FA"
        sub_type = "FA1"
        dataframe = self._get_announcement_table(cat, sub_type, table_dict_list)
        print(dataframe)
