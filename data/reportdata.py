from data.basedata import AttrPosData

class AtrrPosData:
    def __init__(self,name, x, y, content ):
        self._name = name
        self._x = x
        self._y = y
        self._content = content
    
    @property
    def name(self):
        return self._name

class FormatPage(object):

    def __init__(self, cat, pagenum):
        self.cat = cat
        self.pagenum = pagenum
        self.list_attr = []

    def get_cat(self):
        return self.cat
        
    def add_info(self, name , x, y, content):
        self.list_attr.append(AtrrPosData(name,x,y,content))

    def get_info(self, index):
        self.list_attr[index]

    def get_all_info(self):
        return self.list_attr

class ReportFormat():

    def __init__(self, code):
        self.code = code
        self.page = []

    def add_page(self, cat, pagenum):
        self.page.append(FormatPage(cat,pagenum))

    def get_page(self, pagenum):
        return self.page[pagenum]

    def get_all_page(self):
        return self.page

    def add_page_info(self, page,name, x, y, content):
        self.page[page].add_info(name , x, y, content)

    def get_page_info(self,page,index):
        all_info = self.get_page_all_info(page)
        data = all_info[index].name
        return data

    def get_page_all_info(self,page):
        return self.page[page].get_all_info()