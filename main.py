import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont
from f_main import F_main

import pyodbc
from tkinter.messagebox import showinfo



if __name__ == '__main__':

    root = tk.Tk()
    try:
        root.iconphoto(True, tk.PhotoImage(file='./images/bombillo.png'))
    except:
        pass
    defaultfont = tkFont.nametofont("TkDefaultFont")
    defaultfont.configure(size=13)

    style = ttk.Style() 
    style.theme_use('alt')
    # print(ttk.Style().theme_names()) # 'winnative','clam','alt','default','classic','vista','xpnative'
    #print(style.theme_use())

    style.configure('TNotebook.Tab',background='#202124', font='helvetica 18',foreground='#C185EE')
    style.configure('TNotebook',background='#202124')
    style.map('TNotebook.Tab',background=[('selected','#BF6000')],foreground=[('selected','black')])

    root.option_add('*TCombobox*Listbox*Background', '#654D7D')
    root.option_add('*TCombobox*Listbox*Foreground', 'black')
    root.option_add('*TCombobox*Listbox*selectBackground', '#BF6000')
    root.option_add('*TCombobox*Listbox*selectForeground', 'black')
    root.option_add('*TCombobox*Listbox.font', ('helvetica', '11'))   # apply font to combobox list

    # afecta a los Combobox con state='normal'
    style.configure('TCombobox',background='#BF6000',fieldbackground='#654D7D')
    
    # the following alters the Combobox entry field (Combobox state='readonly')
    style.map('TCombobox', fieldbackground=[('readonly', '#202124')])
    style.map('TCombobox', selectbackground=[('readonly', '#202124')])
    style.map('TCombobox', selectforeground=[('readonly', '#C185EE')])
    style.map('TCombobox', background=[('readonly', '#BF6000')])
    style.map('TCombobox', foreground=[('readonly', '#C185EE')])


    def fixed_map(option):
        return [elm for elm in style.map('Treeview', query_opt=option) if elm[:2] != ('!disabled', '!selected')]
 
    style.map('Treeview', foreground=fixed_map('foreground'), background=fixed_map('background'))
    style.configure('Treeview.Heading',background='#654D7D',font=('helvetica','11','bold')) # ,foreground='blue'

    app = F_main(root)

    # showinfo('Availables drivers',pyodbc.drivers())

    app.mainloop()
