import tkinter as tk
from tkinter import ttk
from util import placev
from f_consumidores import F_consumidores
from f_tarifas import F_tarifas


class F_config(tk.Frame):


    def __init__(self,master,fp=None,consumidores=None):

        super().__init__(master)
        self.master = master
        self.fp = fp
        self.consumidores = consumidores
        self.master.title('Configuraciones')
        self.master.resizable(0,0)
        self.master.geometry(placev(self.master,716,465,output=1))
        self.pack()
        self.__initComponentes()


    def __initComponentes(self):
        
        self.nb = ttk.Notebook(self)
        self.nb.pack()
        self.fConsumidores = F_consumidores(self.nb,self,self.consumidores)
        self.nb.add(self.fConsumidores,text='Consumidores')
        self.fTarifas = F_tarifas(self.nb,self)
        self.nb.add(self.fTarifas,text='Tarifas')


    def udConsumidores(self):

        consumidores = self.fp.udConsumidores()
        self.fConsumidores.udConsumidores(consumidores)


      



if __name__ == '__main__':

    root = tk.Tk()
    app = F_config(root)
    app.mainloop()