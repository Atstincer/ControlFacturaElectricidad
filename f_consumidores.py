import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showerror, showinfo, askyesno
from util import setFont
from conexion import Conexion


class F_consumidores(tk.Frame):


    def __init__(self,master,fp=None,consumidores=None):

        super().__init__(master,bg='#202124')
        self.master = master # notebook
        self.fp = fp         # frame padre
        self.__consumidores = consumidores
        self.pack()
        self.__initVariables()
        self.__initFrames()
        self.__initComponents()


    def __initVariables(self):

        self.__textBtnMain = tk.StringVar()
        self.__textBtnMain.set('Registrar')
        self.__imgGoBack = tk.PhotoImage(file=r'.\images\go_back.png').subsample(2)
        self.__udModeOn = False


    def __initFrames(self):

        self.fOperaciones = tk.Frame(self,bg='#202124')
        self.fOperaciones.pack(pady=5,padx=5,fill=tk.X)

        self.fOperaDatos = tk.Frame(self.fOperaciones,bg='#202124') # textboxes
        self.fOperaDatos.pack(side=tk.LEFT,padx=(0,5))

        self.fBtns1 = tk.Frame(self.fOperaciones,bg='#202124')
        self.fBtns1.pack(side=tk.LEFT,fill=tk.Y)

        self.fBtns2 = tk.Frame(self.fOperaciones,bg='#202124')
        self.fBtns2.pack(side=tk.LEFT,expand=True,fill=tk.BOTH,padx=(5,0),pady=(5,0))

        self.ftv = tk.Frame(self,bg='#202124')
        self.ftv.pack()


    def __initComponents(self):

        tk.Label(self.fOperaDatos,text='ID',bg='#202124',fg='#6A98D8').grid(row=0,column=0,padx=5,pady=(10,0),sticky=tk.W)
        self.txtId = tk.Entry(self.fOperaDatos,bg='#CCCCCC',width=15,font=setFont('txt'))
        self.txtId.grid(row=1,column=0,padx=5,pady=(0,10))

        tk.Label(self.fOperaDatos,text='Sucursal',bg='#202124',fg='#6A98D8').grid(row=0,column=1,padx=5,pady=(10,0),sticky=tk.W)
        self.txtSucursal = tk.Entry(self.fOperaDatos,bg='#CCCCCC',width=8,font=setFont('txt'))
        self.txtSucursal.grid(row=1,column=1,padx=5,pady=(0,10))

        tk.Label(self.fOperaDatos,text='Ruta',bg='#202124',fg='#6A98D8').grid(row=0,column=2,padx=5,pady=(10,0),sticky=tk.W)
        self.txtRuta = tk.Entry(self.fOperaDatos,bg='#CCCCCC',width=3,font=setFont('txt'))
        self.txtRuta.grid(row=1,column=2,padx=5,pady=(0,10))

        tk.Label(self.fOperaDatos,text='Folio',bg='#202124',fg='#6A98D8').grid(row=0,column=3,padx=5,pady=(10,0),sticky=tk.W)
        self.txtFolio = tk.Entry(self.fOperaDatos,bg='#CCCCCC',width=5,font=setFont('txt'))
        self.txtFolio.grid(row=1,column=3,padx=5,pady=(0,10))

        tk.Label(self.fOperaDatos,text='Consumidor',bg='#202124',fg='#6A98D8').grid(row=0,column=4,padx=5,pady=(10,0),sticky=tk.W)
        self.txtNombre = tk.Entry(self.fOperaDatos,bg='#CCCCCC',width=20,font=setFont('txt'))
        self.txtNombre.grid(row=1,column=4,padx=4,pady=(0,10))

        self.btnGoBack = tk.Button(self.fBtns1,image=self.__imgGoBack,bg='#BF6000',activebackground='#BF6000',command=self.__goBack)
        self.btnGoBack.pack(anchor=tk.N,pady=15,padx=(5,0))

        self.btnMain = tk.Button(self.fBtns2,textvariable=self.__textBtnMain,font=setFont('btn'),bg='#BF6000',activebackground='#BF6000',command=self.__btnMainClicked)
        self.btnMain.pack(expand=True,anchor=tk.CENTER)

        self.tv_consumidores = ttk.Treeview(self.ftv,show='headings',selectmode=tk.BROWSE)

        self.tv_consumidores['columns'] = (1,2,3,4,5)
        self.tv_consumidores.column(1,anchor=tk.CENTER,width=150)
        self.tv_consumidores.column(2,anchor=tk.CENTER,width=90)
        self.tv_consumidores.column(3,anchor=tk.CENTER,width=40)
        self.tv_consumidores.column(4,anchor=tk.CENTER,width=70)
        self.tv_consumidores.column(5,anchor=tk.CENTER,width=350)

        self.tv_consumidores.heading(1,text='ID')
        self.tv_consumidores.heading(2,text='Sucursal')
        self.tv_consumidores.heading(3,text='Ruta')
        self.tv_consumidores.heading(4,text='Folio')
        self.tv_consumidores.heading(5,text='Consumidor')

        self.__setTV()

        self.tv_consumidores.pack(pady=(0,5),padx=5)
        #self.tv_consumidores.bind('<<TreeviewSelect>>',self.__tvOnSelected)
        self.tv_consumidores.bind('<Double-1>',self.__tvOnDblClick)
        self.tv_consumidores.tag_configure('consumidor',background='#202124',foreground='#6A98D8')

        self.__txts = [
            self.txtId,
            self.txtSucursal,
            self.txtRuta,
            self.txtFolio,
            self.txtNombre
        ]


    def __btnMainClicked(self):

        info = self.__getInfo()

        if not self.__validarInfo(info) or not self.__validarConsumidor(info):
            return

        if self.__udModeOn:
            if info[0] != self.__idC2UD:
                choise = askyesno('Atención','Está intentando modificar el Id de este consumidor.\nDesea continuar así?')
                if choise:
                    query = "UPDATE consumidores SET id='{}',nombre='{}', sucursal='{}',ruta='{}',folio='{}' WHERE id='{}'".format(info[0],info[4],info[1],info[2],info[3],self.__idC2UD)
                else:
                    return
            else:
                query = "UPDATE consumidores SET nombre='{}', sucursal='{}',ruta='{}',folio='{}' WHERE id='{}'".format(info[4],info[1],info[2],info[3],self.__idC2UD)
            opera = 'Actualizado'
        else:
            query = "INSERT INTO consumidores (id,nombre,sucursal,ruta,folio) VALUES ('{}','{}','{}','{}','{}')".format(info[0],info[4],info[1],info[2],info[3])
            opera = 'Registrado'

        try:
            cn = Conexion()
            cn.cursor.execute(query)
            cn.cursor.commit()
            cn.desconectar()
        except:
            showerror('Atención','No se pudo realizar la operación. Tuvimos\nproblema al intentar acceder a la BD.')
            return

        if self.__udModeOn:
            self.__setRegularMode

        self.__cleanTxts()
        self.fp.udConsumidores()
        
        showinfo('Información',f'{opera} correctamente.')


    def udConsumidores(self,consumidores):

        self.__consumidores = consumidores
        self.__udTV()


    def __udTV(self):

        self.__cleanTV()
        self.__setTV()


    def __cleanTV(self):

        items = self.tv_consumidores.get_children()
        if items is not None and len(items) != 0:
            for item in items: self.tv_consumidores.delete(item)


    def __validarConsumidor(self,info):

        if info is None or len(info) == 0:
            return

        rows = self.__findConsumidor(info)
    
        if len(rows) == 0:
            return True

        if self.__udModeOn:
            if len(rows) == 1:
                if rows[0][0] == self.__idC2UD:
                    return True
        
        showerror('Atención',f'No se puede realizar la operación. Ya existe otro\nregistro en sistema con el mismo Id-{info[0]}.')
        return False


    def __findConsumidor(self,info):

        found = []
        for consumidor in self.__consumidores:
            if info[0] == consumidor[0]:
                found.append(consumidor)
        return found


    def __validarInfo(self,info):

        if info is None or len(info) == 0:
            return

        if info[0] == '' or info[4] == '':
            showerror('Atención','Debe introducir al menos "Id" y "Nombre".',master=self.fp.master)
            return False

        try:
            int(info[0])
        except:
            if self.__udModeOn:
                operacion = 'actualizar'
            else:
                operacion = 'registrar'
            choise = askyesno('Atención',f'El "Id" proporcionado no está formado solo por\nnúmeros:\n\n- {info[0]}\n\nDesea {operacion} de todos modos?',master=self.fp.master)
            if not choise:
                return False

        if len(info[0]) != 13 and info[0] != self.__idC2UD:
            choise = askyesno('Atencion',f'El "Id" no contiene la cantidad de caracteres\nhabitual:\n\n- {info[0]}\n\nDesea continuar así?',master=self.fp.master)
            if not choise:
                return False

        return True


    def __getInfo(self):

        info = list(map(lambda x: x.get(),self.__txts))
        return info


    def __tvOnDblClick(self,e):

        item = self.tv_consumidores.selection()
        if item is None:
            return
        values = self.tv_consumidores.item(item,'values')
        self.__showInfo(values)
        self.__setUdMode(values[0])


    def __showInfo(self,info):

        if info is None or len(info) == 0:
            return
        self.__cleanTxts()
        for i in range(len(info)): self.__txts[i].insert(0,info[i])


    def __cleanTxts(self):

        for txt in self.__txts: txt.delete(0,tk.END)


    def __setTV(self):

        if self.__consumidores is None or len(self.__consumidores) < 1:
            return

        for consumidor in self.__consumidores:
            self.tv_consumidores.insert('','end',iid=consumidor[0],values=(consumidor[0],consumidor[2],consumidor[3],consumidor[4],consumidor[1]),tags=['consumidor',])

        self.tv_consumidores.configure(height=len(self.__consumidores))


    def __setUdMode(self,idC2UD):

        if self.__udModeOn:
            self.__idC2UD = idC2UD
            return
        self.__udModeOn = True
        self.__idC2UD = idC2UD
        self.__udBtns()


    def __udBtns(self):

        if self.__udModeOn:
            self.__textBtnMain.set('Actualizar')
            self.btnEliminar = tk.Button(self.fBtns2,text='Eliminar',font=setFont('btn'),width=7,bg='#BF6000',activebackground='#BF6000',command=self.__eliminar)
            self.btnEliminar.pack(pady=5)
        else:
            self.__textBtnMain.set('Registrar')
            #self.btnGoBack.destroy()
            self.btnEliminar.destroy()


    def __eliminar(self):

        choise = askyesno('Confirmación',f'Seguro que desea eliminar el consumidor "{self.__idC2UD}"\ny todas sus lecturas registradas en sistema?')

        if not choise:
            return

        try:
            cn = Conexion()
            cn.cursor.execute("DELETE * FROM consumidores WHERE id='{}'".format(self.__idC2UD))
            cn.cursor.commit()
            cn.desconectar()
        except:
            showerror('Atención','No se pudo realizar la operación. Tuvimos\nproblema al intentar acceder a la BD')
            return

        self.__setRegularMode
        self.__cleanTxts()
        self.fp.udConsumidores()
        showinfo('Información','Registro eliminado correctamente.')


    def __setRegularMode(self):

        if not self.__udModeOn:
            return
        self.__udModeOn = False
        self.__udBtns()


    def __goBack(self):

        self.__cleanTxts()
        if self.__udModeOn:
            self.__setRegularMode()


if __name__ == '__main__':

    root = tk.Tk()
    app = F_consumidores(root)
    app.mainloop()