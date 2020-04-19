import requests
from _utils import _init_session, _convert_res_to_df, _init_selenium_session
import time
from pandas.io.common import urlencode
from bs4 import BeautifulSoup
import pandas as pd

import os
import pdb
import platform
import time

from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options

class _SendRequest(object):
    
    def __init__(
        self,
        retry_count=3,
        pause=0.1,
        timeout=30,
        session=None,
        freq=None,
        ):
        
        if not isinstance(retry_count, int) or retry_count < 0:
            raise ValueError("'retry_count' must be integer larger than 0")
        self.retry_count = retry_count
        self.pause = pause
        self.timeout = timeout
        self.pause_multiplier = 1
        self.session = _init_session(session, retry_count)
        self.freq = freq

    def close(self):
        self.session.close()

    def read_table(self):
        """Read data from connector"""
        try:
            response_bs4 = self._get_bs4_content(self.url, self.params)
            df = _convert_res_to_df(response_bs4)
            return df
        finally:
            self.close()

    def read_all_table(self):
        try:
            df2 = pd.DataFrame(columns=["No" ,"Release Date" ,"Company" ,"Content" ,"Link ID"])
            for params in self.params_list:
                response_bs4 = self._get_bs4_content(self.url, params)
                df = _convert_res_to_df(response_bs4)
                df2 = pd.concat([df2, df], ignore_index=True)

                #Dont drop into trap if less than a table row set
                if(len(df) < params['per_page']):
                    break
            
            del df2['No']
            return df2

        finally:
            self.close()

    def _get_bs4_content(self, url, params):

        res = self._get_response(url,params= params)
        print("*********" + res.url + "*********")
        soup = BeautifulSoup(res.content,'html.parser')
        table_announcements_bs4 = soup.find("table", attrs={"id": "table-announcements"})
        table_announcements_bs4 = table_announcements_bs4.tbody.find_all("tr") 
        return table_announcements_bs4 
    

    def _get_response(self, url, params = None, headers = None):
        pause = self.pause
        last_response_text = ""
        for _ in range(self.retry_count + 1):
            response = self.session.get(url, params=params, headers=headers)
            if response.status_code == requests.codes.ok:
                return response

            if response.encoding:
                last_response_text = response.text.encode(response.encoding)
            time.sleep(pause)

            pause *= self.pause_multiplier

            if self._output_error(response):
                break

        if params is not None and len(params) > 0:
            url = url + "?" + urlencode(params)
        msg = "Unable to read URL: {0}".format(url)
        if last_response_text:
            msg += "\nResponse Text:\n{0}".format(last_response_text)

        print(msg)

    def _output_error(self, out):
        return False


class _BaseSelenium(object):
    def __init__(self, *args, **kwargs):
        self.save_directory = "C:\\report_pdf"
        pass

    def get_driver(self):
        if hasattr(self, 'driver') and self.driver:
            return self.driver
        
        options = Options()
        options.headless = False
        
        fp = webdriver.FirefoxProfile()

        fp.set_preference("browser.download.folderList", 2)
        fp.set_preference("browser.download.manager.showWhenStarting",False)
        fp.set_preference("browser.download.dir", self.save_directory)
        fp.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/pdf,application/x-pdf,application/vnd.openxmlformats-officedocument.wordprocessingml.document")

        fp.set_preference("pdfjs.disabled", True)  # < KEY PART HERE

        driver = webdriver.Firefox(options = options, firefox_profile=fp)

        while len(driver.window_handles) > 1:
            driver.switch_to.window(driver.window_handles[1])
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
            self._wait(2)

        return driver

    def quit_driver(self):
    
        self.driver.quit()

    def wait_until_presence(self, by, selector, source=None, *args, **kwargs):
        source = source or self.driver
        WebDriverWait(source,10).until(EC.presence_of_element_located((by ,selector)))
        return True

    def perform_action(func):
        def wrapper(self, by, selector, *args, **kwargs):
            retry = 0
            success = False

            try:
                max_retries = int(kwargs.get('max_retries', 5))
            except ValueError:
                max_retries = 5

            try:
                timeout = int(kwargs.get('timeout', 0))
            except ValueError:
                timeout = 0

            return_method = func.__name__.startswith('get_')
            raise_exception = kwargs.get('raise_exception', True)

            if timeout:
                self._wait(timeout)

            while not success:
                retry += 1

                if retry > max_retries:
                    if raise_exception:
                        self._start_debug()
                        raise TimeoutException
                    else:
                        return success

                try:
                    if not isinstance(selector, (list, tuple)):
                        selector = [selector]
                        
                    for s in selector:
                        try:
                            self.logger(data={
                                'action': func.__name__,
                                'selector': s,
                                'args': args,
                                'retry': retry,
                            })
                            response = func(self, by, s, *args, **kwargs)
                            success = True
                            break
                        except Exception:
                            pass
                    if not success:
                        raise TimeoutException
                except (TimeoutException, WebDriverException):
                    self._wait(1)

            return response if return_method else success

        return wrapper

    @perform_action
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

    @perform_action
    def clear_input(self, by, selector, source=None, *args, **kwargs):
        source = source or self.driver
        element = source.find_element(by, selector)
        element.clear()

    @perform_action
    def fill_input(self, by, selector, content, source=None, *args, **kwargs):
        source = source or self.driver
        element = source.find_element(by, selector)
        element.send_keys(content)

    @perform_action
    def get_text(self, by, selector, source=None, *args, **kwargs):
        source = source or self.driver
        element = source.find_element(by, selector)
        return element.text

    @perform_action
    def get_element(self, by, selector, source=None, *args, **kwargs):
        source = source or self.driver
        element = source.find_element(by, selector)
        return element

    @perform_action
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
