from bursamy.table import GetTable
import time
from bursamy.file import GetPdf

class BursaFileDownloader(object):
    def __init__(self, symbol):
        self.symbol = symbol
        
    def get_financial_result(self):
        content_df = GetTable(self.symbol).financial_result()
        print(content_df)
        GetPdf().download_all_pdf(content_df)