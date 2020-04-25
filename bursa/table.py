from utils.session import _SendRequest
from utils.beautiful import Beautify
from utils.dataframe import Dataframe
import pandas as pd

class _Table(_SendRequest):
    def __init__(self, symbol, retry_count=3, pause=0.1, timeout=30, session=None, freq=None):
        super().__init__(retry_count=retry_count, pause=pause, timeout=timeout, session=session, freq=freq)
        self.symbol = symbol
        #self.df = pd.DataFrame()
    
    def get_table(self, url, param, format , id_find):
        res = self._get_response(url, params=param)
        beauty_res = Beautify(res.content).get_table_by_id(find_id = id_find)
        data = Dataframe(format)
        data.convert_based_format(beauty_res)
        data.array_list_to_df()
        return data.dataframe

    def get_all_table(self, url, params, header, id_find):
        try:
            df2 = pd.DataFrame(columns=header)
            for param in params:
                res = self._get_response(url, params=param)
                beauty_res = Beautify(res).get_table_by_id(id_find)
                data = Dataframe(beauty_res)
                data.convert_to_df()
                df = data.dataframe
                df2 = pd.concat([df2, df], ignore_index=True)
        
            return df2

        finally:
            self.close()
    
    def concat_df(self, input_df, format):      
        self.df = pd.concat([self.df, input_df])

    @property
    def df(self):
        return self.df