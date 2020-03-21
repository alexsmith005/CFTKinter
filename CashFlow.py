class CashFlow:

    def __init__(self):
        import tkinter as tk
        from tkinter import ttk
        import tkcalendar

        #Initialize Tk
        self.root = tk.Tk()
        #Build the Calendar
        self.buildCal()
        ttk.Button(self.root, text='Calendar').pack(padx=75, pady=75)

        self.root.mainloop()

    def print_sel(self):
        import datetime as dt
        self.temp_sel = self.cal.selection_get()       
        #if self.cal.calevents == None:
            #self.cal.calevent_create(date=self.cal.selection_get(), text='Expense', tags=600)
        if self.cal.get_calevents(date=self.temp_sel) == None:
            self.cal.calevent_create(date=self.temp_sel, text='Expense', tags=600)
        self.cal.calevent_create(date=self.temp_sel, text=600, tags="Expense")
        print(self.cal.get_calevents(date=self.temp_sel, tag='Expense'))
        print(self.cal.calevent_cget(ev_id=0, option='text'))
        self.cal.see(self.cal.selection_get())

    def buildCal(self):
        import tkinter as tk
        from tkinter import ttk
        import datetime as dt

        import tkcalendar

        self.top = tk.Toplevel(self.root)
        self.today = dt.date.today()

        mindate = self.today.replace(day=1, month=1)
        maxdate = self.today + dt.timedelta(days=730)

        self.cal = tkcalendar.Calendar(self.top, font="Arial 14", selectmode='day', locale='en_US',
                   mindate=mindate, maxdate=maxdate, disabledforeground='red', firstweekday='sunday',
                   cursor="hand2", year=self.today.year, month=self.today.month, day=self.today.day)

        self.cal.pack(fill="both", expand=True)
        ttk.Button(self.top, text="ok", command=self.print_sel).pack()
        

    def userExpenses(self):
        pass

    def userIncome(self):
        pass

    def updateCal(self):
        pass

def main():

    get_cal = CashFlow()


if __name__ == '__main__':
    main()