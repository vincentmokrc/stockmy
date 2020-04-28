from bursa.announcement import Announcement
from selebase.firefox import _Firefox


class FileDownloader(_Firefox):
    def __init__(self, symbol, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.symbol = symbol
        self.driver = self.get_driver()

    def download_file(self, url, target):
        pass
