# coding=utf-8
import xlrd

wb = xlrd.open_workbook('test.xls')

# 打印每张表的最后一列
# 方法1
for s in wb.sheets():
    print "== The last column of sheet '%s' ==" % (s.name)
    for i in range(s.nrows):
        print s.row(i)[-1].value

# 方法2
for i in range(wb.nsheets):
    s = wb.sheet_by_index(i)
    print "== The last column of sheet '%s' ==" % (s.name)
    for v in s.col_values(s.ncols - 1):
        print v

# 方法3
for name in wb.sheet_names():
    print "== The last column of sheet '%s' ==" % (name)
    s = wb.sheet_by_name(name)
    c = s.ncols - 1
    for r in range(s.nrows):
        print s.cell_value(r, c)