# coding=utf-8
import datetime
import xlwt

book = xlwt.Workbook(encoding='utf-8')
sheet = book.add_sheet('sheet_test', cell_overwrite_ok=True)

sheet.write(0, 0, 'Python')
sheet.row(0).write(1, 'is')
sheet.write(0, 2, 'very very useful.')
sheet.col(2).width = 4000

font = xlwt.Font()
font.name = 'Arial'
font.height = 240  # font size: 12pt

pattern = xlwt.Pattern()
pattern.pattern = xlwt.Pattern.SOLID_PATTERN
pattern.pattern_fore_colour = 0x0A

style = xlwt.XFStyle()
style.num_format_str = '0.00%'
style.font = font
style.pattern = pattern

a = 8
b = 10
# 以百分比的形式显示，保留两位小数

sheet.write(0, 3, float(a) / b, style)

# 显示日期

sheet.row(0).write(4, datetime.date(2016, 8, 14), xlwt.easyxf(
    'font: name Arial, height 240;'
    'pattern: pattern squares, fore_color red;',
    num_format_str='YYYY-MM-DD'
)
                   )

book.save('test.xls')
