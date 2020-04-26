import pandas as pd
import re

class Dataframe:
    def __init__(self, format):
        self.format = format
        self.list_array = []
        self.init_table_list()


    def init_table_list(self):
        for i in self.format:
            self.list_array.append(list())
        
    def convert_based_format(self, response):
        table_announcements = response
        for i in range(len(self.list_array)):
            self.list_array[i].clear()

        for cell in table_announcements:
            td = cell.find_all('td')
            for i in range(len(self.list_array)):
                if(i < len(td)):
                    if(self.format[i].get('cat') == 'text'):
                        text = td[i].text.strip()
                else:
                    if(self.format[i].get('cat') == 'link'):
                        k = self.format[i].get('index')
                        text = td[k].find('a').get('href')
                
                if self.format[i].get('partition') is not None:
                    
                    before_keyword, keyword, after_keyword = text.partition(self.format[i].get('partition'))

                    if(len(after_keyword)> 0):
                        self.list_array[i].append(str(after_keyword))
                    else:
                        self.list_array[i].append('0')
                else:
                    self.list_array[i].append(text)
                
    @property
    def array_list(self):
        if hasattr(self, 'list_array'):
            return self.list_array

    def array_list_to_df(self):
        list_tuple = list(zip(*self.list_array))
        column_name = self.get_column_name()
        self.df = pd.DataFrame(list_tuple,columns= column_name)

    def get_column_name(self):
        column_name = []

        for i in range(len(self.format)):
            column_name.append(self.format[i].get('colname'))
        
        return column_name
        

    def convert_to_df(self, response):
        table = response
        res = []  
        code = 0
        for cell in table:
            td = cell.find_all('td')
            row = [d.text.strip() for d in td]
            row.append(code)

            if row:
                res.append(row)

        self.df = pd.DataFrame(res)

    @property
    def dataframe(self):
        
        if hasattr(self, 'df'):
            return self.df
        
        return AttributeError()
        
    
    def save_df_to_csv(self, path):
        if hasattr(self, 'df'):
            self.df.to_csv(path)
        else:
            print("No dataframe converted yet!")