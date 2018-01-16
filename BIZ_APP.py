from BIZ_APP_FUNCTIONS import *
from BIZ_APP_STRUCTS import *
import xlrd
from datetime import date

path = "ItemData.xlsx"
workbook = xlrd.open_workbook(path)
itemsWorksheet = workbook.sheet_by_index(0)


masterItemList = read_items(itemsWorksheet)
currOrder = Order(1, [], datetime.datetime.now().date())
orderQueue = []

app = MainWindow(masterItemList, currOrder, orderQueue)
app.mainloop()
