# _*_ coding: utf-8 _*_
import xlrd


class DemandData:
    def __init__(self):
        e_demand = xlrd.open_workbook(r'E:/pythonProject/model/resources/Ele.xlsx')
        h_demand = xlrd.open_workbook(r'E:/pythonProject/model/resources/Heat.xlsx')
        c_demand = xlrd.open_workbook(r'E:/pythonProject/model/resources/Cold.xlsx')
        e_sheet = e_demand.sheet_by_name('Sheet1')
        h_sheet = h_demand.sheet_by_name('Sheet1')
        c_sheet = c_demand.sheet_by_name('Sheet1')
        self.E_sheetnrows = e_sheet.nrows
        self.E_sheetncols = e_sheet.ncols
        self.H_sheetnrows = h_sheet.nrows
        self.H_sheetncols = h_sheet.ncols
        self.C_sheetnrows = c_sheet.nrows
        self.C_sheetncols = c_sheet.ncols
        self.E = []
        self.H = []
        self.C = []
        for i in range(0, self.E_sheetnrows - 1, 1):  # e_sheetnrows = h_sheetnrows = c_sheetnrows
            self.E.append(e_sheet.cell(i + 1, self.E_sheetncols - 1).value)
            self.H.append(h_sheet.cell(i + 1, self.H_sheetncols - 1).value)
            self.C.append(c_sheet.cell(i + 1, self.C_sheetncols - 1).value)


