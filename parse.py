import pandas as pd
import glob
import os
import time
import re
from bs4 import BeautifulSoup
import numpy as np


class XMLParser:
    def __init__(self, file):
        self.file = file
        self.soup = None
        self.whole_pdf = []
        pass

    def get_soup(self):
        with open(self.file, encoding='utf8') as f:   
            contents = f.read()
            soup = BeautifulSoup(contents, 'lxml')
            return soup

    def get_all_pages(self):
        soup = self.get_soup()
        pages = soup.findAll('page')
        return pages

    def convert_pages_to_df(self):
        page = self.get_all_pages()
        for singlepage in page:
            pagenum = singlepage.get('number')
            res = []
            for text in singlepage.findAll('text'):
                top = text.get('top')
                left = text.get('left')
                width = text.get('width')
                row = [pagenum, left, top, width, text.text.strip()]       
                res.append(row)
                df = pd.DataFrame(res, columns=["Page", "Left" ,"Top" ,"Width" ,"Content"])
            self.whole_pdf.append(df)

        return self.whole_pdf

    @staticmethod
    def concat_all_pages_df(wholepdf):
        #dfObj = pd.DataFrame(columns=["Page", "Left" ,"Top" ,"Width" ,"Content"])
        #for pdf in wholepdf:
        #    dfObj = dfObj.append(pdf)
        dfObj = pd.concat(wholepdf)
        
        dfObj = dfObj.astype({"Page": int , "Left": int, "Top": int, "Width": int, "Content": str})
        print(dfObj.dtypes)
        sortedObj = dfObj.sort_values(by = ['Page', 'Top', 'Left'])
        return sortedObj
