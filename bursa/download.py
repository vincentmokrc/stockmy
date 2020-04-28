from bursa.announcement import Announcement
from selebase.firefox import _Firefox


class FileDownloader(_Firefox):
    def __init__(self, symbol, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.symbol = symbol
        self.driver = self.get_driver()

    def do_action(self, action_list):raise NotImplementedError

    def download_file(self, url):
        pass


    def download_finiancial_result(self):
        df = Announcement(self.symbol).get_financial_result()
        #print(df)
        print(df['ID'])
        self.quit_driver()