import pandas as pd

class Dataframe:
    def __init__(self, response):
        self.response = response

    def convert_to_df(self):
        table = self.response
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