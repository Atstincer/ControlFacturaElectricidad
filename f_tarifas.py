import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showerror,showinfo, askyesno
from util import setFont
from conexion import Conexion


# 0-100-0.33,101-150-1.07,151-200-1.43,201-250-2.46,251-300-3.0,301-350-4.0,351-400-5.0,401-450-6.0,451-500-7.0,501-600-9.2,601-700-9.45,701-1000-9.85,1001-1800-10.8,1801-2600-11.8,2601-3400-12.9,3401-4200-13.95,4201-5000-15.0,5001-final-20.0

class F_tarifas(tk.Frame):

    def __init__(self,master,fp=None):

        super().__init__(master,bg='#202124')
        self.master = master
        self.fp = fp
        #self.master.geometry('620x424')
        self.pack(fill=tk.BOTH)
        self.__initVars()
        self.__initFrames()
        self.__initComponents()
        self.__initRangos()     
        self.__udRangos()


    def __initVars(self):

        self.__rangos = 1
        self.imgMas = tk.PhotoImage(file=r'.\images\mas.png').subsample(2)
        self.imgMenos = tk.PhotoImage(file=r'.\images\menos.png').subsample(2)
        self.__tarifas = self.__getTarifasBD()
        self.__newTarifa = False

    
    def __initFrames(self):

        self.fRangos = tk.LabelFrame(self,text='Rangos (Kwts)',bg='#202124',fg='#C185EE',font=setFont('title'),width=468,height=417)
        self.fRangos.pack_propagate(False)
        self.fRangos.pack(side=tk.LEFT,pady=5,padx=5,fill=tk.Y)

        self.fRangosLeft = tk.Frame(self.fRangos,bg='#202124')
        self.fRangosLeft.pack(side=tk.LEFT,fill=tk.Y)

        self.fRangosRight = tk.Frame(self.fRangos,bg='#202124')
        self.fRangosRight.pack(side=tk.LEFT,fill=tk.Y)

        self.fRangosA = tk.Frame(self.fRangosLeft,bg='#202124')
        self.fRangosA.pack(pady=(5,0),padx=10)

        self.fRangosB = tk.Frame(self.fRangosLeft,bg='#202124')
        self.fRangosB.pack(pady=(0,5),padx=10,fill=tk.X)

        self.fRangosC = tk.Frame(self.fRangosRight,bg='#202124')
        self.fRangosC.pack(pady=(5,0),padx=10)

        self.fCb = tk.Frame(self,bg='#202124')
        self.fCb.pack(side=tk.RIGHT,pady=5,padx=5,expand=True,fill=tk.BOTH)

        self.fBtns = tk.Frame(self,bg='#202124')
        self.fBtns.pack(side=tk.RIGHT,pady=5,padx=5,fill=tk.Y)        


    def __initFrameC(self):

        self.lbCD.configure(text='Desde')
        self.lbCH.configure(text='Hasta')
        self.lbCP.configure(text='Precio')        


    def __clearFrameC(self):

        self.lbCD.configure(text='')
        self.lbCH.configure(text='')
        self.lbCP.configure(text='')


    def __Left2Right(self):

        desde, precio = self.__getInfoRLast()

        self.fRangosB.destroy()

        self.fRangosB = tk.Frame(self.fRangosRight,bg='#202124')
        self.fRangosB.pack(pady=(0,5),padx=10,fill=tk.X)

        self.__setLastR(desde,precio)


    def __Right2Left(self):

        desde, precio = self.__getInfoRLast()

        self.fRangosB.destroy()

        self.fRangosB = tk.Frame(self.fRangosLeft,bg='#202124')
        self.fRangosB.pack(pady=(0,5),padx=10,fill=tk.X)

        self.__setLastR(desde,precio)


    def __setLastR(self,desde=None,precio=None):

        if desde is None:
            desde = ''
        self.lbRLastD = tk.Label(self.fRangosB,text=desde,bg='#CCCCCC',font=setFont('txt'),width=6)
        self.lbRLastD.grid(row=0,column=0,pady=5,padx=5)

        self.lbRLastH = tk.Label(self.fRangosB,text='...',bg='#CCCCCC',font=setFont('txt'),width=6)
        self.lbRLastH.grid(row=0,column=1,pady=5,padx=5)

        self.txtRLastP = tk.Entry(self.fRangosB,bg='#CCCCCC',font=setFont('txt'),width=6,justify=tk.CENTER)
        self.txtRLastP.grid(row=0,column=2,pady=5,padx=5)
        if precio is not None:
            self.txtRLastP.insert(0,precio)


    def __getInfoRLast(self):

        desde = self.lbRLastD['text']
        precio = self.txtRLastP.get()
        return desde, precio


    def __initComponents(self):

        tk.Label(self.fRangosA,text='Desde',width=6,font=setFont('txt'),bg='#202124',fg='#6A98D8').grid(row=0,column=0,sticky=tk.W,padx=5)
        tk.Label(self.fRangosA,text='Hasta',width=6,font=setFont('txt'),bg='#202124',fg='#6A98D8').grid(row=0,column=1,sticky=tk.W,padx=5)
        tk.Label(self.fRangosA,text='Precio',width=6,font=setFont('txt'),bg='#202124',fg='#6A98D8').grid(row=0,column=2,sticky=tk.W,padx=5)

        self.lbCD = tk.Label(self.fRangosC,width=6,font=setFont('txt'),bg='#202124',fg='#6A98D8')
        self.lbCD.grid(row=0,column=0,sticky=tk.W,padx=5)
        self.lbCH = tk.Label(self.fRangosC,width=6,font=setFont('txt'),bg='#202124',fg='#6A98D8')
        self.lbCH.grid(row=0,column=1,sticky=tk.W,padx=5)
        self.lbCP = tk.Label(self.fRangosC,width=6,font=setFont('txt'),bg='#202124',fg='#6A98D8')
        self.lbCP.grid(row=0,column=2,sticky=tk.W,padx=5)

        tk.Button(self.fBtns,image=self.imgMenos,bg='#654D7D',activebackground='#654D7D',command=self.__btnMenosClicked).grid(row=1,column=3,pady=35,padx=(0,5))
        tk.Button(self.fBtns,image=self.imgMas,bg='#654D7D',activebackground='#654D7D',command=self.__btnMasClicked).grid(row=1,column=4,pady=35)

        self.cbTarifas = ttk.Combobox(self.fCb,font=('helvetica','11','bold'))
        self.cbTarifas.pack(pady=(35,5))
        self.__udCbTarifas(udRangos=False)
        self.cbTarifas.bind('<<ComboboxSelected>>',self.__udRangos)
        self.cbTarifas.bind('<KeyRelease>',self.__cbWriting)

        self.btnRegistrar = tk.Button(self.fCb,text='Registrar',font=setFont('btn'),state='disable',bg='#BF6000',activebackground='#BF6000',command=self.__registrarBD)
        self.btnRegistrar.pack(pady=(30,5))

        self.btnActualizar = tk.Button(self.fCb,text='Actualizar',font=setFont('btn'),bg='#BF6000',activebackground='#BF6000',command=self.__actualizarBD)
        self.btnActualizar.pack(pady=5)

        self.btnEliminar = tk.Button(self.fCb,text='Eliminar',font=setFont('btn'),bg='#BF6000',activebackground='#BF6000',command=self.__eliminarBD)
        self.btnEliminar.pack(pady=(5,30))

        tk.Button(self.fCb,text='Limpiar',font=setFont('btn'),bg='#BF6000',activebackground='#BF6000',command=self.__cleanRangos).pack(pady=5)
        tk.Button(self.fCb,text='Contraer\ny\nlimpiar',font=setFont('btn'),bg='#BF6000',activebackground='#BF6000',command=self.__contraerLimpiar).pack(pady=5)
        

    def __udTarifas(self):

        self.__tarifas = self.__getTarifasBD()


    def __registrarBD(self):

        info = self.__getInfo()

        if not self.__validarInfo(info):
            return

        tarifa = self.cbTarifas.get()        

        if not self.__validarTarifa(tarifa):
            showerror('Atención','No se puede realizar la operación. Ya existe una\ntarifa con el mismo nombre.')
            return

        rangos = self.__makeStr(info)

        try:
            cn = Conexion()
            cn.cursor.execute("INSERT INTO tarifas (tarifa,rangos) VALUES ('{}','{}')".format(tarifa,rangos))
            cn.cursor.commit()
            cn.desconectar()
        except:
            print('Error al acceder a la base de datos.')
            return

        self.__udTarifas()
        self.__udCbTarifas()
        self.event_generate('<<TarifasChanged>>')
        #self.__setNewTarifaOff()
        showinfo('Información','Tarifa registrada correctamente')


    def __actualizarBD(self):
        
        info = self.__getInfo()

        if not self.__validarInfo(info):
            return

        tarifa = self.cbTarifas.get()        

        if not self.__validarTarifa(tarifa,update=True):
            showerror('Atención','No se puede actualizar.')
            return

        rangos = self.__makeStr(info)

        try:
            cn = Conexion()
            cn.cursor.execute("UPDATE tarifas SET rangos='%s' WHERE tarifa='%s'" % (rangos,tarifa))
            cn.cursor.commit()
            cn.desconectar()
        except:
            print('Error al acceder a la base de datos.')
            return

        self.__udTarifas()
        #self.__udCbTarifas()
        #self.event_generate('<<TarifasChanged>>')
        #self.__setNewTarifaOff()
        showinfo('Información','Tarifa actualizada correctamente')


    def __eliminarBD(self):
        
        tarifa = self.cbTarifas.get()

        if tarifa not in self.__tarifas:
            showerror('Atención','No se puede eliminar. La tarifa no\nestá registrada en la BD.')
            return

        choise = askyesno('Confirmación','Seguro que desea eliminar la información\nde esta tarifa.')

        if not choise:
            return

        try:
            cn = Conexion()
            cn.cursor.execute("DELETE * FROM tarifas WHERE tarifa = '%s'" % (tarifa))
            cn.cursor.commit()
            cn.desconectar()
        except:
            print('Error accediendo a la BD')
            return

        self.__udTarifas()
        self.__udCbTarifas()
        self.event_generate('<<TarifasChanged>>')
        #self.__setNewTarifaOff()
        showinfo('Información','Tarifa eliminada correctamente')


    def __validarTarifa(self,tarifa,update=False):

        try:
            cn = Conexion()
            q = cn.cursor.execute("SELECT * FROM tarifas WHERE tarifa = '%s'" % (tarifa))
            rows = q.fetchall()
            cn.desconectar()
        except:
            print('Error al acceder a la BD')
            return False

        if len(rows) == 0:
            return True

        if update:
            if len(rows) == 1:
                return True

        return False


    def __validarInfo(self,info):

        for r in info[:-1]:

            if r[0] == '' or r[1] == '' or r[2] == '':
                showerror('Atención','Debe llenar todos los ampos.')
                return False

            try:
                if int(r[0]) > int(r[1]):
                    showerror('Atención',f'Al menos uno de los rangos es incorrecto.\nObtuvimos "desde {r[0]} hasta {r[1]} kws". Chequee por favor.')
                    return False
                float(r[2])
            except:
                showerror('Atención',f'Los valores de alguno de los rangos no son correctos.\nObtuvimos "desde {r[0]} hasta {r[1]} kws, a {r[2]}". Chequee por favor.')
                return False

        if info[-1][0] == '' or info[-1][2] == '':
            showerror('Atención','Debe llenar todos los ampos.')
            return False

        try:
            int(info[-1][0])
            float(info[-1][2])
        except:
            showerror('Atención',f'Los valores del último rango no son correctos.\nObtuvimos "de {info[-1][0]} kws en adelante, a {info[-1][2]}". Chequee por favor.')
            return False

        return True


    def __makeStr(self,info):

        rangos = ''
        for r in info:
            rangos += r[0] + '-' + r[1] + '-' + r[2] + ','
        return rangos[:-1]


    def __getInfo(self):

        info = []
        rangos = self.__rangos

        for r in range(1,rangos+1):
            exec(
                "d = self.lbR"+str(r)+"D['text']\n"
                "h = self.txtR"+str(r)+"H.get()\n"
                "p = self.txtR"+str(r)+"P.get()\n"
                "info.append([d,h,p])"
            )
        
        info.append([self.lbRLastD['text'],'final',self.txtRLastP.get()])
        return info        


    def __cbWriting(self,e=None):

        value = self.cbTarifas.get()
        if value in self.__tarifas:
            self.__udRangos()
            if self.__newTarifa: self.__setNewTarifaOff()                
            return
        
        if not self.__newTarifa: self.__setNewTarifaOn()            


    def __setNewTarifaOn(self):

        if self.__newTarifa:
            return

        self.__newTarifa = True
        self.btnRegistrar.configure(state='normal')
        self.btnActualizar.configure(state='disable')
        self.btnEliminar.configure(state='disable')


    def __setNewTarifaOff(self):

        if not self.__newTarifa:
            return

        self.__newTarifa = False
        self.btnRegistrar.configure(state='disable')
        self.btnActualizar.configure(state='normal')
        self.btnEliminar.configure(state='normal')


    def __udCbTarifas(self,udRangos=True):

        last_value = self.cbTarifas.get()
        if self.__tarifas is not None and len(self.__tarifas) != 0:
            cb_values = list(self.__tarifas)[::-1]
        else:
            cb_values = ['']

        self.cbTarifas.configure(values=cb_values)
        self.__setCbWidth()
        if last_value is not None and last_value != '' and last_value in cb_values:
            self.cbTarifas.set(last_value)
        else:
            self.cbTarifas.current(0)
            if udRangos:
                self.__cbWriting()


    def __initRangos(self):

        self.lbR1D = tk.Label(self.fRangosA,text='0',bg='#CCCCCC',font=setFont('txt'),width=6)
        self.lbR1D.grid(row=1,column=0,pady=5,padx=5)

        self.txtR1H = tk.Entry(self.fRangosA,bg='#CCCCCC',font=setFont('txt'),width=6,justify=tk.CENTER)
        self.txtR1H.grid(row=1,column=1,pady=5,padx=5)
        self.txtR1H.bind('<KeyRelease>',self.setNextDesde)
        self.txtR1H.frame = 'A'

        self.txtR1P = tk.Entry(self.fRangosA,bg='#CCCCCC',font=setFont('txt'),width=6,justify=tk.CENTER)
        self.txtR1P.grid(row=1,column=2,pady=5,padx=5)

        self.__setLastR()


    def __createRango(self,frame,row):

        exec(
            "self.lbR"+str(self.__rangos)+"D = tk.Label(self.fRangos"+frame+",bg='#CCCCCC',font=setFont('txt'),width=6)\n"
            "self.lbR"+str(self.__rangos)+"D.grid(row="+str(row)+",column=0,pady=5,padx=5)\n"

            "self.txtR"+str(self.__rangos)+"H = tk.Entry(self.fRangos"+frame+",bg='#CCCCCC',font=setFont('txt'),width=6,justify=tk.CENTER)\n"
            "self.txtR"+str(self.__rangos)+"H.grid(row="+str(row)+",column=1,pady=5,padx=5)\n"
            "self.txtR"+str(self.__rangos)+"H.bind('<KeyRelease>',self.setNextDesde)\n"
            "self.txtR"+str(self.__rangos)+"H.frame = '"+frame+"'\n"

            "self.txtR"+str(self.__rangos)+"P = tk.Entry(self.fRangos"+frame+",bg='#CCCCCC',font=setFont('txt'),width=6,justify=tk.CENTER)\n"
            "self.txtR"+str(self.__rangos)+"P.grid(row="+str(row)+",column=2,pady=5,padx=5)"
        )


    def __destroyRango(self):

        exec(
            "self.lbR"+str(self.__rangos)+"D.destroy()\n"
            "self.txtR"+str(self.__rangos)+"H.destroy()\n"
            "self.txtR"+str(self.__rangos)+"P.destroy()"
        )


    def __btnMasClicked(self):

        self.__mas()
        self.__resetDesde()


    def __btnMenosClicked(self):

        self.__menos()
        self.__resetDesde()


    def __menos(self):

        if self.__rangos == 1:
            return
        self.__destroyRango()
        if self.__rangos == 10:
            self.__clearFrameC()
            self.__Right2Left()
        self.__rangos -= 1


    def __mas(self):

        self.__rangos += 1
        if self.__rangos < 11:
            frame = 'A'
            row = self.__rangos
            if self.__rangos == 10:
                self.__initFrameC()
                self.__Left2Right()
        else:
            if self.__rangos == 20:
                self.__rangos -= 1
                return
            frame = 'C'
            row = self.__rangos - 10
        self.__createRango(frame,row)


    def setNextDesde(self,e):

        txt = e.widget
        try:
            valor = int(txt.get()) + 1
        except:
            return
        row = txt.grid_info()['row']
        frame = txt.frame
        if frame == 'C':
            row += 10
        if self.__rangos == row:
            self.lbRLastD.configure(text=str(valor))
        else:
            exec(
                "self.lbR"+str(row+1)+"D.configure(text='"+str(valor)+"')"
            )


    def __udRangos(self,e=None):

        tarifa = self.cbTarifas.get()
        if tarifa is None or tarifa == '' or tarifa not in self.__tarifas:
            return

        rangos = self.__tarifas[tarifa]

        if len(rangos) == 0 or rangos is None:
            return

        if len(rangos) > self.__rangos:
            for r in range((len(rangos)-1)-self.__rangos): self.__mas()                
        if len(rangos) < self.__rangos:
            for r in range(self.__rangos-(len(rangos)-1)): self.__menos()

        self.__cleanRangos()

        for r in rangos[:-1]:
            exec(
                "self.lbR"+str(rangos.index(r)+1)+"D.configure(text='"+r[0]+"')\n"
                "self.txtR"+str(rangos.index(r)+1)+"H.insert(0,'"+r[1]+"')\n"
                "self.txtR"+str(rangos.index(r)+1)+"P.insert(0,"+r[2]+")"
            )

        self.lbRLastD.configure(text=rangos[-1][0])
        self.txtRLastP.insert(0,rangos[-1][2])        


    def __cleanRangos(self):

        for r in range(1,self.__rangos+1):
            exec(
                "self.lbR"+str(r)+"D.configure(text=\'\')\n"
                "self.txtR"+str(r)+"H.delete(0,tk.END)\n"
                "self.txtR"+str(r)+"P.delete(0,tk.END)"
            )
        self.lbR1D.configure(text='0')
        self.lbRLastD.configure(text='')
        self.txtRLastP.delete(0,tk.END)


    def __contraerLimpiar(self):

        if self.__rangos > 1:
            for r in range(self.__rangos): self.__menos()
        self.__cleanRangos()


    def __setCbWidth(self):

        valores = self.cbTarifas['values']
        if valores is None or len(valores) == 0:
            return
        maxi = 0
        for valor in valores:
            if len(valor) > maxi:
                maxi = len(valor)
        self.cbTarifas.configure(width=(maxi+2))


    def __getTarifasBD(self):

        try:
            cn = Conexion()
            q = cn.cursor.execute("SELECT * FROM tarifas")
            rows = q.fetchall()
            #print(rows)            
            cn.desconectar()
        except:
            print('No se pudo acceder a la BD.')
            return

        tarifas_dic = {}
        for row in rows:
            tarifas_dic[row[0]] = list(map(lambda x:x.split('-'),list(row[1].split(',')))) 

        return tarifas_dic


    def __resetDesde(self):

        rangos = self.__rangos

        for r in range(1,rangos+1):
            exec(
                "valor = self.txtR"+str(r)+"H.get()\n"

                "if r == rangos:\n"
                "   try:\n"
                "       self.lbRLastD.configure(text=str(int(valor)+1))\n"
                "   except:\n"
                "       self.lbRLastD.configure(text='')\n"
                
                "if r < rangos:\n"
                "   try:\n"
                "       self.lbR"+str(r+1)+"D.configure(text=str(int(valor)+1))\n"
                "   except:\n"
                "       self.lbR"+str(r+1)+"D.configure(text='')\n"
            )



if __name__ == '__main__':

    root = tk.Tk()
    app = F_tarifas(root)
    app.mainloop()