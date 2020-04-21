from abc import ABC, abstractmethod
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
import time
from selenium.webdriver.common.action_chains import ActionChains

class _Selenium(ABC):
    def __init__(self, *args, **kwargs):
        pass
        
    @abstractmethod
    def get_driver(self):raise NotImplementedError

    def quit_driver(self):
        self.driver.quit()

    def wait_until_presence(self, by, selector, source=None, *args, **kwargs):
        source = source or self.driver
        WebDriverWait(source,10).until(EC.presence_of_element_located((by ,selector)))
        return True

    def click_element(
        self, by, selector, source=None, move=False, *args, **kwargs
    ):
        final_source = source or self.driver
        element = final_source.find_element(by, selector)

        if move:
            ActionChains(self.driver) \
                .move_to_element(source or element) \
                .perform()

        disabled = element.get_attribute('aria-disabled')
        if disabled == 'true':
            self._wait(5)
            raise WebDriverException
        element.click()

    def clear_input(self, by, selector, source=None, *args, **kwargs):
        source = source or self.driver
        element = source.find_element(by, selector)
        element.clear()

    def fill_input(self, by, selector, content, source=None, *args, **kwargs):
        source = source or self.driver
        element = source.find_element(by, selector)
        element.send_keys(content)

    def get_text(self, by, selector, source=None, *args, **kwargs):
        source = source or self.driver
        element = source.find_element(by, selector)
        return element.text

    def get_element(self, by, selector, source=None, *args, **kwargs):
        source = source or self.driver
        element = source.find_element(by, selector)
        return element

    def get_elements(self, by, selector, source=None, *args, **kwargs):
        source = source or self.driver
        elements = source.find_elements(by, selector)
        if len(elements) == 0:
            raise WebDriverException
        return elements

    def handle(self):
        raise NotImplementedError("`handle` nor implemented in the Base.")

    def _wait(self, seconds):
        for second in range(seconds):
            print('Wait: {:d}/{:d}'.format(second + 1, seconds))
            time.sleep(1)

    def go_url(self, url):
        self.driver.get(url)
    