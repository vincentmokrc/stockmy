import re
import locale

class TextParser():
    
    def __init__(self, file_path):
        self.path = file_path
        self.lineList = []
        self._read_all_lines()

    def _read_all_lines(self):
        with open(self.path, encoding='utf8') as f:   
            lines = [line.rstrip() for line in f]
        
        not_empty_lines = list(filter(lambda t: len(t) > 0, lines))
        self.lineList = [line.strip() for line in not_empty_lines]

    def _get_first_line_match(self, item):
        r = re.compile(item)
        newlist = list(filter(r.match, self.lineList)) # Read Note
        return newlist[0]
        
    def _get_all_numbers(self, item):
        x = re.findall('[\(]?[0-9]+[,]?[0-9]+[\)]?', item)
        return x

    def _clean_num(self,num_string):
        bad_chars = '(),-'
        translator = str.maketrans('', '', bad_chars)
        clean_digits = num_string.translate(translator).strip()

        if clean_digits == '':
            return 0
        elif '(' in num_string:
            return -int(clean_digits)
        else:
            return int(clean_digits) 

    def get_value(self, str_item):
        line = self._get_first_line_match(str_item)
        number = self._get_all_numbers(line)
        value = self._clean_num(number[0])
        print(str_item ,":", value)
        return value;

