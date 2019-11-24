import popup_window as popup
from tkinter.scrolledtext import ScrolledText
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as messagebox
import os
import sys

#CONSTANTS
if not os.path.exists("datas"):
    os.mkdir("datas")
DIRECTORY = "datas"
OS = sys.platform

#months
MONTHS = (
    "Janvier",
    "Fevrier",
    "Mars",
    "Avril",
    "Mai",
    "Juin",
    "Juillet",
    "Aout",
    "Septembre",
    "Octobre",
    "Novembre",
    "Decembre"
)

#CLASSES
class Main(tk.Tk):

    def __init__(self):
        #init
        super().__init__()
        self.initUI()
        self.title("Conduite")
        #path
        self.path = ""
        self.to_show = list()
        self.menubar = list()
        #load datas
        self.cd("")
        #total
        self.calcTotal()

    def open(self, path):
        if OS != "linux":
            year, month, day = path.split("\\")
        else:
            year, month, day = path.split("/")
        datas = self.readData(year, month, day)
        res = popup.showDatas(self, datas)
        if not res:
            return
        else:
            answer = messagebox.askyesno("Save", "Erase previous datas ?")
            if not answer:
                return
            self.saveDatas(day, month, year, res)
            

    def readData(self, year, month, day):
        #read the whole file...
        with open(os.path.join(DIRECTORY, year, month, day), "r") as doc:
            datas = doc.read().split("\n")
        #... then split into the specific parts
        agglo, hagglo, auto = datas[0].split(",")
        remarques = "\n".join(datas[1:])
        #other steps
        month_nb = MONTHS.index(month) + 1
        month_nb = "0" + str(month_nb) if month_nb < 10 else str(month_nb)
        #print the all
        return (f"{day}/{month_nb}/{year}", (int(agglo), int(hagglo), int(auto)), remarques)

    def cd(self, path):
        """Change working directory.
        """
        #change directory
        self.path = path
        #update menubar
        for obj in self.menubar:
            obj.grid_forget()
            obj.destroy()
            del obj
        self.menubar = [tk.Button(self.nav_bar, text = "ROOT", bg = "white",
                                      command = (lambda : self.cd("")))]
        current = list()
        if OS != "linux":
            names = self.path.split("\\")
        else:
            names = self.path.split("/")
        for name in names:
            if name == "":
                continue
            current.append(name)
            self.menubar.append(tk.Button(self.nav_bar, text = name, bg = "white",
                                      command = (lambda c = list(current): self.cd(os.path.join(*c)))))
        #load datas
        self.loadDatas(path = self.path)
        #update ui
        self.updateUI()
        #update total
        self.calcTotalMonth()

    def loadDatas(self, path = ""):
        #i chose a tree architecture
        paths = os.listdir(os.path.join(DIRECTORY, path))
        try:
            paths = sorted(paths, key = lambda elem: MONTHS.index(elem))
        except:
            pass
        for obj in self.to_show:
            obj.destroy()
        #update data list
        self.to_show = list()
        for p in paths:
            if os.path.isdir(os.path.join(DIRECTORY, path, p)):
                #if directory
                self.to_show.append(tk.Button(self.datas_entry, text = p, font = "Arial 12 bold", bg = "#0fa", width = 20, command = (lambda y = p: self.cd(os.path.join(path, y))),))
            else:
                #if file
                 self.to_show.append(tk.Button(self.datas_entry, text = p, font = "Arial 12 bold", bg = "#0af", width = 20, command = (lambda y = p: self.open(os.path.join(path, y)))))

    def initUI(self):
        #two main parts
        self.datas_container = tk.LabelFrame(self, text = "Datas", font = "Arial 12 bold", fg = "blue")
        self.datas_container.grid(column = 0, row = 0, sticky = "nswe")
        self.infos_container = tk.LabelFrame(self, text = "Infos", font = "Arial 12 bold", fg = "blue")
        self.infos_container.grid(column = 1, row = 0, sticky = "nswe")
        #DATAS
        self.nav_bar = tk.Frame(self.datas_container)
        self.nav_bar.grid(column = 0, row = 0, sticky = "nswe")
        self.datas_entry = ScrolledText(self.datas_container, width = 40)
        self.datas_entry.grid(column = 0, row = 1)
        self.add_datas = tk.Button(self.datas_container, text = "ADD", command = self.addData)
        self.add_datas.grid(column = 0, row = 2, sticky = "we")
        #INFOS
        self.total_button = tk.Button(self.infos_container, text = "TOTAL", width = 30, command = self.calcTotal)
        self.total_button.grid(column = 0, row = 0)
        self.la_total = tk.Label(self.infos_container, text = "")
        self.la_total.grid(column = 0, row = 1)
        self.total_month_button = tk.Button(self.infos_container, text = "TOTAL (this month)", width = 30, command = self.calcTotalMonth)
        self.total_month_button.grid(column = 0, row = 2)
        self.la_total_month = tk.Label(self.infos_container, text = "")
        self.la_total_month.grid(column = 0, row = 3)

    def calcTotal(self):
        total = int(0)
        years = os.listdir(DIRECTORY)
        for year in years:
            months = os.listdir(os.path.join(DIRECTORY, year))
            for month in months:
                days = os.listdir(os.path.join(DIRECTORY, year, month))
                for day in days:
                    datas = self.readData(year, month, day)
                    total += sum(datas[1])
        #show total in a window
        self.la_total.configure(text = f"En tout, tu as roulé : {str(total)}km")

    def calcTotalMonth(self):
        total = int(0)
        try:
            if OS != "linux":
                year, month = self.path.split("\\")
            else:
                year, month = self.path.split("/")
        except:
            return
        path = os.path.join(DIRECTORY, self.path)
        for day in os.listdir(path):
            if os.path.isdir(os.path.join(path, day)):
                continue
            datas = self.readData(year, month, day)
            total += sum(datas[1])
        #show total in a window
        self.la_total_month.configure(text = f"{month} {year}, tu as roulé : {str(total)}km")

    def updateUI(self):
        #update nav bar
        for i, obj in enumerate(self.menubar):
            obj.grid(column = i, row = 0)
            obj.configure(width = 10)
        #update datas entry
        self.datas_entry.delete("0.0", tk.END)
        for elem in self.to_show:
            self.datas_entry.window_create(tk.INSERT, window = elem)
            self.datas_entry.insert(tk.INSERT, "\n")

    def addData(self):
        datas = popup.getNewData(self)
        if not datas:
            return
        date = datas[0]
        day, month, year = date.split("/")
        month = MONTHS[int(month) - 1]
        self.saveDatas(day, month, year, datas)
        #update ui
        self.updateUI()
        #total
        self.calcTotal()

    def saveDatas(self, day, month, year, datas):
        #create new file
        if not os.path.exists(os.path.join(DIRECTORY, year)):
            os.mkdir(os.path.join(DIRECTORY, year))
        if not os.path.exists(os.path.join(DIRECTORY, year, month)):
            os.mkdir(os.path.join(DIRECTORY, year, month))
        #write to file
        remarques = datas[2]
        if datas[2].endswith("\n"):
            remarques = datas[2][:-1]
        with open(os.path.join(DIRECTORY, year, month, day), "w") as doc:
            to_write = str(",".join(list(map(str, datas[1]))) + "\n" + remarques)
            doc.write(to_write)
                

if __name__ == "__main__":
    m = Main()
    m.mainloop()
