import tkinter as tk
import tkinter.simpledialog as dialog
import tkinter.scrolledtext as st
import tkinter.messagebox as messagebox
#from tkinter.ttk import *
import time
import re

__all__ = (
    "getNewData",
    "showDatas",
    "showTotal"
)

LABEL_WIDTH = 10
ENTRY_WIDTH = 10

#UTILS
def checkDate(date: str):
    """Check wether a date is valid or not
    """
    pattern = r"^[0-9]{2}/[0-9]{2}/[0-9]{4}$"
    return re.match(pattern, date) is not None

#DATA WINDOW
class DataWindow(dialog.Dialog):
    """Derived class from Dialog. Create a dialog window to add new driving datas.
    """

    def body(self, master):
        #DATE
        label = tk.Label(master, text = "Date : ", width = LABEL_WIDTH)
        label.grid(column = 0, row = 0)
        self.date_entry = tk.Entry(master, width = ENTRY_WIDTH)
        self.date_entry.grid(column = 1, row = 0)
        #KILOMETRES
        #agglo
        label = tk.Label(master, text = "Agglo : ", width = LABEL_WIDTH)
        label.grid(column = 0, row = 1)
        self.agglo_entry = tk.Entry(master, width = ENTRY_WIDTH)
        self.agglo_entry.grid(column = 1, row = 1)
        #h-agglo
        label = tk.Label(master, text = "H-Agglo : ", width = LABEL_WIDTH)
        label.grid(column = 0, row = 2)
        self.h_agglo_entry = tk.Entry(master, width = ENTRY_WIDTH)
        self.h_agglo_entry.grid(column = 1, row = 2)
        #auto
        label = tk.Label(master, text = "Auto : ", width = LABEL_WIDTH)
        label.grid(column = 0, row = 3)
        self.auto_entry = tk.Entry(master, width = ENTRY_WIDTH)
        self.auto_entry.grid(column = 1, row = 3)
        #remarques
        self.remarques_entry = st.ScrolledText(master, width = LABEL_WIDTH + ENTRY_WIDTH, height = 6)
        self.remarques_entry.grid(column = 0, row = 4, columnspan = 2, pady = 10)

    def checkDatas(self, date, agglo, h_agglo, auto):
        if not checkDate(date):
            raise ValueError("Invalid date format. Must be XX/XX/XX")
        a, b, c = int(agglo), int(h_agglo), int(auto)

    def validate(self):
        try:
            #GET DATAS
            date = self.date_entry.get()
            agglo = self.agglo_entry.get()
            h_agglo = self.h_agglo_entry.get()
            auto = self.auto_entry.get()
            remarques = self.remarques_entry.get("0.0", tk.END)
            #CHECK DATAS
            self.checkDatas(date, agglo, h_agglo, auto)
            #IF ALL WENT GOOD
            self.result = tuple([date, tuple([agglo, h_agglo, auto]), remarques])
            return True
        except:
            messagebox.showerror("Error", "Please fill in all text areas.\nDate format must be XX/XX/XXXX")
            return False

    def apply(self):
        pass

#SHOW DATAS
class ShowDatas(tk.Toplevel):

    def __init__(self, master, infos):
        super().__init__()
        self.master = master
        self.datas = infos
        self.title("Infos")
        self.result = False
        self.body()

    def body(self):
        #frame
        self.main_frame = tk.Frame(self)
        self.main_frame.grid(column = 0, row = 0, columnspan = 2)
        self.save_button = tk.Button(self, text = "Save", command = self.save)
        self.save_button.grid(column = 0, row = 1, sticky = "nswe")
        self.cancel_button = tk.Button(self, text = "Cancel", command = self.quit)
        self.cancel_button.grid(column = 1, row = 1, sticky = "nswe")
        #add body
        DataWindow.body(self, self.main_frame)
        #DATE
        self.date_entry.insert(0, self.datas[0])
        #KILOMETERS
        self.agglo_entry.insert(0, str(self.datas[1][0]))
        self.h_agglo_entry.insert(0, str(self.datas[1][1]))
        self.auto_entry.insert(0, str(self.datas[1][2]))
        #OTHERS
        self.remarques_entry.insert("0.0", self.datas[-1])

    def checkDatas(self, date, agglo, h_agglo, auto):
        DataWindow.checkDatas(self, date, agglo, h_agglo, auto)

    def quit(self):
        self.result = False
        self.destroy()

    def save(self):
        if not DataWindow.validate(self):
            return
        else:
            self.destroy()

#SHOW TOTAL
class ShowTotal(tk.Toplevel):

    def __init__(self, master, text):
        super().__init__()
        self.master = master
        self.text = text
        self.title("Infos")
        self.label = Label(self, text = text, font = "Arial 10 bold")
        self.label.grid()

#GET NEW DATAS
def getNewData(master):
    """Function to make easier the use of DataWindow. Return directly the result, like a function.
    """
    w = DataWindow(master)
    return w.result

#SHOW DATAS
def showDatas(master, datas):
    """Function to make easier the use of ShowData.
    """
    w = ShowDatas(master, datas)
    w.grab_set()
    master.wait_window(w)
    master.grab_set()
    #print(w.result)
    return w.result

#SHOW TOTAL
def showTotal(master, text):
    w = ShowTotal(master, text)
    master.wait_window(w)
    return True

if __name__ == "__main__":
    fen = tk.Tk()
    print(getNewData(fen))
    
