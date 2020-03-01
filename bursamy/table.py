from base import _SendRequest
from data.bursadata import *

class GetTable(_SendRequest):
    def __init__(self, symbol , retry_count=3, pause=0.1, timeout=30, session=None, freq=None):
        super().__init__(retry_count=retry_count, pause=pause, timeout=timeout, session=session, freq=freq)
        self.symbol = symbol

    def financial_result(self):
        self.url = "https://www.bursamalaysia.com/market_information/announcements/company_announcement?"
        #self.params = {'cat': AnnouncementCategory.FinancialResults['Symbol'] , 'company' : self.symbol , 'per_page' : 50 , 'page' : 1}
        self.params_list = []
        for x in range(30):
            params = {'cat': AnnouncementCategory.FinancialResults['Symbol'] , 'company' : self.symbol , 'per_page' : 50 , 'page' : x}
            self.params_list.append(params)
        
        content = self.read_all_table()
        return content
        #return self.params_list

