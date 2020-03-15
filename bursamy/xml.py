import pandas as pd
import glob
import os
import time
import re
from bs4 import BeautifulSoup

class XMLConvertor:
    def __init__(self, file_path):
        self.file_path = file_path
    
    def check_all_xml(self):
        file_list = []
        file_list = glob.glob(self.file_path + "//*xml")
        return file_list

    def open_xml(self):
        file_list = self.check_all_xml()
        soup_obj = []
        for file in file_list:
            print(file)
            with open(file, "r") as f:   
                contents = f.read()
                soup = BeautifulSoup(contents, 'lxml')
            
            soup_obj.append(soup)
        
        #return soup_obj