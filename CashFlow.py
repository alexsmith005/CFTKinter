import tkinter as tk
from tkinter import ttk
import tkcalendar
import datetime as dt
import psycopg2
import calendar

class CashFlow:

    def __init__(self):
        self.start_money = 1000
        self.updates_list = []
        self.todays_money = []
        #Initialize SQL connection
        self.initiateSQL()
        #Get current cash dates
        self.cash_dates = self.getData("cashflow")
        self.income_dates = self.getData("income", "income_dates")
        self.expense_dates = self.getData("expense", "expense_dates")
        self.userIncome()
        #Initialize Tk
        self.root = tk.Tk()
        #Build the Calendar
        self.buildCal()
        ttk.Button(self.root, text='Calendar').pack(padx=75, pady=75)
        #Run the GUI until it's closed
        self.root.mainloop()
        #Close out of SQL DB
        self.cursor.close()
        if self.conn is not None:
            self.conn.close()

    def add_expense(self):
        #Create Variable for selected date
        self.temp_sel = self.cal.selection_get()
        print(self.temp_sel)
        #Create event on the selected date and save the event id
        self.events_id = self.cal.calevent_create(date=self.temp_sel, text=600, tags=["Expense"])
        self.updates_list.append(self.events_id)
        #Variable for date's IDs
        self.date_id = self.cal.get_calevents(date=self.temp_sel, tag='Expense')
        #variable for amount changed
        self.amount = self.cal.calevent_cget(ev_id=self.events_id, option='text')
        #Variable to look into the Event's keys
        self.shortcut = self.cal.tooltip_wrapper
        self.shortbut = list(self.shortcut.widgets.keys())[-1]
        #Create a Button representing Expense added
        self.expense_added = tk.Button(self.top, text=self.cal.calevent_cget(ev_id=self.events_id, option='text'), fg='red')
        self.expense_added.pack_configure(expand=False, fill='x', in_=self.shortbut, side='bottom')
        self.cursor.execute("""INSERT INTO expense(expense_dates, expense)
             VALUES(%s, %s) RETURNING expense_id;""", (self.temp_sel, self.amount))
        self.expense_id = self.cursor.fetchone()[0]
        print(self.expense_id)
        self.conn.commit()
        
#Think about heirarchy for tables. Do I need a master table that holds the user ID that dives into the separate table IDs?
#Look into SQL setup overall to answer this question and how other databases are set up. (professional examples)

    def add_income(self):
        #Create Variable for selected date
        self.temp_sel = self.cal.selection_get()
        #Create event on the selected date
        self.events_id = self.cal.calevent_create(date=self.temp_sel, text=600, tags=["Income", self.temp_sel])
        self.updates_list.append(self.events_id)
        #Variable for date's IDs
        self.date_id = self.cal.get_calevents(date=self.temp_sel, tag='Income')
        #Variable for amount changed
        self.amount = self.cal.calevent_cget(ev_id=self.events_id, option='text')
        #Variable to look into the Event's keys
        self.shortcut = self.cal.tooltip_wrapper
        self.shortbut = list(self.shortcut.widgets.keys())[-1]
        #Create a Button representing Income added on each month
        self.income_added = tk.Button(self.top, text=self.cal.calevent_cget(ev_id=self.events_id, option='text'), fg='green')
        self.income_added.pack_configure(expand=False, fill='x', in_=self.shortbut, side='bottom')
        self.cursor.execute("""INSERT INTO income(income_dates, income)
             VALUES(%s, %s) RETURNING income_id;""", (self.temp_sel, self.amount))
        self.income_id = self.cursor.fetchone()[0]
        print(self.income_id)
        self.conn.commit()

    def _left_month_command(self):
        self.cal._prev_month()
        self.updateCal()

    def _right_month_command(self):
        self.cal._next_month()
        self.updateCal()

    def _left_year_command(self):
        self.cal._prev_year()
        self.updateCal()

    def _right_year_command(self):
        self.cal._next_year()
        self.updateCal()

    def buildCal(self):
        self.top = tk.Toplevel(self.root)
        self.today = dt.date.today()

        mindate = self.today.replace(day=1, month=1)
        maxdate = self.today + dt.timedelta(days=730)

        self.cal = tkcalendar.Calendar(self.top, font="Arial 14", selectmode='day', locale='en_US',
                state='normal', mindate=mindate, maxdate=maxdate, disabledforeground='red', firstweekday='sunday',
                cursor="hand1", year=self.today.year, month=self.today.month, day=self.today.day, tooltipalpha=1,
                tooltipbackground='white', tooltipdelay=0)
        #self.top.wm_state('zoomed')
        self.cal.pack(fill='both', expand=True)
        self.enter_amt = ttk.Entry(self.top)
        self.expense_button = ttk.Button(self.top, text="Expense", command=self.add_expense)
        self.income_button = ttk.Button(self.top, text="Income", command=self.add_income)
        self.calculate_button = ttk.Button(self.top, text="Calculate", command=self.monthFlow)
        #if self.enter_amt != 0:
        #    self.start_money_button = ttk.Button(self.top, text="Set Start Money", command=self.setStartMoney(self.enter_amt))

        self.expense_button.pack_configure(expand=True, fill='both', side="right")
        self.income_button.pack_configure(expand=True, fill='both', side="left")
        self.calculate_button.pack_configure(fill='both', side='top')
        #self.start_money_button.pack_configure(fill='both', side='bottom')
        self.enter_amt.pack_configure(fill='both', side='bottom')

        #Reconfigure month and year buttons to change the calendar and change the displayed events to match
        self.cal._l_month.configure(command=self._left_month_command)
        self.cal._r_month.configure(command=self._right_month_command)
        self.cal._l_year.configure(command=self._left_year_command)
        self.cal._r_year.configure(command=self._right_year_command)
        print(self.cash_dates)

    def monthFlow(self):
        #Save the days corresponding to the current month as variables
        first_day = self.cal._date.replace(day=1)
        _last_day = calendar.monthrange(self.cal._date.year, self.cal._date.month)[-1]
        last_day = self.cal._date.replace(day=_last_day)
        #Create a fresh list for the dates we are updating and load them in
        self.all_dates = []
        self.month_dates = []
        for x in range((last_day-first_day).days+1):
            self.month_dates.append(first_day + dt.timedelta(days=x))
        for x, day in enumerate(self.month_dates):
            if self.cash_dates:
                if day not in self.cash_dates[0:-1][0]:
                    print(day, self.cash_dates[x][0])
                    self.cursor.execute("""INSERT INTO cashflow(cash_dates, amount)
                    VALUES(%s, %s)""", (day, self.start_money))
                    self.todays_money.append(tk.Button(self.top, text=self.start_money, fg='blue'))
                    f,h = self.cal._get_day_coords(day)
                    if (f is not None) and (h is not None):
                        self.todays_money[x].pack_configure(expand=False, fill='x', in_=self.cal._calendar[f][h], side='bottom')
                #Add income date check to update calendar with new amount
                elif day in self.cash_dates:
                    self.upd_cash_day = self.cal.get_calevents(date=day, tag='CashFlow')
                    self.cal.calevent_configure(ev_id=self.upd_cash_day, text=self.start_money)
            else:
                self.cursor.execute("""INSERT INTO cashflow(cash_dates, amount)
                    VALUES(%s, %s)""", (day, self.start_money))

    def initFlow(self):
        mindate = self.today.replace(day=1, month=1)
        maxdate = self.today + dt.timedelta(days=730)
        #Create a fresh list for the dates we are updating and load them in
        self.all_dates = []
        for x in range((maxdate-mindate).days+1):
            self.all_dates.append(mindate + dt.timedelta(days=x))
        #Test if DB has been initialized previously and initialize if it hasn't been
        if self.cash_dates:
            pass
        else:
            self.cursor.execute("""INSERT INTO cashflow(cash_dates, amount)
                VALUES(%s, %s)""", (mindate, self.start_money))
            self.conn.commit()
            self.cash_dates = self.getData("cashflow")
        #Loop the calendar initializing DB values
        for x, day in enumerate(self.all_dates):
            if day in self.cash_dates[0:-1][1]:
                pass
            else:
                if x < 10:
                    print(day, self.cash_dates[x][1])
                self.cursor.execute("""INSERT INTO cashflow(cash_dates, amount)
                VALUES(%s, %s)""", (day, self.start_money))

    def updateValues(self):
        self.income_dates = self.getData("income", "income_dates")
        self.expense_dates = self.getData("expense", "expense_dates")

    def setStartMoney(self, amt):
        self.start_money = amt
        return self.start_money

    def initiateSQL(self):
        changes_made = 0
        self.active_tables = []
        self.conn = psycopg2.connect(
            host = ***,
            port = ***,
            user = ***,
            password = ***,
            database=***
        )
        self.cursor = self.conn.cursor()
        #read current tables
        self.cursor.execute("""SELECT table_name FROM information_schema.tables
            WHERE table_schema = 'public'""")
        for table in self.cursor.fetchall():
            self.active_tables.append(table)
        #check for cashflow, income, and expense tables -- create them if missing
        if ('cashflow',) not in self.active_tables:
            self.cursor.execute("""CREATE TABLE cashflow(
                cash_id SERIAL PRIMARY KEY,
                cash_dates date,
                amount integer)"""
            )
            changes_made += 1
        if ('income',) not in self.active_tables:
            self.cursor.execute("""CREATE TABLE income(
                income_id SERIAL PRIMARY KEY,
                income_dates date,
                income integer)"""
            )
            changes_made += 1
        if ('expense',) not in self.active_tables:
            self.cursor.execute("""CREATE TABLE expense(
                expense_id SERIAL PRIMARY KEY,
                expense_dates date,
                expense integer)"""
            )
            changes_made += 1
        if changes_made > 0:
            self.conn.commit()

    def delTables(self):
        self.cursor.execute("""DROP TABLE cashflow""")
        self.cursor.execute("""DROP TABLE expense""")
        self.cursor.execute("""DROP TABLE income""")
        self.conn.commit()
    
    def cleanDB(self):
        #Delete DB entries for clean testing
        self.cursor.execute("""DELETE FROM income""")
        self.cursor.execute("""DELETE FROM expense""")
        self.cursor.execute("""DELETE FROM cashflow""")
        self.conn.commit()

    def userExpenses(self):
        self.cursor.execute("""SELECT * FROM expense""")
        return self.cursor.fetchall()

    def userIncome(self):
        self.cursor.execute("""SELECT * FROM income""")
        return self.cursor.fetchall()

    def getData(self, table, *args):
        argNum = len(args)
        if argNum == 1:
            self.select_string = str("SELECT " + args[0] + " FROM " + table)
        elif argNum == 2:
            self.select_string = str("SELECT " + args[0] + ", " + args[1] + " FROM " + table)
        elif (argNum == 3) or (argNum == 0):
            self.select_string = str("SELECT * FROM " + table)
        if self.select_string:
            self.cursor.execute(self.select_string)
            self.data_list = self.cursor.fetchall()
            self.conn.commit()
            return self.data_list
        else:
            return print("Error, wrong arguments given to getData")

#Need to look into calling my function when the virtual event self.event_generate('<<CalendarMonthChanged>>') is generated
#this might be done through _l_month or _prev_month but i dont know if I can overwrite. might have to watch for virtual events to trigger my cal to update
#    def _prev_month(self):
#        """Display the previous month."""
#        self._date = self._date - self.timedelta(days=1)
#        self._date = self._date.replace(day=1)
#        self._display_calendar()
#        self.event_generate('<<CalendarMonthChanged>>')
#        self._btns_date_range()

    def updateCal(self):
        print(self.cal._calendar)
        for items in self.todays_money:
            items.pack_forget()
        first_day = self.cal._date.replace(day=1)
        last_day = calendar.monthrange(self.cal._date.year, self.cal._date.month)[-1]
        day_coords = self.cal._get_day_coords(first_day)
        for day in range(last_day - first_day.day):
            if day in self.cash_dates[0:-1][0]:
                pass
        print(first_day, last_day, day_coords)
        
        
        #print(self.cal._calendar)
        

def main():

    CashFlow()


if __name__ == '__main__':
    main()