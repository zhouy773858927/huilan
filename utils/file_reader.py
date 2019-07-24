"""
文件读取。YamlReader读取yaml文件，ExcelReader读取excel。
"""
import yaml
import os
from xlrd import open_workbook

class YamlReader:
    def __init__(self,yamlf):
        if os.path.exists(yamlf):
            self.yamlf = yamlf
        else:
            raise FileNotFoundError('文件不存在！')
        self._data = None

    @property
    def data(self):
        #如果是第一次调用data,读取yaml文件，否则直接返回之前保存的数据
        if not self._data:
            with open(self.yamlf,'rb') as f:
                self._data = list(yaml.safe_load_all(f))# load后是个generator，用list组织成列表
        return self._data

class SheetTypeError(Exception):
    pass

class ExcelReader:
    """
     读取excel文件中的内容。返回list。
     如：
     excel中内容为：
     | A  | B  | C  |
     | A1 | B1 | C1 |
     | A2 | B2 | C2 |
     如果 print(ExcelReader(excel, title_line=True).data)，输出结果：
     [{A: A1, B: B1, C:C1}, {A:A2, B:B2, C:C2}]
     如果 print(ExcelReader(excel, title_line=False).data)，输出结果：
     [[A,B,C], [A1,B1,C1], [A2,B2,C2]]
     可以指定sheet，通过index或者name：
     ExcelReader(excel, sheet=2)
     ExcelReader(excel, sheet='BaiDuTest')

    title_line参数，用来声明是否在excel表格里有标题行，如果有标题行，返回dict列表，否则返回list列表
    如果title_line=True
    [{"title1": "value1", "title2": "value2"}, {"title1": "value3", "title2": "value4"}]
    如果title_line=False
    [["title1", "title2"], ["value1", "value2"], ["value3", "value4"]]
    """
    def __init__(self,excel,sheet=0,title_line=True):
        if  os.path.exists(excel):
            self.excel = excel
        else:
            raise FileNotFoundError('文件不存在！')
        self.sheet = sheet
        self.title_line = title_line
        self._data = list()

    @property
    def data(self):
        if not self._data:
            workbook = open_workbook(self.excel)
            #判断excel表中sheet的属性并取值
            if type(self.sheet) not in [int,str]:
                raise SheetTypeError('Please pass in <type int> or <type str>,not{0}'.format(self.sheet))
            elif type(self.sheet) == int:
                s = workbook.sheet_by_index(self.sheet)
            else:
                s = workbook.sheet_by_name(self.sheet)

            if self.title_line:
                title = s.row_values(0)#首行为title
                for col in range(1, s.nrows):
                    #依次遍历其余行，与第一行组成dict字典，拼接到self._data中
                    self._data.append(dict(zip(title,s.row_values(col))))
            else:
                for col in range(0,s.nrows):
                    #遍历所有行，拼到self._data中
                    self._data.append(s.row_values(col))
        return self._data

if __name__ == '__main__':
    y = r'D:\huilan\config\config.yml'
    reader_yml = YamlReader(y)
    print(reader_yml.data)

    e = r'D:\huilan\data\baidu.xlsx'
    reader_excel = ExcelReader(e)
    print(reader_excel.data)

