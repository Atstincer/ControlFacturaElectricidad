import tkinter as tk
from tkinter import ttk
from util import placev, setFont, get_vmodal
from f_registro_lecturas import F_registro_lecturas
from f_graficas import F_graficas
from f_config import F_config
from conexion import Conexion


class F_main(tk.Frame):

    def __init__(self,master):

        super().__init__(master)
        self.master = master
        self.master.title('CONTROL FACTURA ELECTRICA')
        self.master.geometry(placev(self.master,607,551,1))
        self.master.resizable(0,0)
        self.pack(expand=True,fill=tk.BOTH)
        self.__initFrames()
        self.__initVars()
        self.__intiComponents()
        self.__udVars()
        self.udLecturas()
        self.__initSubFrames()


    def __initFrames(self):

        self.fcliente = tk.LabelFrame(self,text='INFO CONSUMIDOR',bg='#202124',fg='#C185EE',font=setFont('title'))
        self.fcliente.pack(fill=tk.X)

        self.fcliente1 = tk.Frame(self.fcliente,bg='#202124')
        self.fcliente1.pack(side=tk.LEFT)

        self.fcliente2 = tk.Frame(self.fcliente,bg='#202124')
        self.fcliente2.pack(side=tk.RIGHT,expand=True,fill=tk.BOTH)

        self.fnb = tk.Frame(self,bg='#202124')
        self.fnb.pack(expand=True,fill=tk.BOTH)


    def __initVars(self):

        self.imgConfig = tk.PhotoImage(file=r'images\config.png').subsample(2)
        self.__id = tk.StringVar()
        self.__sucursal = tk.StringVar()
        self.__ruta = tk.StringVar()
        self.__folio = tk.StringVar()
        self.__consumidores = self.__getConsumidores()


    def __intiComponents(self):

        tk.Label(self.fcliente1,text='ID',bg='#202124',fg='#6A98D8').grid(row=1,column=0,padx=10,pady=(10,0),sticky=tk.W)
        tk.Label(self.fcliente1,textvariable=self.__id,bg='#202124',fg='#6A98D8').grid(row=2,column=0,padx=10,pady=(0,10),sticky=tk.W)

        tk.Label(self.fcliente1,text='Sucursal',bg='#202124',fg='#6A98D8').grid(row=1,column=1,padx=10,pady=(10,0),sticky=tk.W)
        tk.Label(self.fcliente1,textvariable=self.__sucursal,bg='#202124',fg='#6A98D8').grid(row=2,column=1,padx=10,pady=(0,10),sticky=tk.W)

        tk.Label(self.fcliente1,text='Ruta',bg='#202124',fg='#6A98D8').grid(row=1,column=2,padx=10,pady=(10,0),sticky=tk.W)
        tk.Label(self.fcliente1,textvariable=self.__ruta,bg='#202124',fg='#6A98D8').grid(row=2,column=2,padx=10,pady=(0,10),sticky=tk.W)

        tk.Label(self.fcliente1,text='Folio',bg='#202124',fg='#6A98D8').grid(row=1,column=3,padx=10,pady=(10,0),sticky=tk.W)
        tk.Label(self.fcliente1,textvariable=self.__folio,bg='#202124',fg='#6A98D8').grid(row=2,column=3,padx=10,pady=(0,10),sticky=tk.W)

        tk.Button(self.fcliente2,image=self.imgConfig,bg='#BF6000',activebackground='#BF6000',command=self.__btnConfigClicked).pack(side=tk.RIGHT,padx=20,pady=(0,25))

        nombres = self.__getNamesForCb()
        self.cbConsumidores = ttk.Combobox(self.fcliente2,values=nombres,state='readonly',font=('helvetica','11','bold'))
        self.cbConsumidores.pack(side=tk.RIGHT,pady=(0,25))
        self.cbConsumidores.current(0)
        self.cbConsumidores.bind('<<ComboboxSelected>>',self.__cbSelected)
        self.__setCbWidth()

        #print(ttk.Style().theme_use())

        self.nb = ttk.Notebook(self.fnb)
        self.nb.pack(expand=True,fill=tk.BOTH)


    def __btnConfigClicked(self):

        F_config(master=get_vmodal(),fp=self,consumidores=self.__consumidores)


    def __initSubFrames(self):

        #self.f_calculo_obj = F_calculo(self.nb,ventana=False)
        self.f_registro_lecturas = F_registro_lecturas(self.nb,self)
        self.f_graficas = F_graficas(self.nb,self)
        self.nb.add(self.f_registro_lecturas,text='Registro')
        #self.nb.add(self.f_calculo_obj,text='Desglose tarifa')
        self.nb.add(self.f_graficas,text='Gráficos')


    def __udVars(self):

        index = self.cbConsumidores.current()

        self.__id.set(self.__consumidores[index][0])
        self.__sucursal.set(self.__consumidores[index][2])
        self.__ruta.set(self.__consumidores[index][3])
        self.__folio.set(self.__consumidores[index][4])


    def udLecturas(self,graficos=False):
        
        self.__lecturas, self.__consumoProAgno = self.__getLecturasFromBD()
        if graficos:
            self.f_graficas.refreshFrame()


    def __getLecturasFromBD(self):


        def toFormat():

            lecturas_dic = {}
            agnos_list = []
            consumo_list = []

            for row in rows: # creando diccionarios (key=años)
                if row[3] not in lecturas_dic:
                    lecturas_dic[row[3]] = [row]
                else:
                    lecturas_dic[row[3]].append(row)
                if row[3] not in agnos_list:
                    agnos_list.append(row[3])
            
            for k in lecturas_dic: # ordenando lecturas por años (descendente)
                if len(lecturas_dic[k]) > 1:
                    lecturas_dic[k].sort(reverse=True,key=lambda x:x[4])

            agnos_list.sort()

            if len(agnos_list) > 10:
                for i in range(len(agnos_list)-10): agnos_list.pop(0)                

            for agno in agnos_list:
                kwTotal = 0
                for lectura in lecturas_dic[agno]:
                    kwTotal += lectura[9]
                kw_promedio = kwTotal / len(lecturas_dic[agno])
                consumo_list.append(kw_promedio)

            consumoProAgno = (
                tuple(agnos_list),
                tuple(consumo_list)
            )

            return lecturas_dic, consumoProAgno

        id_cliente = self.__id.get()
        cn = Conexion()
        query = f"SELECT * FROM lecturas WHERE cliente = '{id_cliente}'"
        q = cn.cursor.execute(query)
        rows = q.fetchall()
        cn.desconectar()

        if rows is None or len(rows) == 0:
            return None,None

        lecturas, consumoProAgno = toFormat()
        return lecturas, consumoProAgno


    def getInfo(self,agno=None,solo_agnos=False,lectura=None,id_consumidor=False,kwAgno_promedio=False):
        
        if id_consumidor:
            return self.__id.get()        
        if self.__lecturas is None:
            if kwAgno_promedio:
                return None,None
            return
        if agno is not None:
            return self.__lecturas[agno]
        elif solo_agnos:
            return sorted(list(self.__lecturas),reverse=True)
        elif lectura is not None: # (id,año)
            for lect in self.__lecturas[lectura[1]]:
                if str(lect[0]) == lectura[0]:
                    return lect
            if str(int(lectura[1])+1) in self.__lecturas:
                for lect in self.__lecturas[str(int(lectura[1])+1)]:
                    if str(lect[0]) == lectura[0]:
                        return lect
            return None
        elif kwAgno_promedio:
            return self.__consumoProAgno[0], self.__consumoProAgno[1]


    def __getNamesForCb(self):

        nombre_consumidores = list(map(lambda x:x[1],self.__consumidores))
        return nombre_consumidores


    def __getConsumidores(self):

        cn = Conexion()
        q = cn.cursor.execute('SELECT * FROM consumidores')
        rows = q.fetchall()
        cn.desconectar()
        return rows


    def __cbSelected(self,event=None):

        self.__udVars()
        self.udLecturas()
        #self.master.event_generate('<<cbConsumidoresSelected>>')
        self.f_registro_lecturas.setNewConsumidor()
        self.f_graficas.setNewConsumidor()


    def refreshGraficasFrame(self,agno=None):

        self.f_graficas.refreshFrame(agno)


    def refreshRegistrFrame(self,agno=None):
        
        self.f_registro_lecturas.refreshFrame(agno)


    def udConsumidores(self):

        seleccionado = self.__consumidores[self.cbConsumidores.current()]
        self.__consumidores = self.__getConsumidores()
        self.__udCbConsumidores(seleccionado)
        return self.__consumidores


    def __udCbConsumidores(self,seleccionado=None):

        index = 0
        for consumidor in self.__consumidores:
            if consumidor[0] == seleccionado[0]:
                index = self.__consumidores.index(consumidor)
                break

        names = self.__getNamesForCb()
        self.cbConsumidores.configure(values=names)
        self.cbConsumidores.current(index)
        if self.__consumidores[index][0] != seleccionado[0]:
            self.__cbSelected()
        else:
            self.__udVars()

        self.__setCbWidth()


    def __setCbWidth(self):

        values = self.cbConsumidores['values']
        maxi = 0
        for v in values:
            if len(v) > maxi: maxi = len(v)
        self.cbConsumidores.configure(width=(maxi+2))
        



if __name__ == '__main__':

    root = tk.Tk()
    app = F_main(root)
    app.mainloop()
    