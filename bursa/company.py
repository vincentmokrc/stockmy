from selebase.firefox import _Firefox
from selenium.webdriver.common.by import By
from utils.beautiful import Beautify
from utils.dataframe import Dataframe
import pandas as pd

table_dict_list = [
    {'colname': 'No', 'index': 0, 'cat' : 'text'},
    {'colname': 'Company', 'index': 1, 'cat' : 'text'},
    {'colname': 'Website', 'index': 2, 'cat' : 'text'},
    {'colname': 'Code', 'index': 1, 'cat' : 'link', 'partition':'stock_code='},
]


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
        df = Dataframe(table_dict_list)
        df.convert_based_format(table_response)
        df.array_list_to_df()
        df.save_df_to_csv("./source/companylist/"+ self.market_type +".csv")
        self.quit_driver()
        print(df.dataframe)
        return df.dataframe