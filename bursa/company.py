from selebase.firefox import _Firefox
from selenium.webdriver.common.by import By
from utils.beautiful import Beautify
import pandas as pd

class CompanyList(_Firefox):

    def __init__(self, market_type : str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.driver = self.get_driver()
        listing_directory = "https://www.bursamalaysia.com/trade/trading_resources/listing_directory/"
        self.market_type = market_type
        self.url = listing_directory + self.market_type

    def _direct_to_company_list(self):
        print(self.url)
        self.go_url(self.url)
        self._wait(10)
        self.wait_until_presence(By.XPATH,"//table[@id = 'DataTables_Table_0']")
        selector = self.get_element(By.XPATH, "//select[@name='DataTables_Table_0_length']/option[text()='All']")
        self.driver.execute_script("arguments[0].scrollIntoView();", selector)
        self._wait(5)
        selector.click()
        self._wait(1)
    
    def get_list(self):
        self._direct_to_company_list()
        table_response = Beautify(self.driver.page_source).get_table_by_id(find_id = "DataTables_Table_0")
        df = self.convert_response_to_df(table_response)
        print(df)
        self.quit_driver()
        return df

    def convert_response_to_df(self, response):
        table = response
        res = []  
        code = 0
        for cell in table:
            td = cell.find_all('td')
            td2 = cell.find_all('td')[1:2]
            for d in td2: 
                a = d.find_all('a', href=True)
                for b in a:
                    code=b['href'].split('stock_code=')
                    if(len(code) > 1 ):
                        code = code[1]
                    else:
                        code = 0
            
            row = [d.text.strip() for d in td]
            row.append(code)

            if row:
                res.append(row)

        df = pd.DataFrame(res)
        return df