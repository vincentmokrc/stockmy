from selebase.firefox import _Firefox
from selenium.webdriver.common.by import By
from utils.beautiful import Beautify
from utils.dataframe import Dataframe
import pandas as pd


class Statistics(_Firefox):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.driver = self.get_driver()
        self.go_url("https://www.bursamalaysia.com/market_information/market_statistic/securities")
    
    def get_trading_participation(self):
        self.wait_until_presence(By.XPATH,"//table[@class = 'stacktable large-only']")
        table_response = Beautify(self.driver.page_source).get_table_by_class(find_class = "stacktable large-only")
        participation_df = Dataframe(table_response)
        participation_df.convert_to_df()

        print(participation_df.dataframe)

        date_str = self.get_element(By.CLASS_NAME,"bm_footnote").text

        save_path = "./source/participation/" + date_str + ".csv"
        participation_df.save_df_to_csv(save_path)
        self.quit_driver()