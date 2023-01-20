import tkinter as tk
from logica import getCalculo
from util import setFont, placev


class F_calculo(tk.Frame):


    def __init__(self,master,fp=None,info=None,ventana=True):

        super().__init__(master,bg='#202124')
        self.master = master
        self.fp = fp
        self.tarifa = info[2]
        if ventana == True:
            self.master.geometry(placev(self.master,450,550,1)) #'450x550'
            self.master.resizable(0,0)
            self.master.title('Consumo de electricidad')
        self.pack(expand=True,fill=tk.BOTH)
        self.initVariables()
        self.initFrames()
        self.initComponents()
        self.__initValues(info)


    def initVariables(self):

        self.result = tk.StringVar()
        self.result.set('Ingrese las lecturas correspondientes.')


    def initFrames(self):

        self.lbframe = tk.LabelFrame(self,text='CALCULO SEGUN LECTURAS',bg='#202124',fg='#C185EE',font=setFont('title'))
        self.lbframe.pack(fill=tk.X,pady=(15,10))

        self.frame1 = tk.Frame(self.lbframe,bg='#202124')
        self.frame1.pack(side=tk.LEFT)

        self.frame2 = tk.Frame(self.lbframe,bg='#202124')
        self.frame2.pack(side=tk.RIGHT)

        self.frameResult = tk.Frame(self,bg='#202124')
        self.frameResult.pack(expand=True,fill=tk.BOTH)


    def initComponents(self):

        tk.Label(self.frame1,text='anterior',bg='#202124',fg='#6A98D8').grid(row=0,column=0,padx=(10,5),pady=(10,5))
        tk.Label(self.frame1,text='actual',bg='#202124',fg='#6A98D8').grid(row=1,column=0,padx=(5,10),pady=(5,10))

        self.txt_anterior = tk.Entry(self.frame1,width=10,font=setFont('txt'),bg='#CCCCCC')
        self.txt_anterior.grid(row=0,column=1)
        self.txt_anterior.bind('<Return>',self.calcular)
        self.txt_anterior.focus_set()
        self.txt_actual = tk.Entry(self.frame1,width=10,font=setFont('txt'),bg='#CCCCCC')
        self.txt_actual.grid(row=1,column=1)
        self.txt_actual.bind('<Return>',self.calcular)

        self.btn = tk.Button(self.frame2,text='CALCULAR',font=setFont('btn'),bg='#BF6000',activebackground='#BF6000',command=self.calcular)
        self.btn.pack(padx=20)

        tk.Label(self.frameResult,textvariable=self.result,justify=tk.LEFT,bg='#202124',fg='#6A98D8').pack(padx=10,pady=10)


    def __initValues(self,info=None):

        if info == None:
            return

        self.updateFrame(info,calcular=True)


    def calcular(self,event=None):

        lect_anterior = self.txt_anterior.get()
        lect_actual = self.txt_actual.get()

        if self.validar(lect_anterior,lect_actual):
            resultado = getCalculo([int(lect_anterior),int(lect_actual),'',''],solo_cadena=True,tarifa=self.tarifa)
        else:
            resultado = 'Datos incorrectos.'
        self.result.set(resultado)


    def validar(self,x,y):

        if x == '' or y == '':
            return False
                
        try:
            if int(x) > int(y):
                return False
        except:
            return False

        return True


    def updateFrame(self,info,cadena=None,calcular=False):

        self.__clean()
        self.txt_anterior.insert(0,info[0])
        self.txt_actual.insert(0,info[1])
        if cadena is not None:
            self.result.set(cadena)
        if calcular:
            self.calcular()


    def __clean(self):

        self.txt_anterior.delete(0,tk.END)
        self.txt_actual.delete(0,tk.END)