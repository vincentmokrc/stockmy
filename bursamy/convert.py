import pandas as pd
import glob
import os
import time

#call in linux as poppler in only linux
class PdfConverter(object):
    def __init__(self, dir):
        self.dir = dir
        self.output_dir = dir + "//xml"
        self.output_dir2 = dir + "//txt"

    def check_all_pdf(self):
        file_list = []
        file_list = glob.glob(self.dir + "//*pdf")
        return file_list

    def convert_to_xml(self, input_pdf , output_pdf):
        os.system('pdftohtml -c -hidden -xml '  + '"'+ input_pdf  +'"' + ' ' +'"'+  output_pdf + '"')
        time.sleep(4)
    
    def convert_to_text(self, input_pdf , output_pdf):
        os.system('pdftotext -layout '  + '"'+ input_pdf  +'"' + ' ' +'"'+  output_pdf + '"')
        time.sleep(4)

    def covert_all_to_xml(self):
        all_pdf = self.check_all_pdf()
        print(all_pdf)
        for pdf in all_pdf:
            head, tail = os.path.split(pdf)
            #print(head)
            #print(tail)
            print(os.path.join(self.output_dir, tail))
            self.convert_to_xml(pdf, os.path.join(self.output_dir, tail+".xml"))

    def convert_all_to_text(self):
        all_pdf = self.check_all_pdf()
        print(all_pdf)
        for pdf in all_pdf:
            head, tail = os.path.split(pdf)
            #print(head)
            #print(tail)
            print(os.path.join(self.output_dir2, tail))
            self.convert_to_text(pdf, os.path.join(self.output_dir2, tail+".txt"))
