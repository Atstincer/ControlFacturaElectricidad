import matplotlib.pyplot as plt
#plt.style.use('ggplot')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.ticker import MultipleLocator
import tkinter as tk
from tkinter import ttk
from conexion import Conexion


class F_graficas(tk.Frame):


    def __init__(self,master,fp=None):

        super().__init__(master,bg='#202124')
        self.__master = master
        self.__fp = fp
        self.pack()
        self.__initComponents()
        self.__setCanvas()
        self.__cbSelected()


    def __initComponents(self):

        self.cbAgnos = ttk.Combobox(self,state='readonly',width=5,font=('helvetica','11','bold'))
        self.cbAgnos.pack(anchor=tk.E,padx=5,pady=5)
        self.cbAgnos.bind('<<ComboboxSelected>>',self.__cbSelected)
        self.__udCbAgnos()

        self.fgraficos = tk.Frame(self,bg='red')
        self.fgraficos.pack(expand=True,fill=tk.BOTH,padx=5,pady=5)


    def __cbSelected(self,e=None,new_consumidor=False):

        if self.cbAgnos.get() == '':
            self.__drawGrafico()
        elif self.cbAgnos.get() != 'Todos':
            meses_list, kwTotal_list = self.__getMesesKwsForGrafico()
            title = f'Consumo por meses ({self.cbAgnos.get()})'
            self.__drawGrafico(meses_list,kwTotal_list,title)
            if not new_consumidor:
                self.__fp.refreshRegistrFrame(self.cbAgnos.get())
        elif self.cbAgnos.get() == 'Todos':
            agnos_list, kwPromedio_list = self.__fp.getInfo(kwAgno_promedio=True)
            title = 'Consumo promedio por años'
            self.__drawGrafico(agnos_list,kwPromedio_list,title)
        

    def __drawGrafico(self,x=None,y=None,title=None):

        if x is None or y is None:
            x = ['Ene','Feb','Mar','Abr','May','Jun','Jul','Ago','Sep','Oct','Nov','Dic']
            y = list(0 for mes in x)
            title = ''

        self.ax.clear()
        self.ax.set_title(title,fontsize=18,fontweight='bold',color='#C185EE')
        self.ax.set_ylabel('Kws',fontsize=12,fontweight='bold',color='#6A98D8')
        self.ax.bar(x,y,width=0.5,color='#BF6000',edgecolor='#C185EE')
        self.ax.yaxis.set_major_locator(MultipleLocator(25))
        self.ax.yaxis.set_minor_locator(MultipleLocator(5))
        self.ax.grid(which='major',axis='y',alpha=0.2,color='red',linestyle='-.',linewidth=1.5)
        self.ax.grid(which='minor',axis='y',alpha=0.2,color='red',linestyle='dotted')
        self.ax.set_facecolor('#CCCCCC') # '#C185EE'
        self.ax.spines['bottom'].set_color('#6A98D8')
        self.ax.spines['left'].set_color('#6A98D8')
        self.ax.tick_params(axis='x',colors='#6A98D8',which='both')
        self.ax.tick_params(axis='y',colors='#6A98D8',which='both')
        self.ax.yaxis.label.set_color('#6A98D8')
        self.canvas.draw()


    def refreshFrame(self,agno=None):

        if agno is not None:
            self.cbAgnos.set(agno)
        else:
            agno_actual = self.cbAgnos.get()
            self.__udCbAgnos()
            if agno_actual in self.cbAgnos['values']:
                self.cbAgnos.set(agno_actual)
        self.__cbSelected()


    def setNewConsumidor(self):

        self.__udCbAgnos()
        self.__cbSelected(new_consumidor=True)


    def __udCbAgnos(self):

        agnos = self.__fp.getInfo(solo_agnos=True)
        if agnos is None or len(agnos) == 0:
            agnos = ['']
        else:
            agnos.insert(0,'Todos')
        self.cbAgnos.configure(values=agnos)
        self.cbAgnos.current(0)
        self.__setCbWidth()


    def __setCbWidth(self):

        values = self.cbAgnos['values']
        maxi = 0
        for v in values:
            if len(v) > maxi: maxi = len(v)
        if maxi == 0:
            return
        self.cbAgnos.configure(width=(maxi+2))


    def __setCanvas(self):

        self.figure = plt.Figure(figsize=(5,4), dpi=80, facecolor='#202124') # ,edgecolor='red' ,linewidth=5
        #self.figure, self.ax = plt.subplots(1,2)
        #self.figure.set_size_inches(5,4)
        #self.figure.set_facecolor('LightSalmon')
        #self.figure.set_edgecolor('red')
        
        self.ax = self.figure.add_subplot()
        self.canvas = FigureCanvasTkAgg(self.figure, self.fgraficos)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH,expand=1)
        

    def __getMesesKwsForGrafico(self):

        meses_dic = {
            '01':'Ene',
            '02':'Feb',
            '03':'Mar',
            '04':'Abr',
            '05':'May',
            '06':'Jun',
            '07':'Jul',
            '08':'Ago',
            '09':'Sep',
            '10':'Oct',
            '11':'Nov',
            '12':'Dic'
        }

        lecturas = self.__fp.getInfo(agno=self.cbAgnos.get())
        
        if lecturas is None or len(lecturas) == 0:
            print('No se encontraron lecturas.')
            return None,None

        meses_str = []
        kwTotal = []
        
        for lectura in lecturas[::-1]:
            meses_str.append(meses_dic[lectura[4]])
            kwTotal.append(lectura[9])           

        for k,v in meses_dic.items():
            if v not in meses_str:
                meses_str.insert(int(k)-1,v)
                kwTotal.insert(int(k)-1,0)

        return meses_str, kwTotal


'''
    def __getLecturas(self,solo_agnos=False,agno=None,reverse=False):

        cliente = self.__fp.getIdConsumidor()
        cn = Conexion()
        if solo_agnos:
            query = f"SELECT agno_factura FROM lecturas WHERE cliente = '{cliente}'"
        elif agno is not None:
            query = f"SELECT * FROM lecturas WHERE agno_factura = '{agno}' AND cliente = '{cliente}'"
        else:
            return

        q = cn.cursor.execute(query)
        rows = q.fetchall()

        if solo_agnos:
            result = []
            for i in rows:
                if i[0] not in result:
                    result.append(i[0])
            result.sort(reverse=reverse)
        elif agno is not None:
            result = sorted(rows,key=lambda x:x[4])

        cn.desconectar()
        return result
'''


if __name__ == '__main__':

    root = tk.Tk()
    app = F_graficas(root)
    app.mainloop()