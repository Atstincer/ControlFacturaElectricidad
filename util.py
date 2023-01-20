import tkinter as tk
import tkinter.font as tkFont


def setFont(s):

    if s == 'footer':
        footerfont = tkFont.Font(size=8)
        return footerfont
    elif s == 'txt':
        txtfont = tkFont.Font(size=13)
        return txtfont
    elif s == 'btn':
        btnfont = tkFont.Font(size=13,weight=tkFont.BOLD)
        return btnfont
    elif s == 'title':
        titleFont = tkFont.Font(family='Helvetica',size=18,weight=tkFont.BOLD)
        return titleFont


def placev(master,vwidth=None,vheight=None,output=0):

    screen_x = master.winfo_screenwidth()
    screen_y = master.winfo_screenheight()
    if vwidth is None and vheight is None:
        vwidth, vheight = getDimensions(master)
    vx = screen_x//2 - vwidth//2
    vy = screen_y//2 - vheight//2
    if output == 0:
        return "{}x{}+{}+{}".format(vwidth,vheight,vx,vy)
    elif output == 1:
        return "+{}+{}".format(vx,vy)


def getDimensions(master=None):

    master.update()
    w = master.winfo_width()
    h = master.winfo_height()
    return w,h


def get_vmodal(master=None):

        v = tk.Toplevel()
        v.focus_set() # Provoca que la ventana tome el focus
        v.grab_set() # Deshabilita todas las otras ventanas hasta que esta ventana sea destruida.
        v.transient(master=master) # Indica que la ventana es de tipo transient, lo que 
        # significa que la ventana aparece al frente del padre.
        #v.wait_window(v) # Pausa el mainloop de la ventana de donde se hizo la invocación.
        return v