from utils.regex import RegularExpression as regEx
from utils.file import FileOps as file

class Parser:
    def __init__(self, file_path):
        self.file_path = file_path
        self.all_lines = file.read_all_lines(file_path)
        self.pattern = r"^[A-Za-z-].+(-|([\(]?([0-9]?)?[,\.]?[0-9]+[\)]?))(\s|N/A|-)+(-|([\(]?[0-9]?[,\.]?[0-9]+[\)]?))"
    
    def restructure_lines(self):
        for idx , line in enumerate(self.all_lines ):
            if regEx.is_pattern_line(self.pattern, line):
                print(line, "-------Yes", idx)
                #print(re.split(r"(\s-\s.+|\(\d+.+|\d+.+)", line, maxsplit = 0))
                #print(line.split(r'(-|\(|\d+.+)', 2))
            else:
                #pass
                print(line, "-------No", idx)