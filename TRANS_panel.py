##
#  File:
#    TRANS_panel.py
#
#  Synopsis:
#    Illustrates how to create a panel plot
#
#  Categories:
#    contour plot
#    panel plot
#
#  Author:
#    Karin Meier-Fleischer, based on NCL example
#  
#  Date of initial publication:
#    September 2018
#
#  Description:
#    This example shows how to create a panel plot.
#    xarray is used to read the NetCDF file, but PyNIO can also
#    be used. See the lines commented with ###.
#
#  Effects illustrated:
#    o  Read netCDF data
#    o  Drawing a contour fill plot
#    o  Creating a panel plot
# 
#  Output:
#    A single visualization is produced.
#
#  Notes: The data for this example can be downloaded from 
#    http://www.ncl.ucar.edu/Document/Manuals/NCL_User_Guide/Data/
#   
'''
  Transition Guide Python Example: TRANS_panel.py
  
  -  Drawing a contour fill plot
  -  Creating a panel plot

  18-09-10  kmf
'''
import Ngl
from cdo import Cdo
import os
import netCDF4
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.basemap import Basemap
from packInter.showimage import SHOWIMAGE#packInter.
from tkinter import*
from tkinter import messagebox,ttk
class Panelmanager(object):
    def __init__(self,data,var,conteneur,area,masque,GETRefNBRE,step,SELVARL):#dicoTimeStep):
        self.data=data
        self.var=var
        self.conteneur=conteneur
        self.area=area
        self.masque=masque
        self.GETRefNBRE=GETRefNBRE
        self.SELVARL=SELVARL
        #self.dicoTimeStep=dicoTimeStep
        cdo=Cdo()
        B=cdo.showdate(input=self.data)
        LLab= B[0].replace(" ", "")#.replace(" ", " ")
        datatimestp=[LLab[x:x+10] for x in range(0,len(LLab),10)]
        j=0
        self.dicoTimeStep={}
        for i in datatimestp:
            self.dicoTimeStep.update({i:j})#self.dicoTimeStep is the dictionary stp:value example,
            j+=1
        #print(self.dicoTimeStep)
        
        self.SELECTDATEPANEL(datapanel=[*self.dicoTimeStep.keys()],conteneur=self.conteneur)
    def PANELNCL(self,data,var,conteneur,area,masque,dicoTimeStep,GETRefNBRE,SELVARL):
        VARGET=var #get the variable position zero in the list of variable
        nc = netCDF4.Dataset(self.data)
        var = nc.variables[VARGET]

        Lon_lat_notation=var.dimensions
        for i in Lon_lat_notation:
            if i=='lat':
                lat=lat = nc.variables["lat"][:]
            if i=='latitude':
                lat = nc.variables["latitude"][:]
            if i=='lon':
                lon=nc.variables["lon"][:]
            if i=='longitude':
                lon=nc.variables["longitude"][:]
            else:
                lat=lat = nc.variables[Lon_lat_notation[-2]][:]
                lon=nc.variables[Lon_lat_notation[-1]][:]
        time = nc.variables['time'][:]
        
        #mslp = nc.variables[var[0]][:] # mean sea level pressure
        #u = nc.variables['p10u'][:] # 10m u-component of winds
        #v = nc.variables['p10v'][:] # 10m v-component of winds
        map = Basemap(projection='merc',llcrnrlon=float(area[0]),llcrnrlat=float(area[2]),urcrnrlon=float(area[1]),urcrnrlat=float(area[3]),resolution='i') # projection, lat/lon extents and resolution of polygons to draw
            #-- start the graphics
        #wks = Ngl.open_wks("png",os.path.basename(__file__).split('.')[0])
        nomImage='/image.png'
        wks = Ngl.open_wks("png",os.path.basename(nomImage).split('.')[0])
        #-- resource settings
        res                 =  Ngl.Resources()
        res.nglDraw         =  False            #-- don't draw plots
        res.nglFrame        =  False            #-- don't advance the frame

        res.cnLinesOn                   = False # Turn off contour lines

        res.cnFillOn        =  True             #-- contour fill
        res.cnFillPalette   = "WhiteBlueGreenYellowRed"         #-- choose color map
        res.cnLineLabelsOn  =  False            #-- no line labels

        res.lbLabelBarOn    =  False            #-- don't draw a labelbar
        res.cnLevelSelectionMode = "AutomaticLevels" #-- set levels
        #res.cnLevelSelectionMode = "ManualLevels" #-- set levels
        #res.cnMinLevelValF = 20.0    #-- contour min. value
        #res.cnMaxLevelValF = 33.0    #-- contour max. value
        #res.cnLevelSpacingF = 1.0    #-- contour interval
        res.cnFillDrawOrder = "Predraw"         #-- contours first
        res.sfXArray        =  lon              #-- coordinates for the x-axis
        res.sfYArray        =  lat              #-- coordinates for the y-axis
        
        #mask_specs = ["Cameroon","Central African Republic","Chad","Congo","Bioko","Rio Muni","Sao Tome and Principe","Equatorial Guinea", \
            #"Gabon","Rwanda","Burundi","Angola"]
        if masque=="Republic of Congo":
            mask_specs=["Congo"]
        if masque=="Democratic Republic of Congo":
            mask_specs=["Democratic Republic of the Congo"]
        if masque=="ECCAS":
            mask_specs=["Cameroon","Central African Republic","Chad","Congo","Bioko","Rio Muni","Sao Tome and Principe","Equatorial Guinea","Gabon","Rwanda","Burundi","Angola","Democratic Republic of the Congo","exclave called Cabinda"]
        else:
            mask_specs = [masque]  
        res.mpDataBaseVersion = "MediumRes" #-- alias to Ncarg4_1
        res.mpDataSetName = "Earth..4"
        res.mpGridAndLimbOn= False
        res.mpFillOn = True    #-- turn on map fill
        res.mpOutlineBoundarySets = "National"
        res.mpFillBoundarySets = "National"
        res.mpAreaMaskingOn = True
        res.mpMaskAreaSpecifiers = mask_specs
        res.mpFillAreaSpecifiers = ["land","water"]
        res.mpSpecifiedFillColors = ["gray90","deepskyblue2","gray65"]  
        
        
        res.mpLimitMode = "LatLon" #-- limit map via lat/lon
        res.mpMinLatF= int(area[2])   #-- min lat
        res.mpMaxLatF = int(area[3])   #-- max lat
        res.mpMinLonF = int(area[0])
        res.mpMaxLonF =int(area[1])
        
        #-- create the contour plots
        #plot = []
        #for i in range(0,4):
            #p = Ngl.contour_map(wks,var[i,:,:],res)
            #plot.append(p)
        
        plot = []
       
        for i in [*self.stepmapselectdico.keys()]:
            res.tiMainOn        =  True
            step=int(self.stepmapselectdico.get(i))
            
            #print(f'i,step={i,step}')
            ######################
            if var[0,0,0]>200:
                res.tiMainString = f'{i}'
                p = Ngl.contour_map(wks,var[step,:,:]-273.15,res)#step
                plot.append(p)
            else:
                res.tiMainString = f'{i}'
                p = Ngl.contour_map(wks,var[step,:,:],res)#step
                plot.append(p)    
            ######################
            #p = Ngl.contour_map(wks,var[step,:,:],res)#0 is hte time step
            #plot.append(p)
        #-- panel resources
        pnlres = Ngl.Resources()
        pnlres.nglMaximize = True
        #pnlres.nglDraw          = False
        pnlres.nglFrame         = False
        pnlres.nglPanelLabelBar = True #-- common labelbar
        #pnlres.lbOrientation = "Vertical"
        #pnlres.tiMainOn        =  True
        pnlres.txFontHeightF    =  0.2 #= var.long_name
        pnlres.txString    = var.long_name #-- panel title
        pnlres.tiMainFontHeightF    =  0.1 #-- text font size
        #pnlres.lbLabelFontHeightF = 0.015
        pnlres.nglAttachBordenOn =True    #############################################tchendcomment
        #pnlres.lbLabelFontHeightF = 0.02
        pnlres.pmLabelBarWidthF = 0.82  
        pnlres.lbTitleFontHeightF  = 0.015
        pnlres.lbTitlePosition   =  "Top"
        #pnlres.lbTitleString   =  var.units#"~S~o~N~C"
        #pnlres.tiMainString    =  'Precipation'
        
        txres = Ngl.Resources()
        print(self.SELVARL[0])
        if self.SELVARL[0]=="mx2t" or self.SELVARL[0]=="mn2t" or self.SELVARL[0]=="tp":
            if len([*self.stepmapselectdico.keys()])==1:
                Ngl.panel(wks,plot[0:len([*self.stepmapselectdico.keys()])],[1,1],pnlres)
                txres.txFontHeightF = 0.02
                txres.txAngleF    =  90
                if len(var.long_name)>50:
                    Ngl.text_ndc(wks,self.var,0.04,0.5,txres)
                else:
                    Ngl.text_ndc(wks,var.long_name,0.51,0.96,txres)
            
            if len([*self.stepmapselectdico.keys()])==2:
                Ngl.panel(wks,plot[0:len([*self.stepmapselectdico.keys()])],[1,2],pnlres) 
                txres.txFontHeightF = 0.02
                if len(var.long_name)>50:
                    Ngl.text_ndc(wks,self.var ,0.51,0.96,txres)
                else:
                    Ngl.text_ndc(wks,var.long_name,0.51,0.96,txres)
                
            if len([*self.stepmapselectdico.keys()])>=3 and len([*self.stepmapselectdico.keys()])<=4:
                nbreStep=len([*self.stepmapselectdico.keys()])
                
                Ngl.panel(wks,plot[0:len([*self.stepmapselectdico.keys()])],[2,2],pnlres) 
                txres.txFontHeightF = 0.02
                txres.txAngleF    =  90
                if len(var.long_name)>50:
                    Ngl.text_ndc(wks,self.var ,0.07,0.5,txres)
                else:
                    Ngl.text_ndc(wks,var.long_name,0.07,0.5,txres)

            if len([*self.stepmapselectdico.keys()])>=5 and len([*self.stepmapselectdico.keys()])<=6:
                nbreStep=len([*self.stepmapselectdico.keys()])
                
                Ngl.panel(wks,plot[0:len([*self.stepmapselectdico.keys()])],[2,3],pnlres) 
                txres.txFontHeightF = 0.02
                #txres.txAngleF    =  90
                if len(var.long_name)>50:
                    Ngl.text_ndc(wks,self.var,0.51,0.96,txres)
                else:
                    Ngl.text_ndc(wks,var.long_name,0.51,0.96,txres)
                
            if len([*self.stepmapselectdico.keys()])>=7 and len([*self.stepmapselectdico.keys()])<=9:
                nbreStep=len([*self.stepmapselectdico.keys()])
                
                Ngl.panel(wks,plot[0:len([*self.stepmapselectdico.keys()])],[3,3],pnlres) 
                txres.txFontHeightF = 0.02
                txres.txAngleF    =  90
                if len(var.long_name)>50:
                    Ngl.text_ndc(wks,self.var ,0.1,0.5,txres)
                else:
                    Ngl.text_ndc(wks,var.long_name,0.1,0.5,txres)
                
            if len([*self.stepmapselectdico.keys()])>=10 and len([*self.stepmapselectdico.keys()])<=12:
                nbreStep=len([*self.stepmapselectdico.keys()])
                
                Ngl.panel(wks,plot[0:len([*self.stepmapselectdico.keys()])],[3,4],pnlres) 
                txres.txFontHeightF = 0.02
                txres.txAngleF    =  90
                if len(var.long_name)>50:
                    Ngl.text_ndc(wks,self.var,0.015,0.5,txres)
                else:
                    Ngl.text_ndc(wks,var.long_name,0.015,0.5,txres)
            if len([*self.stepmapselectdico.keys()])>=13 and len([*self.stepmapselectdico.keys()])<=16:
                nbreStep=len([*self.stepmapselectdico.keys()])
            
                Ngl.panel(wks,plot[0:len([*self.stepmapselectdico.keys()])],[4,4],pnlres)
                txres.txFontHeightF = 0.02
                txres.txAngleF    =  90
                if len(var.long_name)>50:
                    Ngl.text_ndc(wks,self.var,0.015,0.5,txres)
                else:
                    Ngl.text_ndc(wks,var.long_name,0.015,0.5,txres)

        else:
            if len([*self.stepmapselectdico.keys()])==1:
                Ngl.panel(wks,plot[0:len([*self.stepmapselectdico.keys()])],[1,1],pnlres)
                txres.txFontHeightF = 0.02
                txres.txAngleF    =  90
                if len(var.long_name)>50:
                    Ngl.text_ndc(wks,self.var +' with Threshold equal to '+GETRefNBRE,0.04,0.5,txres)
                else:
                    Ngl.text_ndc(wks,var.long_name,0.51,0.96,txres)
            
            if len([*self.stepmapselectdico.keys()])==2:
                Ngl.panel(wks,plot[0:len([*self.stepmapselectdico.keys()])],[1,2],pnlres) 
                txres.txFontHeightF = 0.02
                if len(var.long_name)>50:
                    Ngl.text_ndc(wks,self.var +' with Threshold equal to '+GETRefNBRE,0.51,0.96,txres)
                else:
                    Ngl.text_ndc(wks,var.long_name,0.51,0.96,txres)
                
            if len([*self.stepmapselectdico.keys()])>=3 and len([*self.stepmapselectdico.keys()])<=4:
                nbreStep=len([*self.stepmapselectdico.keys()])
                
                Ngl.panel(wks,plot[0:len([*self.stepmapselectdico.keys()])],[2,2],pnlres) 
                txres.txFontHeightF = 0.02
                txres.txAngleF    =  90
                if len(var.long_name)>50:
                    Ngl.text_ndc(wks,self.var +' with Threshold equal to '+GETRefNBRE,0.07,0.5,txres)
                else:
                    Ngl.text_ndc(wks,var.long_name,0.07,0.5,txres)

            if len([*self.stepmapselectdico.keys()])>=5 and len([*self.stepmapselectdico.keys()])<=6:
                nbreStep=len([*self.stepmapselectdico.keys()])
                
                Ngl.panel(wks,plot[0:len([*self.stepmapselectdico.keys()])],[2,3],pnlres) 
                txres.txFontHeightF = 0.02
                #txres.txAngleF    =  90
                if len(var.long_name)>50:
                    Ngl.text_ndc(wks,self.var +' with Threshold equal to '+GETRefNBRE,0.51,0.96,txres)
                else:
                    Ngl.text_ndc(wks,var.long_name,0.51,0.96,txres)
                
            if len([*self.stepmapselectdico.keys()])>=7 and len([*self.stepmapselectdico.keys()])<=9:
                nbreStep=len([*self.stepmapselectdico.keys()])
                
                Ngl.panel(wks,plot[0:len([*self.stepmapselectdico.keys()])],[3,3],pnlres) 
                txres.txFontHeightF = 0.02
                txres.txAngleF    =  90
                if len(var.long_name)>50:
                    Ngl.text_ndc(wks,self.var +' with Threshold equal to '+GETRefNBRE,0.1,0.5,txres)
                else:
                    Ngl.text_ndc(wks,var.long_name,0.1,0.5,txres)
                
            if len([*self.stepmapselectdico.keys()])>=10 and len([*self.stepmapselectdico.keys()])<=12:
                nbreStep=len([*self.stepmapselectdico.keys()])
                
                Ngl.panel(wks,plot[0:len([*self.stepmapselectdico.keys()])],[3,4],pnlres) 
                txres.txFontHeightF = 0.02
                txres.txAngleF    =  90
                if len(var.long_name)>50:
                    Ngl.text_ndc(wks,self.var,0.015,0.5,txres)
                else:
                    Ngl.text_ndc(wks,var.long_name,0.015,0.5,txres)
            if len([*self.stepmapselectdico.keys()])>=13 and len([*self.stepmapselectdico.keys()])<=16:
                nbreStep=len([*self.stepmapselectdico.keys()])
            
                Ngl.panel(wks,plot[0:len([*self.stepmapselectdico.keys()])],[4,4],pnlres)
                txres.txFontHeightF = 0.02
                txres.txAngleF    =  90
                if len(var.long_name)>50:
                    Ngl.text_ndc(wks,self.var +' with Threshold equal to '+GETRefNBRE,0.015,0.5,txres)
                else:
                    Ngl.text_ndc(wks,var.long_name,0.015,0.5,txres)
            
            
            #len([*self.stepmapselectdico.keys()])<37:
        #   Ngl.panel(wks,plot[0:len([*self.stepmapselectdico.keys()])],[len([*self.stepmapselectdico.keys()])/6,6],pnlres) 

        #else:
            #Ngl.panel(wks,plot[0:len([*self.stepmapselectdico.keys()])],[4,6],pnlres)
        
        #pnlres.mpNationalLineThicknessF  = 4.0
        #pnlres.mpGeophysicalLineThicknessF  = 3.0
        #pnlres.mpNationalLineColor = "black"
        #pnlres.cnLineLabelsOn    = False
        #pnlres.pmTickMarkDisplayMode  = "always" 
        #pnlres.tiMainFontHeightF  =  0.035
        #pnlres.tmXTOn    = False
        #pnlres.tmYROn  = False
        pnlres.tiMainOn        =  True
        pnlres.txFontHeightF    =  0.2 #= var.long_name
        pnlres.txString    = var.long_name #-- panel title
        #pnlres.tiMainFontHeightF    =  0.1 #-- text font size
        #-- add title string,long_name and units string to panel

        #txres.txFontHeightF = 0.020
        #Ngl.text_ndc(wks,"TRANS: panel example",0.5,0.825,txres)
        #Ngl.text_ndc(wks,f"Precipation of {i}",0.5,0.825,txres)

        #txres.txFontHeightF = 0.02
        #txres.txAngleF    =  90
        #Ngl.text_ndc(wks,var.long_name,0.51,0.96,txres)
        #plt.show()
        #-- min lon
        #Ngl.text_ndc(wks, f.variables["r"],0.975,0.79,txres)

        ###Ngl.text_ndc(wks,f.variables["tsurf"].attributes['long_name'],0.12,0.79,txres)
        ###Ngl.text_ndc(wks,f.variables["tsurf"].attributes['units'],    0.975,0.79,txres)

        #-- advance the frame
        Ngl.frame(wks)
        img = 'image.png'#PhotoImage(file='image.png')
        root1=Toplevel()
        root1.geometry("700x700")
        image_window = SHOWIMAGE(root1, fig=img)
        conteneur.mainloop()
        return Ngl.end()
            ####TIME STEP
            
    ########################################################################################
    def SELECTDATEPANEL(self,datapanel,conteneur):
        NBREIMAGE=16
        self.frame_selpanel =Frame(conteneur,borderwidth=3, padx=0, pady=0.1,bg='#ffffff')
        self.frame_selpanel.place(relx=0.0, rely=0.0,relwidth=1,relheight=1)
        def RETURNPLOT():
            self.frame_selpanel.destroy
            print(f'image_selected={self.image_selected}')
            self.stepmapselectdico={}
            for date in self.image_selected:
                self.stepmapselectdico.update({date:self.dicoTimeStep.get(date)})
            print(f'dicoTimeStep={self.stepmapselectdico}')
            self.PANELNCL(data=self.data,var=self.var,conteneur=self.frame_selpanel,area=self.area,masque=self.masque,GETRefNBRE=self.GETRefNBRE,SELVARL=self.SELVARL,dicoTimeStep=self.stepmapselectdico)
            return
        def callstartdate(even):
            self.image_selected=[]
            Button(self.frame_selpanel, text="OK",padx=0.5, pady=0.1,bg="#ffffff",command=RETURNPLOT,font=("Arial", 16)).place(relx=0.8,rely=0.90 ,relwidth=0.13,relheight=0.06)
            for i in range(NBREIMAGE):
                if STRINGVAR[i].get()!='Please Choose date':
                    if STRINGVAR[i].get() not in self.image_selected:
                        self.image_selected.append(STRINGVAR[i].get())
                        
            print(self.image_selected)
            FRAME0 =Frame(self.frame_selpanel,borderwidth=3, padx=0, pady=0.1,bg='#ffffff')
            FRAME0.place(relx=0.0, rely=0.7,relwidth=1,relheight=0.2)
            if len(self.image_selected)<9:
                Label(FRAME0,text=f"{self.image_selected}",bg='#ffffff',font=("Arial", 16)).place(relx=0.01, rely=0.1,relwidth=1,relheight=0.8)
                return 
            elif len(self.image_selected)<=16:
                Label(FRAME0,text=f"{self.image_selected[:8]}",bg='#ffffff',font=("Arial", 16)).place(relx=0.01, rely=0.0,relwidth=1,relheight=0.2)
                Label(FRAME0,text=f"{self.image_selected[8:]}",bg='#ffffff',font=("Arial", 16)).place(relx=0.01, rely=0.5,relwidth=1,relheight=0.2)
                print(self.image_selected)
                return 
            

        
        
        xvisual=0.2
        pasy=0.1
        STRINGVAR=[StringVar() for i in range(NBREIMAGE)]
        for i in range(NBREIMAGE):
            
            #if i%5!=0:
            xvisual=xvisual+0.2
            #pasy=pasy+0.1
            if i%4!=0:
                Labelstartdate=Label(self.frame_selpanel, text =f'Image {i+1}',font=("Arial", 16))
                Labelstartdate.place(relx=xvisual, \
                rely=pasy-0.051,relwidth=0.1,relheight=0.05)
        #startdate = StringVar()
                #startdate.set(datatimestp[i])
                STRINGVAR[i].set('Please Choose date')
                comboboxSartdate = ttk.Combobox(self.frame_selpanel,textvariable=STRINGVAR[i],value=datapanel,font=("Arial", 16))
                comboboxSartdate.bind('<<ComboboxSelected>>', callstartdate)
                comboboxSartdate.place(relx=xvisual, rely=pasy,relwidth=0.1,relheight=0.05)
                #xvisual=xvisual+0.15
            else:
                pasy=pasy+0.1 
                xvisual=0.2
                Labelstartdate=Label(self.frame_selpanel, text =f'Image {i+1}',font=("Arial", 16))
                Labelstartdate.place(relx=xvisual, \
                rely=pasy-0.051,relwidth=0.1,relheight=0.05)
                startdate = StringVar()
                STRINGVAR[i].set('Please Choose date')
                comboboxSartdate = ttk.Combobox(self.frame_selpanel,textvariable=STRINGVAR[i],value=datapanel,font=("Arial", 16))
                comboboxSartdate.bind('<<ComboboxSelected>>', callstartdate)
                comboboxSartdate.place(relx=xvisual, rely=pasy,relwidth=0.1,relheight=0.05)
        return 
            

    #datapanel=["2009-10-01","2009-10-02","2009-10-03","2009-10-04",\
                            #"2009-10-05","2009-10-06","2009-10-07","2009-10-08","2009-10-09",\
                            #"2009-10-10","2009-10-11","2009-10-12","2009-10-13","2009-10-14",\
                            #"2009-10-15","2009-10-16","2009-10-17","2009-10-18","2009-10-19",\
                            #"2009-10-20","2009-10-21","2009-10-22","2009-10-23","2009-10-24"]
    #conteneur=Tk()
    #SELECTDATEPANEL(datapanel=datapanel,conteneur=conteneur)
    #conteneur.mainloop()
    ################################################################################

#root=Tk()
#masque='ECCAS'
#data='/home/rodrigue/aims-computer/Tchend2/inter_tools/ERA5/datasetERA5/Tmax2m_2009-2018_daily_C.nc'
#var=['mx2t']
#area=['5','32','-19','24']

#cdo=Cdo()
#B=cdo.showdate(input=data)
#LLab= B[0].replace(" ", "")#.replace(" ", " ")
#datatimestp=[LLab[x:x+10] for x in range(0,len(LLab),10)]
#j=0
#dicoTimeStep={}
#for i in datatimestp:
    #dicoTimeStep.update({i:j})#dicoTimeStep is the dictionary stp:value example,2020-07-27:1
    #j+=1
#####END TIME STEP


#Panelmanager(data=data,var=var,conteneur=root,area=area,masque=masque,step=dicoTimeStep)
#root.mainloop()
