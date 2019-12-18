# _*_ coding: utf-8 _*_
import xlrd


class ICEDatabase:
    def __init__(self):
        ice_database = xlrd.open_workbook(r'E:/pythonProject/model/resources/ICE_database.xlsx')
        ice_sheet = ice_database.sheet_by_name('database')
        self.ice_database_rows = ice_sheet.nrows
        self.ice_database_cols = ice_sheet.ncols
        self.ice_database = []
        for i in range(1, self.ice_database_rows):
            ice_database_one = []
            for j in range(1, self.ice_database_cols):
                ice_database_one.append(ice_sheet.cell(i, j).value)
            self.ice_database.append(ice_database_one)

