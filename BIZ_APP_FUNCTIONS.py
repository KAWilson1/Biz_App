#Author: Kyle Wilson, Austin Wilson
#Init: 1/13/18
#Last Updated: 1/15/18
#Purpose: Define functions for BIZ_APP

from BIZ_APP_STRUCTS import *
import xlsxwriter
import xlrd
from datetime import date
import random
import tkinter as tk
from tkinter.messagebox import showinfo
from tkinter import ttk



def read_items(sheet):
    #list of items from xlsx sheet
    toReturn = []
    
    for row in range(1, sheet.nrows):
        tempItem = Item(sheet.cell_value(row, 0),
                        sheet.cell_value(row, 1),
                        sheet.cell_value(row, 2),
                        sheet.cell_value(row, 3))
        toReturn.append(tempItem)
    return toReturn

def get_total(itemList, currOrder):
    total = 0
    for currItem in currOrder.cart:
        for item in itemList:
            if item.get_ID() == currItem.get_ID():
                total += float(currItem.get_cost())
                if item.get_taxable() == "Y":
                    total += float(currItem.get_cost()) * 0.07
    return round(total, 2)

def excelify_date(currDate):
    if type(currDate) != datetime.date:
        raise Exception("Requires a datetime.date argument, received: " + str(type(currDate)))

    currDate = date(currDate.year, currDate.month, currDate.day)
    excelDate = date(1900, 1, 1)

    delta = currDate - excelDate
    toReturn = delta.days
    toReturn += 2 #excel's calculations are different than datetime's

    return float(toReturn)

#Author: AW
def show_analytics(queue, itemList):
    total = 0

    for order in queue:
        for item in order.cart:
            total += item.get_cost()
            
    IDList = []
    allItemOccurances = []
    
    for order in queue:
        for item in order.cart:
            IDList.append(int(item.get_ID()))
    for item in itemList:
        allItemOccurances.append(0)
    for ID in IDList:
        allItemOccurances[ID-1] += 1

    lowest = 999
    highest = 0
    for num in allItemOccurances:
        if num > highest:
            highest = num
        if num < lowest:
            lowest = num

    lowItems = []
    highItems = []
    for i in range(0, len(allItemOccurances)):
        if allItemOccurances[i] == highest:
            highItems.append(itemList[i].get_name())
        if allItemOccurances[i] == lowest:
            lowItems.append(itemList[i].get_name())

    showinfo("Analytics Manager", "Total Revenue: " + str(round(total,2)) +
             "\nMost Bought Item(s): " + ', '.join(highItems) +
             "\nLeast Bought Item(s): " + ', '.join(lowItems))
            
        


#GUI buttons
def clear_order(textbox, totalLabel, currOrder):
    print(type(textbox))
    print(type(totalLabel))
    currOrder.cart = []
    currOrder.orderID += 1
    currOrder.myDate = datetime.datetime.now().date()
    
    textbox.delete(1.0, 'end')
    totalLabel['text'] = "Total: $0.00"

def pay(textbox, label, currOrder, queue):
    tempOrder = Order(currOrder.get_ID(), currOrder.get_cart(), currOrder.get_date())
    queue.append(tempOrder)
    clear_order(textbox, label, currOrder)

def export_queue(queue):
    currDate = datetime.datetime.now().date()

    #copy old worksheets into new book
    outputWb = xlsxwriter.Workbook("Sales_Report_" + str(currDate.month) + "_" + str(currDate.day) + ".xlsx")
    outputWs = outputWb.add_worksheet("Sales")

    #define date format
    f_date = outputWb.add_format()
    f_date.set_num_format('m/d/yy')

    #write headers
    outputWs.write("A1", "Order ID")
    outputWs.write("B1", "Item IDs")
    outputWs.write("C1", "Date")

    for i in range(0, len(queue)):
        #format IDs
        idString = ""
        for item in queue[i].cart:
            idString += str(int(item.get_ID())) + ","
            
        outputWs.write(i+1, 0, str(queue[i].get_ID()))     
        outputWs.write(i+1, 1, idString[:-1])
        outputWs.write(i+1, 2, excelify_date(queue[i].get_date()), f_date)

    try:
        outputWb.close()
        showinfo("Export Manager", "Export successful!")
    except PermissionError:
        showinfo("Export Manager", "Export failed. Please close the current Sales Report and re-try.")
def simulate_order(textbox, totalLabel, itemList, currOrder):
    #get 1-4 items to simulate
    numItems = random.randint(1,4)

    #get a list of random items
    for i in range(numItems):
        currIdx = random.randint(0, len(itemList)-1)
        if itemList[currIdx].get_taxable() == "Y":
            textbox.insert('end', itemList[currIdx].get_name() + ": $" + str(round(float(itemList[currIdx].get_cost()) * 1.07, 2)) + "\n")
        else:
            textbox.insert('end', itemList[currIdx].get_name() + ": $" + str(itemList[currIdx].get_cost()) + "\n")
        currOrder.add_item(itemList[currIdx])

    totalLabel['text'] = "Total: $" + str(get_total(itemList, currOrder))

FONT = ("Verdana", 12)

#start of GUI section
class MainWindow(tk.Tk):

    def __init__(self, *args):
        tk.Tk.__init__(self)
        window = tk.Frame(self)
        tk.Tk.wm_title(self, "Biz App")

        
        window.pack(side="top", fill="both", expand=True)
        window.grid_rowconfigure(0, weight=1)
        window.grid_columnconfigure(0, weight=1)

        self.frames = {}

        frame = StartPage(window, self, *args)
        self.frames[StartPage] = frame
        frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, controller):
        frame = self.frames[controller]
        frame.tkraise()


class StartPage(tk.Frame):

    def __init__(self, parent, controller, itemList, currentOrder, queue):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Start Page", font=FONT)
        label.pack(pady=10, padx=10)

        button1 = ttk.Button(self, text="Clear Order", command=lambda: clear_order(textBox, totalLabel, currentOrder))
        button1.pack(side="left")

        button2 = ttk.Button(self, text="Pay", command=lambda: pay(textBox, totalLabel, currentOrder, queue))
        button2.pack(side="left")

        button3 = ttk.Button(self, text="Export Orders", command=lambda: export_queue(queue))
        button3.pack(side="left")

        button4 = ttk.Button(self, text="Print Report", command=lambda: show_analytics(queue, itemList))
        button4.pack(side="left")

        button5 = ttk.Button(self, text="Simulate Order", command=lambda: simulate_order(textBox, totalLabel, itemList, currentOrder))
        button5.pack(side="left")

        textBox = tk.Text()
        textBox.pack()

        totalLabel = tk.Label(self, text="Total: $0.00", font=FONT)
        totalLabel.pack()
