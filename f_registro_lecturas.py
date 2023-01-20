import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo, showerror, askokcancel
from util import get_vmodal, setFont
from datetime import date, datetime
from datechooser import MyDatePicker
from logica import getCalculo
from conexion import Conexion
from f_calculo import F_calculo


class F_registro_lecturas(tk.Frame):


    def __init__(self,master,fp=None):

        super().__init__(master,bg='#508354')
        self.master = master
        self.fp = fp
        self.pack(expand=True,fill=tk.BOTH)
        self.__initVars()
        self.__initFrames()
        self.__initComponents()
        self.__setLecturaAnterior()
        self.bind_all('<<TarifasChanged>>',self.__udCbTarifas)
        #self.bind('<<cbConsumidoresSelected>>',self.__setNewConsumidor)


    def __initVars(self):

        self.__textBtn = tk.StringVar()
        self.__textBtn.set('Registrar')
        self.__udModeOn = False
        self.__fechaAnterior = 'fecha'
        self.__fechaActual = self.__dateHandler(date=date.today(),mode=0)
        self.__textlbObs = tk.StringVar()
        self.__lectura2UD = None
        self.__dias = tk.StringVar()
        self.__textLbLectura2UD = tk.StringVar()
        self.img_ud = tk.PhotoImage(file=r'.\images\update.png').subsample(2)
        self.img_goBack = tk.PhotoImage(file=r'.\images\go_back.png').subsample(2)
        self.img_calcular = tk.PhotoImage(file=r'.\images\calcular.png').subsample(2)
        

    def __initFrames(self):

        self.fRegPadre = tk.LabelFrame(self,bg='#202124',width=605,height=180)
        self.fRegPadre.pack(fill=tk.X)
        self.fRegPadre.pack_propagate(False)

        self.fregistrar = tk.Frame(self.fRegPadre,bg='#202124')
        self.fregistrar.pack(fill=tk.X)

        self.flecturas = tk.LabelFrame(self.fregistrar,text='Lecturas',bg='#202124',fg='#C185EE')
        self.flecturas.pack(side=tk.LEFT,padx=5,pady=5,anchor=tk.N)

        self.fLectAnterior = tk.Frame(self.flecturas,bg='#202124')
        self.fLectAnterior.pack(side=tk.LEFT,padx=5,pady=(0,5))
        self.fLectActual = tk.Frame(self.flecturas,bg='#202124')
        self.fLectActual.pack(side=tk.LEFT,padx=(0,5),pady=(0,5))

        self.fconsumoT = tk.Frame(self.fregistrar,bg='#202124')
        self.fconsumoT.pack(side=tk.LEFT,padx=(0,5),pady=5,anchor=tk.N)
        self.fconsumo = tk.LabelFrame(self.fconsumoT,text='Consumo(kWh)',bg='#202124',fg='#C185EE')
        self.fconsumo.pack()

        self.fapagar = tk.Frame(self.fregistrar,bg='#202124')
        self.fapagar.pack(side=tk.LEFT,padx=(0,5),pady=5,anchor=tk.N)

        self.ftarifa = tk.LabelFrame(self.fapagar,text='Tarifa',bg='#202124',fg='#C185EE')
        self.ftarifa.pack(fill=tk.X)

        self.fimporte = tk.LabelFrame(self.fapagar,text='Importe',bg='#202124',fg='#C185EE')
        self.fimporte.pack()

        self.fBtnUD = tk.Frame(self.fregistrar,bg='#202124')
        self.fBtnUD.pack(side=tk.LEFT,anchor=tk.N,pady=5,padx=(5,0))

        self.fBtnMain = tk.Frame(self.fregistrar,bg='#202124')
        self.fBtnMain.pack(side=tk.LEFT,expand=True,fill=tk.BOTH,pady=5,padx=5)

        self.fObs = tk.Frame(self.fRegPadre,bg='#202124')
        self.fObs.pack(fill=tk.X)

        self.ftv = tk.Frame(self,bg='#202124')
        self.ftv.pack(expand=True,fill=tk.BOTH)


    def __initComponents(self):

        tk.Label(self.fLectAnterior,text='anterior',bg='#202124',fg='#6A98D8').grid(row=0,column=0)
        tk.Label(self.fLectActual,text='actual',bg='#202124',fg='#6A98D8').grid(row=0,column=0)

        self.txtLectAnterior = tk.Entry(self.fLectAnterior,width=8,bg='#CCCCCC',justify=tk.CENTER,font=setFont('txt'))
        self.txtLectAnterior.grid(row=1,column=0,pady=(0,2))
        self.txtLectAnterior.focus_set()
        self.txtLectAnterior.bind('<KeyRelease>',self.__newInfo)

        self.txtLectActual = tk.Entry(self.fLectActual,width=8,bg='#CCCCCC',justify=tk.CENTER,font=setFont('txt'))
        self.txtLectActual.grid(row=1,column=0,pady=(0,2))
        self.txtLectActual.bind('<KeyRelease>',self.__newInfo)

        self.lbFechaAnterior = tk.Label(self.fLectAnterior,text=self.__fechaAnterior,bg='#CCCCCC')
        self.lbFechaAnterior.grid(row=2,column=0,sticky=tk.NSEW)
        self.lbFechaAnterior.bind('<Button-1>',self.__selectFechaAnterior)

        date = self.__dateHandler(s=self.__fechaActual,mode=1)
        self.lbFechaActual = tk.Label(self.fLectActual,text=date,bg='#CCCCCC')
        self.lbFechaActual.grid(row=2,column=0,sticky=tk.NSEW)
        self.lbFechaActual.bind('<Button-1>',self.__selectFechaActual)

        tk.Label(self.fconsumo,text='diario',bg='#202124',fg='#6A98D8').grid(row=0,column=0)
        tk.Label(self.fconsumo,text='total',bg='#202124',fg='#6A98D8').grid(row=0,column=1)

        self.txtKwDiario = tk.Entry(self.fconsumo,width=5,bg='#CCCCCC',justify=tk.CENTER,font=setFont('txt'))
        self.txtKwDiario.grid(row=1,column=0,padx=(8,5),pady=(0,5))

        self.txtKwTotal = tk.Entry(self.fconsumo,width=5,bg='#CCCCCC',justify=tk.CENTER,font=setFont('txt'))
        self.txtKwTotal.grid(row=1,column=1,padx=(5,0),pady=(0,5))
        self.txtKwTotal.bind('<KeyRelease>',self.__sugestLectura)

        tk.Label(self.fconsumoT,textvariable=self.__dias,bg='#202124',fg='#6A98D8').pack(anchor=tk.W,padx=5)

        self.cbTarifas = ttk.Combobox(self.ftarifa,state='readonly',width=7,font=('helvetica','11','bold'))
        self.cbTarifas.pack(padx=5,pady=(0,5),anchor=tk.E)
        self.__udCbTarifas()

        self.txtImporte = tk.Entry(self.fimporte,text='000,00',width=10,bg='#CCCCCC',justify=tk.CENTER,font=setFont('txt'))
        self.txtImporte.pack(side=tk.LEFT,padx=5,pady=(0,5))

        tk.Button(self.fBtnUD,image=self.img_ud,bg='#BF6000',activebackground='#BF6000',command=self.__autoFill).pack(pady=(10,0))
        tk.Button(self.fBtnUD,image=self.img_calcular,bg='#BF6000',activebackground='#BF6000',command=self.__vCalculoOpen).pack(pady=(5,0))
        
        tk.Label(self.fBtnMain,textvariable=self.__textLbLectura2UD,bg='#202124',fg='#6A98D8',font=setFont('btn')).pack(padx=5,pady=(5,0))

        self.btnMain = tk.Button(self.fBtnMain,textvariable=self.__textBtn,bg='#BF6000',activebackground='#BF6000',font=setFont('btn'),command=self.__btnMainClicked)
        self.btnMain.pack(expand=True,anchor=tk.CENTER,padx=5,pady=5)

        tk.Label(self.fObs,textvariable=self.__textlbObs,bg='#202124',fg='#6A98D8').pack(side=tk.LEFT,padx=10)

        self.cbAgnos = ttk.Combobox(self.ftv,state='readonly',font=('helvetica','11','bold'))
        self.cbAgnos.pack(anchor=tk.E,padx=10,pady=5)
        self.cbAgnos.bind('<<ComboboxSelected>>',self.__cbSelected) # __udTV
        self.__resetCbAgnos_values()

        self.tv_lecturas = ttk.Treeview(self.ftv,show='headings',selectmode=tk.BROWSE)

        self.tv_lecturas['columns'] = (1,2,3,4,5,6)
        self.tv_lecturas.column(1,anchor=tk.CENTER,width=120)
        self.tv_lecturas.column(2,anchor=tk.CENTER,width=60)
        self.tv_lecturas.column(3,anchor=tk.CENTER,width=120)
        self.tv_lecturas.column(4,anchor=tk.CENTER,width=90)
        self.tv_lecturas.column(5,anchor=tk.CENTER,width=90)
        self.tv_lecturas.column(6,anchor=tk.CENTER,width=100)

        self.tv_lecturas.heading(1,text='Fecha')
        self.tv_lecturas.heading(2,text='Mes')
        self.tv_lecturas.heading(3,text='Lectura')
        self.tv_lecturas.heading(4,text='Cons/dia')
        self.tv_lecturas.heading(5,text='Consumo')
        self.tv_lecturas.heading(6,text='Importe')

        self.__setTV()

        self.tv_lecturas.pack(pady=(0,5),padx=5)
        self.tv_lecturas.tag_configure('lectura',background='#202124',foreground='#6A98D8')
        self.tv_lecturas.bind('<<TreeviewSelect>>',self.__tvOnSelected)
        self.tv_lecturas.bind('<Double-1>',self.__tvOnDoubleClick)


    def __udCbTarifas(self,e=None):

        tarifas = self.__getTarifas()
        current = self.cbTarifas.get()
        if tarifas is None or tarifas == '':
            self.cbTarifas.configure(values=[''])
        else:
            self.cbTarifas.configure(values=tarifas[::-1])
        if current != '' and current is not None and current in tarifas:
            self.cbTarifas.set(current)
        else:
            self.cbTarifas.current(0)
        self.__setCbWidth(self.cbTarifas)


    def __getTarifas(self):

        try:
            cn = Conexion()
            q = cn.cursor.execute("SELECT tarifa FROM tarifas")
            rows = q.fetchall()
            cn.desconectar()
        except:
            print('Error al intentar acceder a la BD')
            return

        tarifas = list(map(lambda x: x[0],rows))
        return tarifas


    def __vCalculoOpen(self):

        v = tk.Toplevel()
        info = (self.txtLectAnterior.get(),self.txtLectActual.get(),self.cbTarifas.get())
        F_calculo(v,self,info,True)


    def __setLecturaAnterior(self):

        items = self.tv_lecturas.get_children()
        self.txtLectAnterior.delete(0,tk.END)
        
        if len(items) > 0:
            item0_values = self.tv_lecturas.item(items[0],'values')
            self.txtLectAnterior.insert(0,item0_values[2])
            self.__fechaAnterior = item0_values[0]
        else:
            self.__fechaAnterior = 'fecha'

        self.__udLbFechas()


    def __cbSelected(self,e):

        self.__udTV()
        if not self.__udModeOn:
            self.__setLecturaAnterior()
        self.fp.refreshGraficasFrame(agno=self.cbAgnos.get())


    def refreshFrame(self,agno=None):

        if agno is not None:
            self.cbAgnos.set(agno)
        self.__udTV()


    def __newInfo(self,e):

        if self.__udModeOn:
            return
        self.__autoFill()


    def __sugestLectura(self,e):

        if self.__udModeOn:
            return

        anterior = self.txtLectAnterior.get()
        consumo = self.txtKwTotal.get()

        if anterior == '':
            return

        try:
            int(anterior)
            int(consumo)
        except:
            return

        self.txtLectActual.delete(0,tk.END)
        self.txtLectActual.insert(0,int(anterior)+int(consumo))
    

    def __tvOnDoubleClick(self,e):

        item = self.tv_lecturas.selection()
        if len(item) == 0:
            return
        values = (item[0],self.cbAgnos.get())
        #print(values)
        self.__setUdMode(values)


    def __setUdMode(self,lectura):

        self.__lectura2UD = self.fp.getInfo(lectura=lectura)
        #print('Lect2UD',self.__lectura2UD)
        if self.__lectura2UD is None:
            return
        self.__cleanFregistro()
        self.__showResult(self.__lectura2UD,lectura=True)
        self.__textLbLectura2UD.set(f'Lect. {self.__lectura2UD[4]}/{self.__lectura2UD[3]}')
        if self.__udModeOn:
            return
        self.__udModeOn = True
        self.__textBtn.set('Actualizar')
        self.btnEliminar = tk.Button(self.fBtnMain,text='Eliminar',bg='#BF6000',activebackground='#BF6000',font=setFont('btn'),command=self.__eliminarLectura)
        self.btnEliminar.pack()
        self.btnGoBack = tk.Button(self.fBtnUD,image=self.img_goBack,bg='#BF6000',activebackground='#BF6000',command=self.__goBack)
        self.btnGoBack.pack(pady=5)


    def __goBack(self):

        self.__cleanFregistro()
        self.__setRegularMode()
        self.__setLecturaAnterior()


    def __eliminarLectura(self):

        choise = askokcancel('Confirmación',f'Seguro que desea eliminar el registro\nde la lectura {self.__lectura2UD[4]}/{self.__lectura2UD[3]}?',master=self.master)
        if not choise:
            return
        
        try:
            cn = Conexion()
            cn.cursor.execute("DELETE * FROM lecturas WHERE id = %d" % (self.__lectura2UD[0]))
            cn.cursor.commit()
            cn.desconectar()
        except:
            showerror('Atención','No se pudo eliminar el registro.\nOcurrió un problema al intentar acceder\na la base de datos.',master=self.master)
            return

        self.__setRegularMode()
        self.fp.udLecturas(graficos=True)
        self.__udTV(cbAgnos=True)

        showinfo('Información','Registro eliminado correctamente.',master=self.master)


    def __cleanFregistro(self):

        txts = [
            self.txtLectAnterior,
            self.txtLectActual,
            self.txtKwDiario,
            self.txtKwTotal,
            self.txtImporte
        ]
        for i in txts: i.delete(0,tk.END)
        self.__fechaAnterior = 'fecha'
        self.__fechaActual = self.__dateHandler(date=date.today(),mode=0)
        self.__udLbFechas()
        self.__dias.set('')
        self.__textlbObs.set('')


    def __tvOnSelected(self,e):

        item = self.tv_lecturas.selection()
        if len(item) == 0:
            return
        self.__fechaAnterior = self.tv_lecturas.item(item[0])['values'][0]
        lectura = self.tv_lecturas.item(item[0])['values'][2]
        self.txtLectAnterior.delete(0,tk.END)
        self.txtLectAnterior.insert(0,lectura)
        self.lbFechaAnterior.configure(text=self.__dateHandler(s=self.__fechaAnterior,mode=1))
        if self.__udModeOn:
            return
        self.__autoFill()
        

    def __setTV(self):

        lecturas = self.fp.getInfo(agno=self.cbAgnos.get())
        if lecturas is None:
            self.tv_lecturas.configure(height=0)
            return
        self.tv_lecturas.configure(height=len(lecturas))
        for i in lecturas:
            self.tv_lecturas.insert('','end',iid=i[0],text=f'Lectura {i[4]}/{i[3]}',values=(i[2],i[4],i[7],i[8],i[9],i[11]),tags=('lectura',))


    def __udTV(self,e=None,cbAgnos=False):

        if cbAgnos:
            self.__resetCbAgnos_values()
        self.__cleanTV()
        self.__setTV()


    def __cleanTV(self):

        items = self.tv_lecturas.get_children()
        if len(items) != 0 and items is not None:
            for i in items: self.tv_lecturas.delete(i)


    def __udCbAgnos(self):

        agnos = self.fp.getInfo(solo_agnos=True)
        if agnos is None or len(agnos) == 0:
            agnos = ['',]
        self.cbAgnos.configure(values=agnos)
        self.cbAgnos.current(0)
        self.__setCbWidth(self.cbAgnos)


    def setNewConsumidor(self):

        self.__udCbAgnos()
        self.__udTV()
        if not self.__udModeOn:
            self.__setLecturaAnterior()


    def __btnMainClicked(self):

        info = self.__getInfo()
        if not self.__validarInfo(info):
            return

        #id_lectura = (info[3].replace('/',''))[2:]
        if not self.__udModeOn:
            cliente = self.fp.getInfo(id_consumidor=True)

        mes_factura, agno_factura = self.__makeMesAgnoFactura(info[3])

        if not self.__validarLectura(mes_factura,agno_factura):
            return

        if self.__udModeOn:
            query = "UPDATE lecturas SET fecha_actual='{}',fecha_anterior='{}',lectura_ant='{}',lectura_mes='{}',consumoxdia='{}',consumo='{}',tarifa='{}',importe='{}' WHERE id={}".format(info[3],info[2],info[0],info[1],info[4],info[5],info[6],info[7],self.__lectura2UD[0])
        else:
            query = "INSERT INTO lecturas (cliente,fecha_actual,agno_factura,mes_factura,fecha_anterior,lectura_ant,lectura_mes,consumoxdia,consumo,tarifa,importe) VALUES ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')".format(cliente,info[3],agno_factura,mes_factura,info[2],info[0],info[1],info[4],info[5],info[6],info[7])

        try:
            cn = Conexion()
            cn.cursor.execute(query)
            cn.cursor.commit()
            cn.desconectar()
        except:
            showerror('Atención','Ha ocurrido un error al intentar registrar\nla lectura en la base de datos.')
            return

        self.fp.udLecturas(graficos=True)
        self.__udTV(cbAgnos=True)
        self.__cleanFregistro()
        self.__setLecturaAnterior()
        
        if self.__udModeOn:
            msg_title = 'Actualizado'
            msg_cuerpo = 'Lectura actualizada correctamente.'
            self.__setRegularMode()
        else:
            msg_title = 'Registrado'
            msg_cuerpo = 'Lectura registrada correctamente.'
        
        showinfo(msg_title,msg_cuerpo,master=self.master)


    def __setRegularMode(self):

        self.__udModeOn = False
        self.__lectura2UD = None
        self.__textLbLectura2UD.set('')
        self.__textBtn.set('Registrar')
        self.btnEliminar.destroy()
        self.btnGoBack.destroy()


    def __makeMesAgnoFactura(self,fecha):

            mes = fecha[3:5]
            agno = fecha[6:]
            if mes == '12':
                mes = '01'
                agno = str(int(agno)+1)
            else:
                mes = str(int(mes)+1)
                if len(mes) == 1:
                    mes = f'0{mes}'
            return mes, agno


    def __validarLectura(self,mes_factura,agno_factura):

        lecturas = self.fp.getInfo(agno=agno_factura)
        if lecturas is None or len(lecturas) == 0:
            return True

        for lectura in lecturas:
            if lectura[4] == mes_factura:
                if self.__udModeOn:
                    if lectura[0] != self.__lectura2UD[0]:
                        showerror('Atención','No se puede actualizar la lectura. Ya existe\notra lectura del mismo mes y año en sistema.')
                        return False
                else:
                    showerror('Atención','No se puede registrar la lectura. Ya existe\notra lectura del mismo mes y año en sistema.')
                    return False

        return True


    def __getInfo(self):

        info = [
            self.txtLectAnterior.get(),
            self.txtLectActual.get(),
            self.__fechaAnterior,
            self.__fechaActual,
            self.txtKwDiario.get(),
            self.txtKwTotal.get(),
            self.cbTarifas.get(),
            self.txtImporte.get()
        ]
        return info


    def __validarInfo(self,info,full=True,msg=True):

        if info[0] == '':
            if msg:
                showerror('Atención','Debe proporcionar la "lectura anterior".',master=self.master)
            return False

        if info[1] == '':
            if msg:
                showerror('Atención','Debe proporcionar la "lectura actual".',master=self.master)
            return False

        try:
            int(info[0])
            int(info[1])
        except:
            if msg:
                showerror('Atención','Las lecturas no son correctas.\nChequee por favor.',master=self.master)
            return False

        if int(info[0]) > int(info[1]):
            if msg:
                showerror('Atención','Las lecturas no son correctas.\nChequee por favor.',master=self.master)
            return False

        if full:

            if info[4] == '':
                showerror('Atención','Debe proporcionar el "consumo por día".',master=self.master)
                return False

            if info[5] == '':
                showerror('Atención','Debe proporcionar el "consumo total".',master=self.master)
                return False

            if info[7] == '':
                showerror('Atención','Debe proporcionar el "importe total".',master=self.master)
                return False

            try:
                int(info[4])
                int(info[5])
                float(info[7])
            except:
                showerror('Atención','Los valores "Consumo(kw)" o "Importe"\nno son correctos. Chequee por favor.',master=self.master)
                return False

        return True


    def __dateHandler(self,date=None,s=None,mode=0):

        if s == 'fecha' or s == '':
            return s
        elif date is not None:
            day = date.day
            month = date.month
            year = date.year

            if len(str(day)) == 1:
                day = f'0{day}'
            if len(str(month)) == 1:
                month = f'0{month}'
        elif s is not None:
            day = s[:2]
            month = s[3:5]
            year = s[6:]

        if mode == 0: # 00/00/0000
            fecha_str = f'{day}/{month}/{year}'
        elif mode == 1: # 00/00/00
            fecha_str = f'{day}/{month}/{str(year)[2:]}'

        return fecha_str


    def setFechaAnterior(self,fecha):

        self.__fechaAnterior = fecha
        self.__udLbFechas()
        if self.__udModeOn:
            return
        self.__autoFill()


    def setFechaActual(self,fecha):

        self.__fechaActual = fecha
        self.__udLbFechas()
        if self.__udModeOn:
            return
        self.__autoFill()


    def __selectFechaAnterior(self,e):

        MyDatePicker(get_vmodal(),self,'anterior',self.__fechaAnterior,e)


    def __selectFechaActual(self,e):

        MyDatePicker(get_vmodal(),self,'actual',self.__fechaActual,e)


    def __autoFill(self,e=None):

        info = self.__getInfo()

        if not self.__validarInfo(info,full=False,msg=False):
            return

        result = getCalculo(info,solo_tpl=True)
        self.__showResult(result)
        #self.fp.updateCalculoObj(info,cadena)


    def __showResult(self,data,lectura=False):

        txts = [
            self.txtLectAnterior,
            self.txtLectActual,
            self.txtKwDiario,
            self.txtKwTotal,
            self.txtImporte
        ]

        if not lectura:
            for i in range(3):
                txts[i+2].delete(0,tk.END)
                txts[i+2].insert(0,data[i])
            self.__dias.set(f'- para {data[3]} días')
            if data[4] is not None and data[5] is not None:
                self.__textlbObs.set(f'Estimado en 30 días de {data[4]}kws a pagar {data[5]}cup.')
            else:
                self.__textlbObs.set('')
                #print('No estimado..')
            return

        for i in range(len(txts)):
            if i < 4:
                txts[i].insert(0,data[i+6])
            else:
                txts[i].insert(0,data[i+7])

        if data[5] is None:
            self.__fechaAnterior = 'fecha'
        else:
            self.__fechaAnterior = data[5]
        
        self.__fechaActual = data[2]
        self.__udLbFechas()
        self.cbTarifas.set(data[10])


    def __udLbFechas(self):
        
        self.lbFechaAnterior.configure(text=self.__dateHandler(s=self.__fechaAnterior,mode=1))
        self.lbFechaActual.configure(text=self.__dateHandler(s=self.__fechaActual,mode=1))


    def __resetCbAgnos_values(self):

        agno_anterior = self.cbAgnos.get()
        agnos = self.fp.getInfo(solo_agnos=True)
        if agnos is None:
            agnos = ['']
        self.cbAgnos.configure(values=agnos)
        if agno_anterior in agnos:
            self.cbAgnos.set(agno_anterior)
        else:
            self.cbAgnos.current(0)
        self.__setCbWidth(self.cbAgnos)
        

    def __setCbWidth(self,cb):

        values = cb['values']
        maxi = 0
        for v in values:
            if len(v) > maxi: maxi = len(v)
        if maxi == 0: return
        cb.configure(width=(maxi+2))