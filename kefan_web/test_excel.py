#!/usr/bin/python

# -*- codding: cp936 -*-

 

import xlsxwriter

 

book = xlsxwriter.Workbook('pict.xlsx')

sheet = book.add_worksheet('demo')
format = book.add_format()
#sheet.set_row(0, 18, format)
sheet.set_row(0, 50)
sheet.set_column('A:A', 10)
#heet.set_column('A:A', 30)
sheet.set_row(1, 50)
sheet.insert_image('A1','1.jpg')
sheet.insert_image('A2','1.jpg')
book.close()
