import re
from datetime import datetime

class RegularExpression:

    @staticmethod
    def is_pattern_line(pattern, line):
        r =re.compile(pattern)
        return bool(r.match(line))

    @staticmethod
    def clean_num(num_string : str):
        
        bad_chars = '(),-'
        translator = str.maketrans('', '', bad_chars)
        clean_digits = num_string.translate(translator).strip()

        if clean_digits == '':
            return 0
        elif '(' in num_string:
            return -int(clean_digits)
        else:
            return int(clean_digits)

    @staticmethod
    def get_pattern_lines(pattern, lines):
        r = re.compile(pattern)
        match_list = list(filter(r.match, lines))
        return match_list

    @staticmethod
    def change_date_format(date_string):
        date = datetime.strptime(date_string, r'%d/%m/%Y')
        return date.strftime("%d %b %Y")