import tkinter as tk
from tkinter import ttk
import tkcalendar
import datetime as dt

class CashFlow:

    def __init__(self):
        #Initialize Tk
        self.root = tk.Tk()
        #Build the Calendar
        self.buildCal()
        ttk.Button(self.root, text='Calendar').pack(padx=75, pady=75)
        self.root.mainloop()

    def add_expense(self):
        #Set Expense color
        self.cal.tooltip_wrapper.configure(foreground='red')
        #Create Variable for selected date
        self.temp_sel = self.cal.selection_get()       
        #Create event on the selected date and save the event id
        self.curr_id = self.cal.calevent_create(date=self.temp_sel, text=600, tags=["Expense"])
        #self.cal.calevent_create(date=self.temp_sel, text=600, tags="Expense")
        #Variable for date's IDs
        self.date_id = self.cal.get_calevents(date=self.temp_sel, tag='Expense')
        #Variable to look into the Event's keys
        self.shortcut = self.cal.tooltip_wrapper
        self.shortbut = list(self.shortcut.widgets.keys())[0]
        #ttk.Button(self.top, text=self.cal.calevent_cget(ev_id=self.curr_id, option='tag')).pack_configure(expand=False, in_=self.shortbut)
        self.cal.tooltip_wrapper.configure()
        self.top.wm_deiconify()
        """if self.reset_num <= 1:
            self.reset_num += 1
            self.top.wm_state('zoomed')
            self.top.wm_state('normal')"""
        #self.cal.see(self.cal.selection_get())
        #self.expense_button.update_idletasks()

    def add_income(self):
        print(self.cal.tooltip_wrapper.widgets)
        #Create Variable for selected date
        self.temp_sel = self.cal.selection_get()       
        #Create event on the selected date and save the event id
        self.curr_id = self.cal.calevent_create(date=self.temp_sel, text=600, tags=["Income"])
        #self.cal.calevent_create(date=self.temp_sel, text=600, tags="Expense")
        #Set Income color
        #self.cal.tooltip_wrapper.configure(widget=list(self.cal.tooltip_wrapper.widgets.values())[0], foreground='green')
        print(self.cal.tooltip_wrapper.configure())
        #Variable for date's IDs
        self.date_id = self.cal.get_calevents(date=self.temp_sel, tag='Income')
        #Variable to look into the Event's keys
        self.shortcut = self.cal.tooltip_wrapper
        self.shortbut = list(self.shortcut.widgets.keys())[0]
        #ttk.Button(self.top, text=self.cal.calevent_cget(ev_id=self.curr_id, option='tag')).pack_configure(expand=False, in_=self.shortbut)
        self.top.wm_deiconify()
        #self.cal.see(self.cal.selection_get())
        #self.expense_button.update_idletasks()
        

    def buildCal(self):
        self.top = tk.Toplevel(self.root)
        self.today = dt.date.today()

        mindate = self.today.replace(day=1, month=1)
        maxdate = self.today + dt.timedelta(days=730)

        self.cal = tkcalendar.Calendar(self.top, font="Arial 14", selectmode='day', locale='en_US',
                state='normal', mindate=mindate, maxdate=maxdate, disabledforeground='red', firstweekday='sunday',
                cursor="hand1", year=self.today.year, month=self.today.month, day=self.today.day, tooltipalpha=1,
                tooltipbackground='white', tooltipdelay=0)

        self.cal.pack(fill="both", expand=True)
        self.top.wm_state('normal')
        self.expense_button = ttk.Button(self.top, text="Expense", command=self.add_expense)
        self.income_button = ttk.Button(self.top, text="Income", command=self.add_income)

        self.expense_button.pack_configure(expand=True, fill="both", side="right")
        self.income_button.pack_configure(expand=True, fill="both", side="left")

        

    def userExpenses(self):
        pass

    def userIncome(self):
        pass

    def updateCal(self):
        pass

def main():

    CashFlow()


if __name__ == '__main__':
    main()