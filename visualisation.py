from tkinter import*
from packInter.fonctionplot import*#packInter.
from PIL import ImageTk, Image
from datetime import datetime
from tkinter import messagebox
import os
#
import tkinter.ttk as ttk
import random
from tkinter import filedialog 
import time
from scipy.io import netcdf
import numpy as np
import matplotlib

import pandas as pd # import libraries
import netCDF4 # import libraries
from netCDF4 import Dataset
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from cdo import *
from matplotlib import gridspec

import subprocess
from packInter.scrollableimage import ScrollableImage#packInter.
from packInter.PLotcities import TimeSeries,plot_map_contry#packInter.
from packInter.PLotcities import TimeSeriesT
#from packInter.plotvar import Plotvar
#from packInter.map_projection import Map_projection
#from packInter import packInter/fspays
#from showplt import SHOWPLT
#from packInter.nCL_color_1 import NCL_color_1
#from packInter.rain import Rain
#from packInter.win import Win
import pandas as pd
import shapefile as shp
import seaborn as sns
import tkinter
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
import Ngl
import numpy as np
#from extensive import Temperature
from packInter.precipitation import PrecipitationNCL,TemperatureNCL##packInter.
from packInter.TRANS_panel import Panelmanager#packInter.

class VISUALISATION(object): 
    def __init__(self,conteneur,DataForPlot,SELVARL,SELAREAL,masque,GETRefNBRE,step):
        self.conteneur=conteneur
        self.DataForPlot=DataForPlot
        self.SELVARL=SELVARL
        self.SELAREAL=SELAREAL
        self.masque=masque
        self.GETRefNBRE=GETRefNBRE
        self.step=step
        self.Visualization()
        self.btnUpdtePresend=0#detector for 
        #Enddate
    def movl(self,a):
        a.place_forget()
        return
    #def RESET(self):
        #self.Framevisualisatio.destroy
        #self.Visualization()
        #if self.btnUpdtePresend==1:
            #self.btnUpdte.destroy
        return
    def Visualization(self):
        self.List_Idsf=[]
        self.List_Idsf1plot=[]
        self.List_sfLocality=[]
        self.List_sfLocality1plot=[]
        self.List_nameAdmi=[]
        self.List_nameAdmi1plot=[]

        #self.tmax()
         #frame de Visualisation
        self.Framevisualisatio =self.conteneur# LabelFrame(self.conteneur, bg='#ffffff',text='Visualization',font=("Arial", 13))
        #self.Framevisualisatio.place(relx=0.0, rely=0.0,relwidth=1,relheight=0.97)
        #frame de choix des plot
        self.Framevisualisation = LabelFrame(self.Framevisualisatio, bg='#ffffff')#,text='specification',font=("Arial", 13))
        self.Framevisualisation.place(relx=0.0001, rely=0.0,relwidth=1,relheight=0.15)
        #frame d'afficage
        self.Frameplt= Frame(self.Framevisualisatio, bg='#000000')
        self.Frameplt.place(relx=0.01, rely=0.155,relwidth=0.98,relheight=0.77)
        ###parameter xy


        
     
        Button(self.Framevisualisatio, text="Close",padx=0.5, pady=0.1,bg="#ffffff",command=self.Framevisualisatio.destroy,font=("Arial", 13),activebackground="#606666").place(relx=0.9,rely=0.93 ,relwidth=0.08,relheight=0.06)
        
        #Button(self.Framevisualisatio, text="Run",padx=0.5, pady=0.1,bg="#ffffff",command=None,font=("Arial", 13)).place(relx=0.6,rely=0.93 ,relwidth=0.13,relheight=0.06)
        
        Button(self.Framevisualisatio, text="Next Step",padx=0.5, pady=0.1,bg="#ffffff",command=self.NEXTSTEPMAP,font=("Arial", 13),activebackground="#606666").place(relx=0.81,rely=0.93 ,relwidth=0.09,relheight=0.06)
        
        Button(self.Framevisualisatio, text="Previous Step",padx=0.5, pady=0.1,bg="#ffffff",command=self.PREVIOUSSTEPMAP,font=("Arial", 13),activebackground="#606666").place(relx=0.699,rely=0.93 ,relwidth=0.115,relheight=0.06)
        ############# #606666
        


        
        
        ####TIME STEP
        cdo=Cdo()
        B=cdo.showdate(input=self.DataForPlot)
        LLab= B[0].replace(" ", "")#.replace(" ", " ")
        self.datatimestp=[LLab[x:x+10] for x in range(0,len(LLab),10)]
        j=0
        self.dicoTimeStep={}
        for i in self.datatimestp:
            self.dicoTimeStep.update({i:j})#dicoTimeStep is the dictionary stp:value example,2020-07-27:1
            j+=1
        #####END TIME STEP    
        ##################
        
        self.ListtypeOfmap={'map':['Single map','Panel','map3'],'xy':['histogram','boxplot','Time Series Spatial','Time Series Tempoaral','barchart'],'contour':['contour1','contour2','contour2']}
        
        self.fonctionDico={'Single map':TemperatureNCL,'Panel':Panelmanager,'map3':fontmap3,'histogram':fonthist,'boxplot':fontboxplot,'Time Series Spatial':TimeSeries,'Time Series Tempoaral':TimeSeriesT,'barchart':fonbar,'contour1':fontcontour1,'contour2':fontcontour2}
        ###var
        self.xvisual=0.01
        self.yvisual=0.1
        self.pas=0.2
        self.pasy=0.5
        #TYPE OF Visualization
        self.TypeOfplot=Label(self.Framevisualisation, text ='Variable ',font=("Arial", 13))
        self.TypeOfplot.place(relx=self.xvisual, rely=self.yvisual,relwidth=0.07,relheight=0.38)

        self.varselected = StringVar()
        self.varselected.set(self.SELVARL[0])

        comboboxA=ttk.Combobox(self.Framevisualisation,textvariable=self.varselected,values=self.SELVARL,font=("Arial"))
        comboboxA.bind("<<ComboboxSelected>>",self.Callvar)
        comboboxA.place(relx=self.xvisual, rely=self.yvisual+self.pasy,relwidth=0.07,relheight=0.3)
        
        ####type
        self.xvisual=self.xvisual+self.pas-0.09
        self.pasy=0.5
       
        self.subTypeOfplot=Label(self.Framevisualisation, text ='types of Plot ',font=("Arial", 13))
        self.subTypeOfplot.place(relx=self.xvisual-0.03, rely=self.yvisual,relwidth=0.07,relheight=0.38)
        
        self.Typemap=StringVar()
        self.Typemap.set('Type Visualization')#stp = StringVar()
        #stp.set('Type Visualization')

        comboboxB=ttk.Combobox(self.Framevisualisation,textvariable=self.Typemap,values=[*self.ListtypeOfmap.keys()],font=("Arial"))
        comboboxB.bind("<<ComboboxSelected>>",self.CallTypeOfMap)
        comboboxB.place(relx=self.xvisual-0.03, rely=self.yvisual+self.pasy,relwidth=0.07,relheight=0.3)
        
        
    def Callvar(self,*args):
        self.varselectedget = self.varselected.get()
        Label(self.Framevisualisatio, text =f'Variable: {self.varselectedget} ',font=("Arial", 16)).place(relx=0, rely=0.93,relwidth=0.68,relheight=0.06)
        
    def CallTypeOfMap(self,even):
        self.xvisual=0.229
        self.pasy=0.5

        #Subtypes
        self.Subtypesplot=Label(self.Framevisualisation, text ='Subtypes of plot',font=("Arial", 13))
        self.Subtypesplot.place(relx=self.xvisual-0.06, rely=self.yvisual,relwidth=0.07,relheight=0.38)

        self.datab=self.ListtypeOfmap.get(self.Typemap.get())
        self.strvartypeMap=StringVar()

        self.strvartypeMap.set(self.datab[0])

        comboboxC=ttk.Combobox(self.Framevisualisation,textvariable=self.strvartypeMap,values=self.datab,font=("Arial"))
        comboboxC.bind("<<ComboboxSelected>>",self.CallTypesubOfMap)
        comboboxC.place(relx=self.xvisual-0.06, rely=self.yvisual+self.pasy,relwidth=0.07,relheight=0.3)
        
        self.typeget=self.Typemap.get()
        self.geteur=0 #permet de savoir si un element a ete place sur la fenetre ou non geteur=1 pr xy,
        #geteur=2 pr map
        self.geteurcalladmi=0
        self.geteursubadmi=0
        if self.typeget=='xy':
            #if self.geteur==2:
                #movl(comboboxstepmap)
            self.geteur=1
            self.xvisual=0.337
            self.pasy=0.5

            #Subtypes
            self.AdmiForplot=Label(self.Framevisualisation, text ='Admi ',font=("Arial", 13))
            self.AdmiForplot.place(relx=self.xvisual-0.09, rely=self.yvisual,relwidth=0.07,relheight=0.38)
            
            ##admi0    
            self.databrutadmi0={"Angola":'packInter/fspays/AGO_adm/AGO_adm0.shp',"Cameroon":"packInter/fspays/CMR_adm/CMR_adm0.shp","Republic of Congo":'packInter/fspays/COG_adm/COG_adm0.shp',"Gabon":'packInter/fspays/GAB_adm/GAB_adm0.shp',"Equatorial Guinea":'packInter/fspays/GNQ_adm/GNQ_adm0.shp',"Central African Republic":1,"Democratic Republic of Congo":'packInter/fspays/COD_adm/COD_adm0.shp',"Rwanda":'packInter/fspays/RWA_adm/RWA_adm0.shp',"Burundi":'packInter/fspays/BDI_adm/BDI_adm0.shp',"Sao Tome and Principe":"packInter/fspays/STP_adm/STP_adm0.shp","Chad":'packInter/fspays/TCD_adm/TCD_adm0.shp',"ECCAS":1,"CEMAC":1,"Other Area":1}#dictionary keys=contry, value=shapefile admi1
            self.shp_pathadmi0=self.databrutadmi0[self.masque]
            sfadmi0= shp.Reader(self.shp_pathadmi0).records()
            self.dicoAdmi0=plot_map_contry(self.shp_pathadmi0)
            self.nameIdAdmi0=plot_map_contry(self.shp_pathadmi0)
            ##admi1
            self.databrutadmi1={"Angola":'packInter/fspays/AGO_adm/AGO_adm1.shp',"Cameroon":"packInter/fspays/CMR_adm/CMR_adm1.shp","Republic of Congo":'packInter/fspays/COG_adm/COG_adm1.shp',"Gabon":'packInter/fspays/GAB_adm/GAB_adm1.shp',"Equatorial Guinea":'packInter/fspays/GNQ_adm/GNQ_adm1.shp',"Central African Republic":1,"Democratic Republic of Congo":'packInter/fspays/COD_adm/COD_adm1.shp',"Rwanda":'packInter/fspays/RWA_adm/RWA_adm1.shp',"Burundi":'packInter/fspays/BDI_adm/BDI_adm1.shp',"Sao Tome and Principe":'packInter/fspays/STP_adm/STP_adm1.shp',"Chad":'packInter/fspays/TCD_adm/TCD_adm1.shp',"ECCAS":1,"CEMAC":1,"Other Area":1}#dictionary keys=contry, value=shapefile admi1
            self.shp_pathadmi1=self.databrutadmi1[self.masque]
            sfadmi1 = shp.Reader(self.shp_pathadmi1).records()
            self.dicoAdmi1=plot_map_contry(self.shp_pathadmi1)
            self.nameIdAdmi1=plot_map_contry(self.shp_pathadmi1)
            #self.KeysRegionAdmi1=[*self.nameIdAdmi1.keys()]
            #print(f"self.nameIdAdmi1={self.nameIdAdmi1}")
            ###
            ##Admi2
            self.databrutadmi2={"Angola":'packInter/fspays/AGO_adm/AGO_adm0.shp',"Cameroon":"packInter/fspays/CMR_adm/CMR_adm2.shp","Republic of Congo":'packInter/fspays/COG_adm/COG_adm2.shp',"Gabon":'packInter/fspays/GAB_adm/GAB_adm2.shp',"Equatorial Guinea":1,"Central African Republic":1,"Democratic Republic of Congo":'packInter/fspays/COD_adm/COD_adm2.shp',"Rwanda":'packInter/fspays/RWA_adm/RWA_adm2.shp',"Burundi":'packInter/fspays/BDI_adm/BDI_adm2.shp',"Sao Tome and Principe":1,"Chad":'packInter/fspays/TCD_adm/TCD_adm2.shp',"ECCAS":1,"CEMAC":1,"Other Area":1}#dictionary keys=contry, value=shapefile admi1
            self.shp_pathadmi2=self.databrutadmi2[self.masque]
            sfadmi2 = shp.Reader(self.shp_pathadmi2).records()
            self.dicoAdmi2=plot_map_contry(self.shp_pathadmi2)
            self.nameIdAdmi2=plot_map_contry(self.shp_pathadmi2)
            #self.KeysRegionAdmi2=[*self.nameIdAdmi2.keys()]
            ###
            ##Admi3
            self.databrutadmi3={"Angola":'packInter/fspays/AGO_adm/AGO_adm3.shp',"Cameroon":"packInter/fspays/CMR_adm/CMR_adm3.shp","Republic of Congo":1,"Gabon":1,"Equatorial Guinea":1,"Central African Republic":1,"Democratic Republic of Congo":'packInter/fspays/COD_adm/COD_adm3.shp',"Rwanda":'packInter/fspays/RWA_adm/RWA_adm3.shp',"Burundi":'packInter/fspays/BDI_adm/BDI_adm3.shp',"Sao Tome and Principe":1,"Chad":'packInter/fspays/TCD_adm/TCD_adm3.shp',"ECCAS":1,"CEMAC":1,"Other Area":1}#dictionary keys=contry, value=shapefile admi1
            self.shp_pathadmi3=self.databrutadmi3[self.masque]
            sfadmi3 = shp.Reader(self.shp_pathadmi3).records()
            self.dicoAdmi3=plot_map_contry(self.shp_pathadmi3)
            self.nameIdAdmi3=plot_map_contry(self.shp_pathadmi3)
            #self.KeysRegionAdmi3=[*self.nameIdAdmi3.keys()]
            ###
            
            self.dataAdmi={'Admi0':self.dicoAdmi0,'Admi1':self.dicoAdmi1,'Admi2':self.dicoAdmi2,'Admi3':self.dicoAdmi3}
            self.Admi=StringVar()

            self.Admi.set([*self.dataAdmi.keys()][0])

            self.comboboxAdmi=ttk.Combobox(self.Framevisualisation,textvariable=self.Admi,values=[*self.dataAdmi.keys()],font=("Arial"))
            self.comboboxAdmi.bind("<<ComboboxSelected>>",self.Calladmi)
            self.comboboxAdmi.place(relx=self.xvisual-0.09, rely=self.yvisual+self.pasy,relwidth=0.07,relheight=0.3)
#############################################################################################################################################################################
            
            
        if  self.typeget=='map':
                 
            self.xvisual=0.337
            self.pasy=0.5

            #Ptime step
            self.timestepForplot=Label(self.Framevisualisation, text ='Time Steps',font=("Arial", 13))
            self.timestepForplot.place(relx=self.xvisual-0.09, rely=self.yvisual,relwidth=0.07,relheight=0.38)

            
            ListD=self.datatimestp
            self.stpMap = StringVar()
            self.stpMap.set('Please Choose the step')

            comboboxstepmap=ttk.Combobox(self.Framevisualisation,textvariable=self.stpMap,values=self.datatimestp,font=("Arial"))
            comboboxstepmap.bind("<<ComboboxSelected>>",self.callStepMap)
            comboboxstepmap.place(relx=self.xvisual-0.09, rely=self.yvisual+self.pasy,relwidth=0.07,relheight=0.3)
            
            
        return 
    def CallTimestep(self,even):
        self.STEP=self.stpd.get()
        print(self.STEP)
        return
    
    def CallTypesubOfMap(self,even):#for xy
        #step=self.stpMap.get()
        #step=self.dicoTimeStep.get(step, 0)
        self.typeget1=self.strvartypeMap.get()
        if self.typeget1!='Time Series Tempoaral':
            self.xvisual=0.48
            self.pasy=0.5
            self.Labelstartdate=Label(self.Framevisualisation, text ='Start Date',font=("Arial", 13))
            self.Labelstartdate.place(relx=self.xvisual-0.04, \
                rely=self.yvisual,relwidth=0.09,relheight=0.3)
            self.startdate = StringVar()
            self.startdate.set(f"{self.datatimestp[0]}")
            self.comboboxSartdate = ttk.Combobox(self.Framevisualisation,textvariable=self.startdate,value=self.datatimestp,font=("Arial", 13))
            self.comboboxSartdate.bind('<<ComboboxSelected>>', self.callstartdate)
            self.comboboxSartdate.place(relx=self.xvisual-0.04, rely=0.5,relwidth=0.09,relheight=0.3)
            ###End startdate
            ###start date
            self.xvisual=0.59
            self.pasy=0.5
            self.LabelEnddate=Label(self.Framevisualisation, text ='End Date',font=("Arial", 13))
            self.LabelEnddate.place(relx=self.xvisual-0.04, \
                rely=self.yvisual,relwidth=0.09,relheight=0.3)
            self.Enddate = StringVar()
            self.Enddate.set(self.datatimestp[-1])
            self.comboboxEnddate = ttk.Combobox(self.Framevisualisation,textvariable=self.Enddate,value=self.datatimestp,font=("Arial", 13))
            self.comboboxEnddate.bind('<<ComboboxSelected>>', self.callEnddate)
            self.comboboxEnddate.place(relx=self.xvisual-0.04, rely=0.5,relwidth=0.09,relheight=0.3)
            Button(self.Framevisualisation, text="Reset",padx=0.5, pady=0.1,bg="#ffffff",command=self.RESET,font=("Arial", 10)).place(relx=0.71,rely=0.035 ,relwidth=0.1,relheight=0.32)
            self.stateaddfonction=0
            
            self.btnUpdte=Button(self.Framevisualisation, text="View Plot",padx=0.5, pady=0.1,bg="#ffffff",command=self.ViewMultiGraph,font=("Arial", 10)).place(relx=0.71,rely=0.47 ,relwidth=0.1,relheight=0.32) #view plot
            
            self.btnUpdte=Button(self.Framevisualisation, text="Add Curve",padx=0.5, pady=0.1,bg="#ffffff",command=self.StateAdd_fn,font=("Arial", 10)).place(relx=0.83,rely=0.035 ,relwidth=0.1,relheight=0.32) #USE to add plot
        
            Button(self.Framevisualisation, text="Stop Add Curve",padx=0.5, pady=0.1,bg="#ffffff",command=self.StatestopaddCurve_fn,font=("Arial", 10)).place(relx=0.83,rely=0.47 ,relwidth=0.1,relheight=0.32) #USE to add plot
        
        #
        self.stpMap = StringVar()    
        step=self.stpMap.get()
        step=self.dicoTimeStep.get(step, 0)
        self.stepmap=self.dicoTimeStep.get(self.stpMap.get(), 0)
        self.varselectedget = self.varselected.get()
        self.Frameplt.destroy
        self.Frameplt= Frame(self.Framevisualisatio, bg='#000000')
        self.Frameplt.place(relx=0.01, rely=0.155,relwidth=0.98,relheight=0.77)
        #
        b=self.fonctionDico.get(self.strvartypeMap.get())
        print(self.typeget1)
        step=0
        #b(data=self.DataForPlot,var=self.SELVARL,conteneur=self.Frameplt,area=self.SELAREAL,masque=self.masque,step=step)
        if self.typeget1=='Panel':
            b(data=self.DataForPlot,var=self.varselectedget,conteneur=self.Frameplt,area=self.SELAREAL,masque=self.masque,GETRefNBRE=self.GETRefNBRE,SELVARL=self.SELVARL,step=self.stepmap)
            return
        if self.typeget1=='Single map':
            b(data=self.DataForPlot,var=self.varselectedget,conteneur=self.Frameplt,area=self.SELAREAL,masque=self.masque,step=self.stepmap)
        self.frame_selpanel.destroy()
        return

        print("yes")
        return
    def Calladmi(self,even):#for xy
        self.geteurcalladmi=1
        self.typeadmiget=[*self.dataAdmi.get(self.Admi.get()).keys()]
        
        self.xvisual=0.445
        self.pasy=0.5

        #Subtypes
        self.AdmiForplot=Label(self.Framevisualisation, text ='Locality ',font=("Arial", 13))
        self.AdmiForplot.place(relx=self.xvisual-0.12, rely=self.yvisual,relwidth=0.07,relheight=0.38)
  
        self.subadmi=StringVar()

        self.subadmi.set(self.typeadmiget[0])

        self.comboboxsubAdmi=ttk.Combobox(self.Framevisualisation,textvariable=self.subadmi,values=self.typeadmiget,font=("Arial"))
        self.comboboxsubAdmi.bind("<<ComboboxSelected>>",self.CallSubadmi)
        self.comboboxsubAdmi.place(relx=self.xvisual-0.12, rely=self.yvisual+self.pasy,relwidth=0.07,relheight=0.3)
        self.frame_selpanel.destroy()

        print(self.typeadmiget)
        return
#############################################################################################################################################################################
    
#############################################################################################################################################################################
          
    def CallSubadmi(self,even):
        self.geteursubadmi=1
        print(self.subadmi.get())
        self.typeget1=self.strvartypeMap.get()
        print(self.typeget1)
        #self.Frameplt.destroy
        #self.Frameplt= Frame(self.Framevisualisatio, bg='#000000')
        #self.Frameplt.place(relx=0.01, rely=0.155,relwidth=0.98,relheight=0.77)
        if self.typeget1=='Time Series Tempoaral':
            self.listEnddate=[]
            self.listsartdate=[]
            self.xvisual=0.445
            self.pasy=0.5
            self.frame_selpanel =Frame(self.Framevisualisation,borderwidth=3, padx=0, pady=0.1,bg='#ffffff')
            self.frame_selpanel.place(relx=self.xvisual-0.05, rely=0.01,relwidth=1,relheight=1) 
            self.xvisual=0.54+0.012
            self.pasy=0.5
            self.Labelstartdate=Label(self.frame_selpanel, text ='Start Date1',font=("Arial", 13))
            self.Labelstartdate.place(relx=0.0, \
                rely=0.05,relwidth=0.053,relheight=0.3)
            self.startdate = StringVar()
            self.startdate.set(f"{self.datatimestp[0]}")
            self.comboboxSartdate = ttk.Combobox(self.frame_selpanel,textvariable=self.startdate,value=self.datatimestp,font=("Arial", 13))
            self.comboboxSartdate.bind('<<ComboboxSelected>>', self.callstartdate)
            self.comboboxSartdate.place(relx=0.0, rely=0.4,relwidth=0.053,relheight=0.3)
            ###End startdate
            ###start date
            self.xvisual=0.65+0.011
            self.pasy=0.5
            self.LabelEnddate=Label(self.frame_selpanel, text ='End Date1',font=("Arial", 13))
            self.LabelEnddate.place(relx=0.056, \
                rely=0.05,relwidth=0.053,relheight=0.3)
            self.Enddate = StringVar()
            self.Enddate.set(self.datatimestp[-1])
            self.comboboxEnddate = ttk.Combobox(self.frame_selpanel,textvariable=self.Enddate,value=self.datatimestp,font=("Arial", 13))
            self.comboboxEnddate.bind('<<ComboboxSelected>>', self.callenddate)
            self.comboboxEnddate.place(relx=0.056, rely=0.4,relwidth=0.053,relheight=0.3)

            self.Labelstartdate2=Label(self.frame_selpanel, text ='Start Date2',font=("Arial", 13))
            self.Labelstartdate2.place(relx=0.112, \
                rely=0.05,relwidth=0.053,relheight=0.3)
            self.startdate2 = StringVar()
            self.startdate2.set(f"{self.datatimestp[0]}")
            self.comboboxSartdate2 = ttk.Combobox(self.frame_selpanel,textvariable=self.startdate2,value=self.datatimestp,font=("Arial", 13))
            self.comboboxSartdate2.bind('<<ComboboxSelected>>', self.callstartdate2)
            self.comboboxSartdate2.place(relx=0.112, rely=0.4,relwidth=0.053,relheight=0.3)
            self.LabelEnddate2=Label(self.frame_selpanel, text ='End Date2',font=("Arial", 13))
            self.LabelEnddate2.place(relx=0.169, \
                rely=0.05,relwidth=0.053,relheight=0.3)
            self.Enddate2 = StringVar()
            self.Enddate2.set(self.datatimestp[-1])
            self.comboboxEnddate2 = ttk.Combobox(self.frame_selpanel,textvariable=self.Enddate2,value=self.datatimestp,font=("Arial", 13))
            self.comboboxEnddate2.bind('<<ComboboxSelected>>', self.callenddate2)
            self.comboboxEnddate2.place(relx=0.169, rely=0.4,relwidth=0.053,relheight=0.3)
            self.Labelstartdate3=Label(self.frame_selpanel, text ='Start Date3',font=("Arial", 13))
            self.Labelstartdate3.place(relx=0.225, \
                rely=0.05,relwidth=0.053,relheight=0.3)
            self.startdate3 = StringVar()
            self.startdate3.set(f"{self.datatimestp[0]}")
            self.comboboxSartdate3 = ttk.Combobox(self.frame_selpanel,textvariable=self.startdate3,value=self.datatimestp,font=("Arial", 13))
            self.comboboxSartdate3.bind('<<ComboboxSelected>>', self.callstartdate3)
            self.comboboxSartdate3.place(relx=0.225, rely=0.4,relwidth=0.053,relheight=0.3)
            self.LabelEnddate3=Label(self.frame_selpanel, text ='End Date3',font=("Arial", 13))
            self.LabelEnddate3.place(relx=0.281, \
                rely=0.05,relwidth=0.053,relheight=0.3)
            self.Enddate3 = StringVar()
            self.Enddate3.set(self.datatimestp[-1])
            self.comboboxEnddate3 = ttk.Combobox(self.frame_selpanel,textvariable=self.Enddate3,value=self.datatimestp,font=("Arial", 13))
            self.comboboxEnddate3.bind('<<ComboboxSelected>>', self.callenddate3)
            self.comboboxEnddate3.place(relx=0.281, rely=0.4,relwidth=0.053,relheight=0.3)
            self.Labelstartdate4=Label(self.frame_selpanel, text ='Start Date4',font=("Arial", 13))
            self.Labelstartdate4.place(relx=0.337, \
                rely=0.05,relwidth=0.053,relheight=0.3)
            self.startdate4 = StringVar()
            self.startdate4.set(f"{self.datatimestp[0]}")
            self.comboboxSartdate4 = ttk.Combobox(self.frame_selpanel,textvariable=self.startdate4,value=self.datatimestp,font=("Arial", 13))
            self.comboboxSartdate4.bind('<<ComboboxSelected>>', self.callstartdate4)
            self.comboboxSartdate4.place(relx=0.337, rely=0.4,relwidth=0.053,relheight=0.3)
            self.LabelEnddate4=Label(self.frame_selpanel, text ='End Date4',font=("Arial", 13))
            self.LabelEnddate4.place(relx=0.394, \
                rely=0.05,relwidth=0.053,relheight=0.3)
            self.Enddate4 = StringVar()
            self.Enddate4.set(self.datatimestp[-1])
            self.comboboxEnddate4 = ttk.Combobox(self.frame_selpanel,textvariable=self.Enddate4,value=self.datatimestp,font=("Arial", 13))
            self.comboboxEnddate4.bind('<<ComboboxSelected>>', self.callenddate4)
            self.comboboxEnddate4.place(relx=0.394, rely=0.4,relwidth=0.053,relheight=0.3)
            self.Labelstartdate5=Label(self.frame_selpanel, text ='Start Date5',font=("Arial", 13))
            self.Labelstartdate5.place(relx=0.46, \
                rely=0.05,relwidth=0.053,relheight=0.3)
            self.startdate5 = StringVar()
            self.startdate5.set(f"{self.datatimestp[0]}")
            self.comboboxSartdate5 = ttk.Combobox(self.frame_selpanel,textvariable=self.startdate5,value=self.datatimestp,font=("Arial", 13))
            self.comboboxSartdate5.bind('<<ComboboxSelected>>', self.callstartdate5)
            self.comboboxSartdate5.place(relx=0.46, rely=0.4,relwidth=0.053,relheight=0.3)
            self.LabelEnddate5=Label(self.frame_selpanel, text ='End Date5',font=("Arial", 13))
            self.LabelEnddate5.place(relx=0.52, \
                rely=0.05,relwidth=0.053,relheight=0.3)
            self.Enddate5 = StringVar()
            self.Enddate5.set(self.datatimestp[-1])
            self.comboboxEnddate5 = ttk.Combobox(self.frame_selpanel,textvariable=self.Enddate5,value=self.datatimestp,font=("Arial", 13))
            self.comboboxEnddate5.bind('<<ComboboxSelected>>', self.callenddate5)
            self.comboboxEnddate5.place(relx=0.52, rely=0.4,relwidth=0.055,relheight=0.3)
            Button(self.frame_selpanel,text='Ok',command=lambda:[self.callEnddate(even)]).place(relx=0.58, \
                rely=0.05,relwidth=0.03,relheight=0.5)
            print(self.listEnddate)
        else:
            pass
    
    
    #for 'xy' ploting
        
   
    def callstartdate(self,even):
        self.startdateget=self.startdate.get()#self.startdateget=self.startdate.get()
        self.startdate=self.startdateget
        self.listsartdate.append(self.startdateget)
        #return
    def callenddate(self,even):
        self.Enddateget=self.Enddate.get()
        self.Enddate=self.Enddateget
        self.listEnddate.append(self.Enddateget)
        
        return
    def callstartdate2(self,even):
        self.startdateget2=self.startdate2.get()
        self.startdate2=self.startdateget2
        self.listsartdate.append(self.startdateget2)
        return
    def callenddate2(self,even):
        self.Enddateget2=self.Enddate2.get()
        self.Enddate2=self.Enddateget2
        self.listEnddate.append(self.Enddateget2)
        return
        
    def callstartdate3(self,even):
        self.startdateget3=self.startdate3.get()
        self.startdate3=self.startdateget3
        self.listsartdate.append(self.startdateget3)
        return
    def callenddate3(self,even):
        self.Enddateget3=self.Enddate3.get()
        self.Enddate3=self.Enddateget3
        self.listEnddate.append(self.Enddateget3)
        return
    def callstartdate4(self,even):
        self.startdateget4=self.startdate4.get()
        self.startdate4=self.startdateget4
        self.listsartdate.append(self.startdateget4)
        return
        
    def callenddate4(self,even):
        self.Enddateget4=self.Enddate4.get()
        self.Enddate4=self.Enddateget4
        self.listEnddate.append(self.Enddateget4)
        return
        
    def callstartdate5(self,even):
        self.startdateget5=self.startdate5.get()
        self.startdate5=self.startdateget5
        self.listsartdate.append(self.startdateget5)
        return
        
    def callenddate5(self,even):
        self.Enddateget5=self.Enddate5.get()
        self.Enddate5=self.Enddateget5
        self.listEnddate.append(self.Enddateget5)
        return
    #for 'xy' ploting
    
    def StatestopaddCurve_fn(self):
        self.stateaddfonction=0
        return
    
    
    def StateAdd_fn(self):
        self.stateaddfonction=1
        return
    
    def callEnddate(self,even):
        if self.typeget1=='Time Series Tempoaral':
            self.Frameplt= Frame(self.Framevisualisatio, bg='#000000')
            self.Frameplt.place(relx=0.01, rely=0.155,relwidth=0.98,relheight=0.77)
            #if self.stateaddfonction==1:
            if self.Admi.get()=='Admi1':
                idsubAdmi=self.nameIdAdmi1.get(self.subadmi.get(),0)
                print(f"idsubAdmi={idsubAdmi}")
                self.fonction=self.fonctionDico.get(self.strvartypeMap.get())#get de right fonction to use
                self.List_Idsf.append(idsubAdmi)#add selected admi in the list of admi

                if len(self.List_Idsf)>1:
                    self.btnUpdtePresend=1
                    
                self.List_sfLocality.append(self.shp_pathadmi1)
                s=self.subadmi.get()
                self.List_nameAdmi.append(s)
                x0y0Admi1=self.fonction(id=self.List_Idsf,ShapeFilecontry=self.List_sfLocality,s=self.List_nameAdmi,conteneur=self.Frameplt,data=self.DataForPlot,startdate=self.startdateget,enddate=self.Enddateget,listEnddate=self.listEnddate,listsartdate=self.listsartdate,VAR=self.varselectedget)
                print(f'x0y0{x0y0Admi1[0]}')
                self.stateaddfonction=0
            if self.Admi.get()=='Admi2':
                idsubAdmi=self.nameIdAdmi2.get(self.subadmi.get(),0)
                print(f"idsubAdmi={idsubAdmi}")
                self.fonction=self.fonctionDico.get(self.strvartypeMap.get())#get de right fonction to use
                self.List_Idsf.append(idsubAdmi)#add selected admi in the list of admi
                self.List_sfLocality.append(self.shp_pathadmi2)
                s=self.subadmi.get()
                self.List_nameAdmi.append(s)
                x0y0Admi2=self.fonction(id=self.List_Idsf,ShapeFilecontry=self.List_sfLocality,s=self.List_nameAdmi,conteneur=self.Frameplt,data=self.DataForPlot,startdate=self.startdateget,enddate=self.Enddateget,listEnddate=self.listEnddate,listsartdate=self.listsartdate,VAR=self.varselectedget)
                print(f'x0y0{x0y0Admi2[0]}')
                self.stateaddfonction=0
            if self.Admi.get()=='Admi3':
                idsubAdmi=self.nameIdAdmi3.get(self.subadmi.get(),0)
                print(f"idsubAdmi={idsubAdmi}")
                self.fonction=self.fonctionDico.get(self.strvartypeMap.get())#get de right fonction to use
                self.List_Idsf.append(idsubAdmi)#add selected admi in the list of admi
                self.List_sfLocality.append(self.shp_pathadmi3)
                s=self.subadmi.get()
                self.List_nameAdmi.append(s)
                x0y0Admi3=self.fonction(id=self.List_Idsf,ShapeFilecontry=self.List_sfLocality,s=self.List_nameAdmi,conteneur=self.Frameplt,data=self.DataForPlot,startdate=self.startdateget,enddate=self.Enddateget,listEnddate=self.listEnddate,listsartdate=self.listsartdate,VAR=self.varselectedget)
                print(f'x0y0{x0y0Admi3[0]}')
                self.stateaddfonction=1
            #
        #else:

            #if self.Admi.get()=='Admi1':
                #idsubAdmi=self.nameIdAdmi1.get(self.subadmi.get(),0)
                #print(f"idsubAdmi={idsubAdmi}")
                #self.fonction=self.fonctionDico.get(self.strvartypeMap.get())#get de right fonction to use
                
                #self.List_Idsf1plot=[idsubAdmi]#add selected admi in the list of admi
                #self.List_sfLocality1plot=[self.shp_pathadmi1]
                #s=self.subadmi.get()
                #self.List_nameAdmi1plot=[s]
                #x0y0Admi1=self.fonction(id=self.List_Idsf1plot,ShapeFilecontry=self.List_sfLocality1plot,s=self.List_nameAdmi1plot,conteneur=self.Frameplt,data=self.DataForPlot,listsartdate=self.listsartdate,listEnddate=self.listEnddate,startdate=self.startdateget,enddate=self.Enddateget,startdate2=self.startdateget2,startdate3=self.startdateget3,VAR=self.varselectedget)
                #print(f'x0y0{x0y0Admi1[0]}')
                #self.stateaddfonction=0
            #if self.Admi.get()=='Admi2':
                #idsubAdmi=self.nameIdAdmi2.get(self.subadmi.get(),0)
                #print(f"idsubAdmi={idsubAdmi}")
                #self.fonction=self.fonctionDico.get(self.strvartypeMap.get())#get de right fonction to use
                
                #self.List_Idsf1plot=[idsubAdmi]#add selected admi in the list of admi
                #self.List_sfLocality1plot=[self.shp_pathadmi2]
                #s=self.subadmi.get()
                #self.List_nameAdmi1plot=[s]
                #x0y0Admi3=self.fonction(id=self.List_Idsf1plot,ShapeFilecontry=self.List_sfLocality1plot,s=self.List_nameAdmi1plot,conteneur=self.Frameplt,data=self.DataForPlot,listsartdate=self.listsartdate,listEnddate=self.listEnddate,startdate=self.startdateget,enddate=self.Enddateget,startdate2=self.startdateget2,startdate3=self.startdateget3,VAR=self.varselectedget)
                #print(f'x0y0{x0y0Admi2[0]}')
                #self.stateaddfonction=0
            #if self.Admi.get()=='Admi3':
                #idsubAdmi=self.nameIdAdmi3.get(self.subadmi.get(),0)
                #print(f"idsubAdmi={idsubAdmi}")
                #self.fonction=self.fonctionDico.get(self.strvartypeMap.get())#get de right fonction to use
                
                #self.List_Idsf1plot=[idsubAdmi]#add selected admi in the list of admi
                #self.List_sfLocality1plot=[self.shp_pathadmi3]
                #s=self.subadmi.get()
                #self.List_nameAdmi1plot=[s]
                #x0y0Admi3=self.fonction(id=self.List_Idsf1plot,ShapeFilecontry=self.List_sfLocality1plot,s=self.List_nameAdmi1plot,conteneur=self.Frameplt,data=self.DataForPlot,listsartdate=self.listsartdate,listEnddate=self.listEnddate,startdate=self.startdateget,enddate=self.Enddateget,startdate2=self.startdateget2,startdate3=self.startdateget3,VAR=self.varselectedget)
                #print(f'x0y0{x0y0Admi3[0]}')
                #self.stateaddfonction=0
        #self.stateaddfonction=0
        #return
        else:
            
            self.Enddateget=self.Enddate.get()
            self.Frameplt.destroy
            self.Frameplt= Frame(self.Framevisualisatio, bg='#000000')
            self.Frameplt.place(relx=0.01, rely=0.155,relwidth=0.98,relheight=0.77)
            if self.stateaddfonction==1:
                if self.Admi.get()=='Admi1':
                    idsubAdmi=self.nameIdAdmi1.get(self.subadmi.get(),0)
                    print(f"idsubAdmi={idsubAdmi}")
                    fonction=self.fonctionDico.get(self.strvartypeMap.get())#get de right fonction to use
                    self.List_Idsf.append(idsubAdmi)#add selected admi in the list of admi

                    if len(self.List_Idsf)>1:
                        self.btnUpdtePresend=1
                        
                    self.List_sfLocality.append(self.shp_pathadmi1)
                    s=self.subadmi.get()
                    self.List_nameAdmi.append(s)
                    x0y0Admi1=fonction(id=self.List_Idsf,ShapeFilecontry=self.List_sfLocality,s=self.List_nameAdmi,conteneur=self.Frameplt,data=self.DataForPlot,startdate=self.startdateget,enddate=self.Enddateget,VAR=self.varselectedget)
                    print(f'x0y0{x0y0Admi1[0]}')
                    self.stateaddfonction=0
                if self.Admi.get()=='Admi2':
                    idsubAdmi=self.nameIdAdmi1.get(self.subadmi.get(),0)
                    print(f"idsubAdmi={idsubAdmi}")
                    fonction=self.fonctionDico.get(self.strvartypeMap.get())#get de right fonction to use
                    self.List_Idsf.append(idsubAdmi)#add selected admi in the list of admi
                    self.List_sfLocality.append(self.shp_pathadmi2)
                    s=self.subadmi.get()
                    self.List_nameAdmi.append(s)
                    x0y0Admi2=fonction(id=self.List_Idsf,ShapeFilecontry=self.List_sfLocality,s=self.List_nameAdmi,conteneur=self.Frameplt,data=self.DataForPlot,startdate=self.startdateget,enddate=self.Enddateget,VAR=self.varselectedget)
                    print(f'x0y0{x0y0Admi2[0]}')
                    self.stateaddfonction=0
                if self.Admi.get()=='Admi3':
                    idsubAdmi=self.nameIdAdmi3.get(self.subadmi.get(),0)
                    print(f"idsubAdmi={idsubAdmi}")
                    fonction=self.fonctionDico.get(self.strvartypeMap.get())#get de right fonction to use
                    self.List_Idsf.append(idsubAdmi)#add selected admi in the list of admi
                    self.List_sfLocality.append(self.shp_pathadmi3)
                    s=self.subadmi.get()
                    self.List_nameAdmi.append(s)

                    x0y0Admi3=fonction(id=self.List_Idsf,ShapeFilecontry=self.List_sfLocality,s=self.List_nameAdmi,conteneur=self.Frameplt,data=self.DataForPlot,startdate=self.startdateget,enddate=self.Enddateget,VAR=self.varselectedget)
                    print(f'x0y0{x0y0Admi3[0]}')
                    self.stateaddfonction=0
            else:

                if self.Admi.get()=='Admi1':
                    idsubAdmi=self.nameIdAdmi1.get(self.subadmi.get(),0)
                    print(f"idsubAdmi={idsubAdmi}")
                    fonction=self.fonctionDico.get(self.strvartypeMap.get())#get de right fonction to use
                    
                    self.List_Idsf1plot=[idsubAdmi]#add selected admi in the list of admi
                    self.List_sfLocality1plot=[self.shp_pathadmi1]
                    s=self.subadmi.get()
                    self.List_nameAdmi1plot=[s]
                    x0y0Admi1=fonction(id=self.List_Idsf1plot,ShapeFilecontry=self.List_sfLocality1plot,s=self.List_nameAdmi1plot,conteneur=self.Frameplt,data=self.DataForPlot,startdate=self.startdateget,enddate=self.Enddateget,VAR=self.varselectedget)
                    print(f'x0y0{x0y0Admi1[0]}')
                    self.stateaddfonction=0
                if self.Admi.get()=='Admi2':
                    idsubAdmi=self.nameIdAdmi1.get(self.subadmi.get(),0)
                    print(f"idsubAdmi={idsubAdmi}")
                    fonction=self.fonctionDico.get(self.strvartypeMap.get())#get de right fonction to use

                    
                    self.List_Idsf1plot=[idsubAdmi]#add selected admi in the list of admi
                    self.List_sfLocality1plot=[self.shp_pathadmi2]
                    s=self.subadmi.get()
                    self.List_nameAdmi1plot=[s]
                    x0y0Admi2=fonction(id=self.List_Idsf1plot,ShapeFilecontry=self.List_sfLocality1plot,s=self.List_nameAdmi1plot,conteneur=self.Frameplt,data=self.DataForPlot,startdate=self.startdateget,enddate=self.Enddateget,VAR=self.varselectedget)
                    print(f'x0y0{x0y0Admi2[0]}')
                    self.stateaddfonction=0
                if self.Admi.get()=='Admi3':
                    idsubAdmi=self.nameIdAdmi3.get(self.subadmi.get(),0)
                    print(f"idsubAdmi={idsubAdmi}")
                    fonction=self.fonctionDico.get(self.strvartypeMap.get())#get de right fonction to use
                    
                    self.List_Idsf1plot=[idsubAdmi]#add selected admi in the list of admi
                    self.List_sfLocality1plot=[self.shp_pathadmi3]
                    s=self.subadmi.get()
                    self.List_nameAdmi1plot=[s]
                    x0y0Admi3=fonction(id=self.List_Idsf1plot,ShapeFilecontry=self.List_sfLocality1plot,s=self.List_nameAdmi1plot,conteneur=self.Frameplt,data=self.DataForPlot,startdate=self.startdateget,enddate=self.Enddateget,VAR=self.varselectedget)
                    print(f'x0y0{x0y0Admi3[0]}')
                    self.stateaddfonction=0
            self.stateaddfonction=0
            return
            
       
    #for 'map' ploting
    def callStepMap(self,even):
        self.stepmap=self.dicoTimeStep.get(self.stpMap.get(), 0)
        b=self.fonctionDico.get(self.strvartypeMap.get())
        b(data=self.DataForPlot,var=self.varselectedget,conteneur=self.Frameplt,area=self.SELAREAL,masque=self.masque,GETRefNBRE=self.GETRefNBRE,step=self.stepmap)
        return
    
    def NEXTSTEPMAP(self):
        self.pointeurStep=self.stepmap
        if self.pointeurStep<int([*self.dicoTimeStep.values()][-1]):
            self.pointeurStep+=1
            self.stepmap=self.pointeurStep
            for k in self.dicoTimeStep:
                if self.dicoTimeStep[k]==self.stepmap:
                    c=k
            self.stpMap.set(c)
            time.sleep(0.5)
            b=self.fonctionDico.get(self.strvartypeMap.get())
            b(data=self.DataForPlot,var=self.varselectedget,conteneur=self.Frameplt,area=self.SELAREAL,masque=self.masque,GETRefNBRE=self.GETRefNBRE,step=self.stepmap)
            return
        else:
            messagebox.showinfo('Well Done', 'This step is the Last step in the Database ')

    def PREVIOUSSTEPMAP(self):
        self.pointeurStep=self.stepmap
        if self.pointeurStep>int([*self.dicoTimeStep.values()][0]):
            self.pointeurStep-=1
            self.stepmap=self.pointeurStep
            for k in self.dicoTimeStep:
                if self.dicoTimeStep[k]==self.stepmap:
                    c=k
            self.stpMap.set(c)
            time.sleep(0.5)
            b=self.fonctionDico.get(self.strvartypeMap.get())
            b(data=self.DataForPlot,var=self.varselectedget,conteneur=self.Frameplt,area=self.SELAREAL,masque=self.masque,GETRefNBRE=self.GETRefNBRE,step=self.stepmap)
            return
        else:
            messagebox.showinfo('Well Done', 'This step is the First step in the Database at this moment')          
    
    
    def ViewMultiGraph(self):
        self.Frameplt.destroy
        self.Frameplt= Frame(self.Framevisualisatio, bg='#000000')
        self.Frameplt.place(relx=0.01, rely=0.155,relwidth=0.98,relheight=0.77)
        if len(self.List_Idsf)>1:
            #self.List_Idsf.append(idsubAdmi)#add selected admi in the list of admi
            #self.List_sfLocality.append(self.shp_pathadmi2)
            #s=self.subadmi.get()
            #self.List_nameAdmi.append(s)
            x0y0Admi2=self.fonction(id=self.List_Idsf,ShapeFilecontry=self.List_sfLocality,s=self.List_nameAdmi,conteneur=self.Frameplt,data=self.DataForPlot,startdate=self.startdateget,enddate=self.Enddateget,listEnddate=self.listEnddate,listsartdate=self.listsartdate,VAR=self.varselectedget)
            print(f'x0y0{x0y0Admi2[0]}')
            self.stateaddfonction=1
            
        return
    
    def RESET(self):
        self.Framevisualisatio.destroy
        self.Frameplt= Frame(self.Framevisualisatio, bg='#000000')
        self.Frameplt.place(relx=0.01, rely=0.155,relwidth=0.98,relheight=0.77)
        self.List_Idsf=[]
        self.List_Idsf1plot=[]
        self.List_sfLocality=[]
        self.List_sfLocality1plot=[]
        self.List_nameAdmi=[]
        self.List_nameAdmi1plot=[]
        return
#DataForPlot='/home/rodrigue/aims-computer/Tchend2/inter_tools/ERA5/datasetERA5/yearsIndice/Tmax2m_2010_daily_C.nc'
#root=Tk()
#root.geometry('1200x700')
#VISUALISATION(conteneur=root,DataForPlot=DataForPlot,SELVARL=['tp'],SELAREAL=['8','17','1','14'],masque='Cameroon',step=0)                                                  

#root.mainloop()
