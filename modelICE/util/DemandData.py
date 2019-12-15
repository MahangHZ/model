# _*_ coding: utf-8 _*_
import xlrd
from cn.modelICE.Parameters import Parameters


class DemandData:
    def __init__(self):
        e_demand = xlrd.open_workbook(r'E:/pythonProject/model/resources/Ele.xlsx')
        h_demand = xlrd.open_workbook(r'E:/pythonProject/model/resources/Heat.xlsx')
        c_demand = xlrd.open_workbook(r'E:/pythonProject/model/resources/Cold.xlsx')
        e_sheet = e_demand.sheet_by_name('Sheet1')
        h_sheet = h_demand.sheet_by_name('Sheet1')
        c_sheet = c_demand.sheet_by_name('Sheet1')
        self.E_sheetnrows = e_sheet.nrows  # 行
        self.E_sheetncols = e_sheet.ncols  # 列
        self.H_sheetnrows = h_sheet.nrows
        self.H_sheetncols = h_sheet.ncols
        self.C_sheetnrows = c_sheet.nrows
        self.C_sheetncols = c_sheet.ncols
        self.E = []
        self.H_steam = []
        self.H_space = []
        self.H_water = []
        self.H = []
        self.C = []
        for i in range(0, self.E_sheetnrows - 1, 1):  # e_sheetnrows = h_sheetnrows = c_sheetnrows
            self.E.append(e_sheet.cell(i + 1, self.E_sheetncols - 1).value / Parameters.delttime)
            self.H_steam.append(h_sheet.cell(i + 1, 2).value / Parameters.delttime)
            self.H_space.append(h_sheet.cell(i + 1, 3).value / Parameters.delttime / Parameters.effi_FanCoil)
            self.H_water.append(h_sheet.cell(i + 1, 4).value / Parameters.delttime)
            self.H.append(self.H_space[i] + self.H_water[i])
            self.C.append(c_sheet.cell(i + 1, self.C_sheetncols - 1).value
                          / Parameters.delttime / Parameters.effi_FanCoil)
        self.sum_E = sum(self.E)
        self.sum_H_steam = sum(self.H_steam)
        self.sum_H_space = sum(self.H_space)
        self.sum_H_water = sum(self.H_water)
        self.sum_C = sum(self.C)
        length = len(self.E)
        self.average_E = self.sum_E / length
        self.average_H_steam = self.sum_H_steam / length
        self.average_H_space = self.sum_H_space / length
        self.average_H_water = self.sum_H_water / length
        self.average_C = self.sum_C / length


# 该部分ok
