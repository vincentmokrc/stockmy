from bs4 import BeautifulSoup

class Beautify:

    def __init__(self, source, parser = 'html.parser', *args, **kwargs):
        parser = parser
        self.soup = BeautifulSoup(source, parser)

    def get_table_by_id(self, *args, **kwargs):
        id_find = kwargs.get("find_id", None)
        table = self.soup.find('table', id = id_find)
        whole_table = table.tbody.find_all("tr") 
        return whole_table