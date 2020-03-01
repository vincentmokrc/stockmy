import requests
import pandas as pd
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

def _init_session(session, retry_count=3):
    if session is None:
        session = requests.Session()
        # do not set requests max_retries here to support arbitrary pause
    return session

def _init_selenium_session(session, retry_count=3):
    if session is None:
        options = Options()
        options.headless = True
        session = webdriver.Firefox(options=options)
    return session

def _convert_res_to_df(response):
        table = response
        res = []  
        link = ""
        for cell in table:
            td = cell.find_all('td')
            tags = cell.find_all('a')[1:2]
            for tag in tags:
                link = tag.get('href')
            row = [i.text.strip() for i in td]
            row.append(link.split('ann_id=')[1])
            res.append(row)

        df = pd.DataFrame(res, columns=["No" ,"Release Date" ,"Company" ,"Content" ,"Link ID"])
        return df