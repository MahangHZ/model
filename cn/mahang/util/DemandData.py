# _*_ coding: utf-8 _*_
import xlrd


class DemandData:
    E_sheetnrows = 0
    E_sheetncols = 0
    H_sheetnrows = 0
    H_sheetncols = 0
    C_sheetnrows = 0
    C_sheetncols = 0
    E = {}
    H = {}
    C = {}

    def __init__(self):
        pass

    @staticmethod
    def init():
        e_demand = xlrd.open_workbook(r'../../resources/Ele.xlsx')
        h_demand = xlrd.open_workbook(r'../../resources/Heat.xlsx')
        c_demand = xlrd.open_workbook(r'../../resources/Cold.xlsx')
        e_sheet = e_demand.sheet_by_name('Sheet1')
        h_sheet = h_demand.sheet_by_name('Sheet1')
        c_sheet = c_demand.sheet_by_name('Sheet1')
        DemandData.E_sheetnrows = e_sheet.nrows
        DemandData.E_sheetncols = e_sheet.ncols
        DemandData.H_sheetnrows = h_sheet.nrows
        DemandData.H_sheetncols = h_sheet.ncols
        DemandData.C_sheetnrows = c_sheet.nrows
        DemandData.C_sheetncols = c_sheet.ncols
        for i in range(0, DemandData.E_sheetnrows - 1, 1):  # e_sheetnrows = h_sheetnrows = c_sheetnrows
            DemandData.E[i] = e_sheet.cell(i + 1, DemandData.E_sheetncols - 1).value  # 单位KWh
            DemandData.H[i] = h_sheet.cell(i + 1, DemandData.H_sheetncols - 1).value
            DemandData.C[i] = c_sheet.cell(i + 1, DemandData.C_sheetncols - 1).value  # i 为0 - (n_rows-2), 共 n_rows-1 个值

