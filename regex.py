import re
import locale
import typing

class RegularExp():

    def __init__(self, input_text):
        self.input_lines = input_text
        self.pattern = r"^[A-Za-z-].+(-|([\(]?([0-9]?)?[,\.]?[0-9]+[\)]?))(\s|N/A|-)+(-|([\(]?[0-9]?[,\.]?[0-9]+[\)]?))"

    def get_all_not_empty_lines(self):
        not_empty_lines = list(filter(lambda t: len(t) > 0, self.input_lines))
        solid_lines = [line.strip() for line in not_empty_lines]
        return solid_lines

    @staticmethod
    def get_pattern_lines(pattern, lines):
        r = re.compile(pattern)
        match_list = list(filter(r.match, lines))
        return match_list
    
    @staticmethod
    def is_pattern_line(pattern, line):
        r =re.compile(pattern)
        return bool(r.match(line))

    @staticmethod
    def _clean_num(num_string : str):
        bad_chars = '(),-'
        translator = str.maketrans('', '', bad_chars)
        clean_digits = num_string.translate(translator).strip()

        if clean_digits == '':
            return 0
        elif '(' in num_string:
            return -int(clean_digits)
        else:
            return int(clean_digits) 
    
    def restructure_lines(self):
        lines = self.get_all_not_empty_lines()
        for idx , line in enumerate(lines):
            if self.is_pattern_line(self.pattern, line):
                print(line, "-------Yes", idx)
                #print(re.split(r"(\s-\s.+|\(\d+.+|\d+.+)", line, maxsplit = 0))
                #print(line.split(r'(-|\(|\d+.+)', 2))
            else:
                #pass
                print(line, "-------No", idx)

        