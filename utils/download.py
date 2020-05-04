from bursa.announcement import Announcement
from selebase.firefox import _Firefox
from abc import ABC, abstractmethod


class FileDownloader(_Firefox):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.driver = self.get_driver()

    @abstractmethod
    def download_file(self, *args, **kwargs):
        pass
