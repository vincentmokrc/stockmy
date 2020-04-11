from base import _BaseSelenium
import pandas as pd
import glob
import os
import shutil
from bs4 import BeautifulSoup
from os import path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class GetCompanyList(_BaseSelenium):

    tup_market_type = ('main_market', 'ace_market', 'leap_market', 'lfx_market', 'pn17_and_gn13_companies','change_of_name')
    
    
    def __init__(self, market_type : str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.driver = self.get_driver()
        listing_directory = "https://www.bursamalaysia.com/trade/trading_resources/listing_directory/"
        self.market_type = market_type
        self.url = listing_directory + self.market_type

    def _get_company_list(self):
        print(self.url)
        self.driver.get(self.url)
        self._wait(10)
        self.wait_until_presence(By.XPATH,"//table[@id = 'DataTables_Table_0']")
        
        selector = self.driver.find_element_by_xpath("//select[@name='DataTables_Table_0_length']/option[text()='All']")
        self.driver.execute_script("arguments[0].scrollIntoView();", selector)
        self._wait(5)
        selector.click()
        self._wait(1)
    
    def _get_bs4_content(self):
        soup = BeautifulSoup(self.driver.page_source,'html.parser')
        table = soup.find('table', id="DataTables_Table_0")
        table = table.tbody.find_all("tr") 
        return table

    def get_company_table(self):
        self._get_company_list()
        table = self._get_bs4_content()
        df = self._convert_to_df(table)
        print(df)
        df.to_csv(r'./companylist/ace.csv',index=False)
        self.quit_driver()
        return df

    def _convert_to_df(self, response):
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

                    print(code)
            
            row = [d.text.strip() for d in td]
            row.append(code)

            if row:
                res.append(row)

        df = pd.DataFrame(res)
        return df
