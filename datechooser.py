import tkinter as tk
from tkinter import ttk
import calendar, time, locale
from datetime import date
from util import setFont, placev



class MyDatePicker(tk.Frame):


    def __init__(self, master=None, fp=None, request=None, date=None, event=None):

        super().__init__(master,bg='#999999')
        self.master = master
        self.fp = fp
        self.request = request
        if date == 'fecha' or date is None:
            self.date = ''
        else:
            self.date = date
        if self.date != '':
            self.date = self.date.split('/')
        self.master.title('Calendario')
        self.master.resizable(0, 0)
        if event is None:
            self.master.geometry(placev(self.master,270,250,output=1))
        else:
            self.master.geometry("+{}+{}".format(event.x_root,event.y_root))
        self.pack(expand=True,fill=tk.BOTH)
        self.init_frames()
        self.init_needed_vars()
        self.init_components_f1()
        self.make_calendar()
        self.confiCalender()
        

    def init_frames(self):

        self.frame1 = tk.Frame(self) # botones y label (mes/año)
        self.frame1.pack(expand=True,fill=tk.X)

        self.frame_days = tk.Frame(self,bg='#9B7E7B') # botones días
        self.frame_days.pack()


    def init_needed_vars(self):

        #locale.setlocale(locale.LC_ALL, 'es-ES')
        #self.month_names = tuple(calendar.month_name) # meses del año
        self.month_names = ('','Enero','Febrero','Marzo','Abril','Mayo','Junio','Julio','Agosto','Sept','Octubre','Noviembre','Diciembre')
        self.month_colors = ('#0000DD','#00954A','#E2252C','#BF6000')
        #self.day_names = tuple(calendar.day_abbr) # abreviatura dias de la semana
        self.day_names = ('Lun','Mar','Mie','Jue','Vie','Sab','Dom')
        if self.date == '':
            self.year = int(time.strftime("%Y")) # Year with century as a decimal number.
            #self.month = time.strftime("%B") # Locale’s full month name.
            self.month = self.month_names[date.today().month]
        else:
            self.year = int(self.date[2])
            self.month = self.month_names[int(self.date[1])]
        self.lbl_str_var = tk.StringVar()
        self.style = ttk.Style()
        self.style.configure('Dom.TButton',foreground='red')


    def confi_f1(self,month,year):

        self.lbl_str_var.set(month + ' ' + year)
        index = self.month_names.index(month)
        if index > 0 and index < 3 or index > 11:
            self.lbl_month.configure(bg=self.month_colors[0])
            self.frame1.configure(bg=self.month_colors[0])
        elif index > 2 and index < 6:
            self.lbl_month.configure(bg=self.month_colors[1])
            self.frame1.configure(bg=self.month_colors[1])
        elif index > 5 and index < 9:
            self.lbl_month.configure(bg=self.month_colors[2])
            self.frame1.configure(bg=self.month_colors[2])
        elif index > 8 and index < 12:
            self.lbl_month.configure(bg=self.month_colors[3])
            self.frame1.configure(bg=self.month_colors[3])


    def init_components_f1(self):

        ttk.Button(self.frame1, text="←", width=3, command=self.prev_month).pack(side=tk.LEFT,padx=5,pady=5)
        self.lbl_month = tk.Label(self.frame1, textvariable=self.lbl_str_var,font=setFont('title'),bg='#E2252C',fg='#CCCCCC')
        self.lbl_month.pack(side=tk.LEFT,expand=True,fill=tk.X,pady=5)
        ttk.Button(self.frame1, text="→", width=3, command=self.next_month).pack(side=tk.RIGHT,padx=5,pady=5)        


    def prev_month(self):

        index_current_month = int(self.month_names.index(self.month))
        index_prev_month = index_current_month - 1

        #  index 0 is empty string, use index 12 instead, which is index of December.
        if index_prev_month == 0:
            self.month = self.month_names[12]
            self.year -= 1
        else:
            self.month = self.month_names[index_prev_month]

        self.make_calendar()

        if self.date != '':
            if self.month == self.month_names[int(self.date[1])]:
                if self.year == int(self.date[2]):
                    self.confiCalender()


    def next_month(self):

        index_current_month = int(self.month_names.index(self.month))

        #  index 13 does not exist, use index 1 instead, which is January.
        try:
            self.month = self.month_names[index_current_month + 1]
        except IndexError:
            self.month = self.month_names[1]
            self.year += 1

        self.make_calendar()

        if self.date != '':
            if self.month == self.month_names[int(self.date[1])]:
                if self.year == int(self.date[2]):
                    self.confiCalender()


    def fill_days(self):

        col = 0
        #  Creates days label
        for day in self.day_names:
            if self.day_names.index(day) < 6:
                tk.Label(self.frame_days, text=day,bg='#C2C2C2').grid(row=0, column=col,sticky=tk.S+tk.N+tk.E+tk.W)
            elif self.day_names.index(day) == 6:
                tk.Label(self.frame_days, text=day,bg='#CCAAA2',fg='red').grid(row=0, column=col,sticky=tk.S+tk.N+tk.E+tk.W)
            col += 1        


    def make_calendar(self):

        self.confi_f1(self.month,str(self.year))
        month = self.month_names.index(self.month)
        self.m_cal = calendar.monthcalendar(self.year, month)
        w_list = self.frame_days.winfo_children()

        if len(w_list) != 0:
            for item in w_list: item.destroy()

        self.fill_days()

        #  build date buttons.
        for week in self.m_cal:
            row = self.m_cal.index(week) + 1
            for date in week:
                col = week.index(date)
                if date == 0:
                    continue
                self.make_button(str(date), str(row), str(col))


    def make_button(self, date, row, column):

        if column == '6':
            exec(
                "self.btn_" + date + "= tk.Button(self.frame_days, text=" + date + ", width=4, foreground='red', background='#CCAAA2')\n"    
                "self.btn_" + date + ".grid(row=" + row + " , column=" + column + ",padx=2,pady=2)\n"
                "self.btn_" + date + ".bind(\"<Button-1>\", self.set_date)"
            )
        else:
            exec(
                "self.btn_" + date + "= tk.Button(self.frame_days, text=" + date + ", width=4)\n"
                "self.btn_" + date + ".grid(row=" + row + " , column=" + column + ",padx=2,pady=2)\n"
                "self.btn_" + date + ".bind(\"<Button-1>\", self.set_date)"
            )


    def confiCalender(self):

        if self.date != '':
            date = str(int(self.date[0]))
            exec(
                "self.btn_" + date + ".configure(background='red',foreground='white')"
            )
    

    def set_date(self, clicked=None):

        clicked_button = clicked.widget
        year = str(self.year)
        month = self.month_names.index(self.month)
        date = clicked_button['text']

        #  Change string format for different date formats.
        full_date = '%02d/%02d/%s' % (date, month, year)

        if self.request == 'anterior':
            self.fp.setFechaAnterior(full_date)
        elif self.request == 'actual':
            self.fp.setFechaActual(full_date)

        self.master.destroy()
        


if __name__ == '__main__':

    root = tk.Tk()
    app = MyDatePicker(root)
    app.mainloop()
