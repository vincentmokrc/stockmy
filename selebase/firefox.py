from selebase.base import _Selenium
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

class _Firefox(_Selenium):
    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)
        self.save_dir = kwargs.get('save_dir','C:\\report_pdf')

    def get_driver(self):
        if hasattr(self, 'driver') and self.driver:
            return self.driver

        options = Options()
        options.headless = False
        
        fp = webdriver.FirefoxProfile()

        fp.set_preference("browser.download.folderList", 2)
        fp.set_preference("browser.download.manager.showWhenStarting",False)
        fp.set_preference("browser.download.dir", self.save_dir)
        fp.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/pdf,application/x-pdf,application/vnd.openxmlformats-officedocument.wordprocessingml.document")

        fp.set_preference("pdfjs.disabled", True)  # < KEY PART HERE

        driver = webdriver.Firefox(options = options, firefox_profile=fp)

        while len(driver.window_handles) > 1:
            driver.switch_to.window(driver.window_handles[1])
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
            self._wait(2)

        return driver
