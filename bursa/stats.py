from selebase.firefox import _Firefox
from selenium.webdriver.common.by import By
from utils.beautiful import Beautify
from utils.dataframe import Dataframe
from utils.regex import RegularExpression
import pandas as pd
from database.mongo import DatabaseMongo, TradingParticipation

table_dict_list = [
    {'colname': 'Participation', 'index': 0, 'cat' : 'text'},
    {'colname': 'Participation %', 'index': 1, 'cat' : 'text'},
    {'colname': 'Bought (RM Mil)', 'index': 2, 'cat' : 'text'},
    {'colname': 'Sold (RM Mil)', 'index': 3, 'cat' : 'text'},
    {'colname': 'Net (RM Mil)', 'index': 4, 'cat' : 'text'}
]


class Statistics(_Firefox):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.driver = self.get_driver()
        self.date_str = ''
    
    def get_trading_participation(self, updatedb = False):
        action_dict_list = [
            {'action' :'go_to' , 'params': {'url' :'https://www.bursamalaysia.com/market_information/market_statistic/securities'} } ,
            {'action' :'wait' , 'params': {'by': By.XPATH, 'selector' : "//table[@class = 'stacktable large-only']"}}
        ]

        self.do_action(action_dict_list)

        table_response = Beautify(self.driver.page_source).get_table_by_class(find_class = "stacktable large-only")
        participation_df = Dataframe(table_dict_list)
        participation_df.convert_based_format(table_response)

        participation_df.array_list_to_df()
        print(participation_df.dataframe)

        self.date_str = self.get_element(By.CLASS_NAME,"bm_footnote").text
        self.update_db(participation_df.dataframe)
        save_path = "C://source//participation//" + self.date_str + ".csv"
        participation_df.save_df_to_csv(save_path)
        self.quit_driver()

    def update_db(self, df ,type = 'mongo'):
        if type == 'mongo':
            record_db = TradingParticipation()
            record_db.Date = self.date_str
            record_db.Foreign_Bought = float(df['Bought (RM Mil)'][0].replace(',', ''))
            record_db.Foreign_Sold = float(df['Sold (RM Mil)'][0].replace(',', ''))
            record_db.Local_Institution_Bought = float(df['Bought (RM Mil)'][1].replace(',', ''))
            record_db.Local_Institution_Sold = float(df['Sold (RM Mil)'][1].replace(',', ''))
            record_db.Local_Retail_Bought = float(df['Bought (RM Mil)'][2].replace(',', ''))
            record_db.Local_Retail_Sold = float(df['Sold (RM Mil)'][2].replace(',', ''))
            mongodb = DatabaseMongo('db_test','192.128.1.130', item_object=record_db)
            mongodb.insert()

    def do_action(self, action_list):
        for action in action_list:
            self.action_dict[action.get('action')](**action.get('params'))