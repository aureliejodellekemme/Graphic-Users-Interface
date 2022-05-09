#a) Plots the shape (polygon) based on the city’s coordinates and,
#b) calculates and return the medium point of that specific shape (x0, y0).
#This medium point is also used to define where to print the city name.
from cdo import *
import numpy as np
import pandas as pd
import shapefile as shp
import matplotlib.pyplot as plt
import seaborn as sns
from packInter.showplt import SHOWPLT#packInter.
import xarray as xr
import matplotlib.pyplot as plt
import numpy as np
import random
import netCDF4
def plot_map_contry(sf, x_lim = None, y_lim = None, figsize = (11,9)):
    sf = shp.Reader(sf)
    #plt.figure(figsize = figsize)
    id=0
    dic_city={}
    for shape in sf.shapeRecords():
        x = [i[0] for i in shape.shape.points
             [:]]
        y = [i[1] for i in shape.shape.points[:]]
        if (x_lim == None) & (y_lim == None):
            x0 = np.mean(x)
            y0 = np.mean(y)
            dic_city.update({sf.records()[id][-5]:id})
        id = id+1
    return dic_city
#################################
def plot_contry(sf, x_lim = None, y_lim = None, figsize = (11,9)):
    plt.close()
    sf = shp.Reader(sf)
    #plt.figure(figsize = figsize)
    id=0
    dic_city={}
    for shape in sf.shapeRecords():
        x = [i[0] for i in shape.shape.points[:]]
        y = [i[1] for i in shape.shape.points[:]]
        plt.plot(x, y, 'k')
        
        if (x_lim == None) & (y_lim == None):
            x0 = np.mean(x)
            y0 = np.mean(y)
            plt.text(x0, y0, sf.records()[id][-1], fontsize=10)
        id = id+1
        
    if (x_lim != None) & (y_lim != None):     
        plt.xlim(x_lim)
        plt.ylim(y_lim)#calling the function and passing required parameters to plot the full mapplot_map(sf)
        
###############################
def TimeSeries(id, ShapeFilecontry,s,conteneur,data,startdate,enddate,VAR,x_lim = None,y_lim = None,figsize = (17,12),color = 'y'):
    cdo=Cdo()
    cdo.chname(VAR,'Var_xr', input=data, output='ERA5/outputERA5/dataLastTimeSeries.nc')
    path='ERA5/outputERA5/dataLastTimeSeries.nc'
    print(f'startdate={startdate}, enddate={enddate}')
    print(ShapeFilecontry)
    
            #plt.figure(figsize = figsize)
    fig = plt.figure(figsize=figsize, constrained_layout=True)
    gs = fig.add_gridspec(4, 12)

    #fig.suptitle(f'{nom}', fontweight='bold', fontsize=20)
   
    axs1= fig.add_subplot(gs[:, 0:3])
    axs2=fig.add_subplot(gs[:, 4:])
    for j in range(len(id)):
        sf = shp.Reader(ShapeFilecontry[j])
        

        #axs3=fig.add_subplot(gs[1, 0:7])
        for shape in sf.shapeRecords():
            x = [i[0] for i in shape.shape.points[:]]
            y = [i[1] for i in shape.shape.points[:]]
            axs1.plot(x, y, 'k')
            
        shape_ex = sf.shape(id[j])
        x_lon = np.zeros((len(shape_ex.points),1))
        y_lat = np.zeros((len(shape_ex.points),1))
        for ip in range(len(shape_ex.points)):
            x_lon[ip] = shape_ex.points[ip][0]
            y_lat[ip] = shape_ex.points[ip][1]
        axs1.fill(x_lon,y_lat, color)
        
        if (x_lim != None) & (y_lim != None):     
            axs1.xlim(x_lim)
            axs1.ylim(y_lim)#
            axs1.plot_map_fill(0, sf, x_lim, y_lim)
            #axs1.plot_map_fill(13, sf,color='y') 

        ###########################
        shape_ex = sf.shape(id[j])#NP.ZERO initializes an array of rows and column with 0 in place of each elements 
        #an array will be generated where number of rows will be(len(shape_ex,point))and number of columns will be 1 and stored into the variable
        x_lon = np.zeros((len(shape_ex.points),1))#an array will be generated where number of rows will be(len(shape_ex,point))and number of columns will be 1 and stored into the variable
        y_lat = np.zeros((len(shape_ex.points),1))
        for ip in range(len(shape_ex.points)):
            x_lon[ip] = shape_ex.points[ip][0]
            y_lat[ip] = shape_ex.points[ip][1]#plotting using the derived coordinated stored in array created by numpy
        x0 = np.mean(x_lon)
        y0 = np.mean(y_lat)
        axs1.plot(x0,y0,'o', label=f'{s[j]} (Lon={round(x0,2)}; Lat={round(y0,2)})')
        #axs2.plot(x_lon,y_lat,label=f'{x0,y0}',color='y')
        axs1.grid()
        axs1.legend()
        #axs2.text(x0, y0, s[j], fontsize=10)# use bbox (bounding box) to set plot limits
        #plt.xlim(shape_ex.bbox[0],shape_ex.bbox[2])

        
        ncf = netCDF4.Dataset(path, 'r')
        dataset = xr.open_dataset(path)
        #
        # all_times variable includes the time:units attribute
        
        varlL = ncf.variables['Var_xr']

        Lon_lat_notation=varlL.dimensions
        for i in Lon_lat_notation:
            if i=='lat':
                lats=ncf.variables["lat"][:]
            if i=='latitude':
                lats = ncf.variables["latitude"][:]
            if i=='lon':
                lons=ncf.variables["lon"][:]
            if i=='longitude':
                lons=ncf.variables["longitude"][:]
            else:
                lats= ncf.variables[Lon_lat_notation[-2]][:]
                lons=ncf.variables[Lon_lat_notation[-1]][:]
        #
        indexlat = np.argmin( np.abs( lats - x0))
        indexlon = np.argmin( np.abs( lons - y0))

        #if dataset.Var_xr[0,0,0]>200:
            #b=dataset.Var_xr[:,indexlat,indexlon].sel(time=slice(startdate,enddate))-273.15
        #else:
        b=dataset.Var_xr[:,indexlat,indexlon].sel(time=slice(startdate,enddate))
        #plt.plot(dataset.time[:],b)
        data1=b
        print(b)
        print(slice(startdate,enddate))
        #Index=pd.date_range(startdate,enddate)
        #mx2t=pd.Series(data1,index=Index)
        #dataf=pd.DataFrame({'var':mx2t})
        #df=dataf['var']
        #dtmean=[np.mean(b) for i in range(len(b))]
        if len(id)>1:
            axs2.plot(b.time,b)
            fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
        else:
            axs2.plot(b.time,b,'-')#, label=f'{s[j]} (Lon={round(x0,2)}; Lat={round(y0,2)})')   #label=f'{VAR} at {s[j]}')
            #df.resample('M').mean().plot(ax=axs2,label=f'{VAR} resample reports the average of previous Month')
            fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
        axs2.legend()
        axs2.grid()
        plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
                                    #random.seed(10)
                                    #x1=range(100)
                                    #random.seed(11)
                                    #x2=np.random.normal(0, 0.8, 100)
                                    #axs2.plot(x1,x2)
    #plt.show()
    #plt.tight_layout(pad=1.0, w_pad=1.0, h_pad=1.0)
    #fig.set_constrained_layout_pads() #pad=0.4, w_pad=0.5, h_pad=1.0
    return [x0, y0],SHOWPLT(fig=fig,conteneur=conteneur),
  
############################################
def plot_map_fill_multiples_ids(title, city, sf, 
                                               x_lim = None, 
                                               y_lim = None, 
                                               figsize = (11,9), 
                                               color = 'r'):
  
    
    plt.figure(figsize = figsize)
    fig, ax = plt.subplots(figsize = figsize)
    fig.suptitle(title, fontsize=16)
    for shape in sf.shapeRecords():
        x = [i[0] for i in shape.shape.points[:]]
        y = [i[1] for i in shape.shape.points[:]]
        ax.plot(x, y, 'k')
            
    for id in city:
        shape_ex = sf.shape(id)
        x_lon = np.zeros((len(shape_ex.points),1))
        y_lat = np.zeros((len(shape_ex.points),1))
        for ip in range(len(shape_ex.points)):
            x_lon[ip] = shape_ex.points[ip][0]
            y_lat[ip] = shape_ex.points[ip][1]
        ax.fill(x_lon,y_lat, color)
             
        x0 = np.mean(x_lon)
        y0 = np.mean(y_lat)
        plt.text(x0, y0, id, fontsize=10)
    
    if (x_lim != None) & (y_lim != None):     
        plt.xlim(x_lim)
        plt.ylim(y_lim)









#BOXPLOT
def BOXPLOT(id, ShapeFilecontry,s,conteneur,data,startdate,enddate,x_lim = None,y_lim = None,figsize = (17,12),color = 'y'):
    

    print(f'startdate={startdate}, enddate={enddate}')
    sf = shp.Reader(ShapeFilecontry)
    #plt.figure(figsize = figsize)
    fig = plt.figure(figsize=figsize, constrained_layout=True)
    gs = fig.add_gridspec(4, 12)

    #fig.suptitle(f'{nom}', fontweight='bold', fontsize=20)
    fig.suptitle(f'{s}', fontweight='bold', fontsize=20)
    axs1= fig.add_subplot(gs[:, 0:3])
    axs2=fig.add_subplot(gs[:, 4:])
    #axs3=fig.add_subplot(gs[1, 0:7])
    for shape in sf.shapeRecords():
        x = [i[0] for i in shape.shape.points[:]]
        y = [i[1] for i in shape.shape.points[:]]
        axs1.plot(x, y, 'k')
        
    shape_ex = sf.shape(id)
    x_lon = np.zeros((len(shape_ex.points),1))
    y_lat = np.zeros((len(shape_ex.points),1))
    for ip in range(len(shape_ex.points)):
        x_lon[ip] = shape_ex.points[ip][0]
        y_lat[ip] = shape_ex.points[ip][1]
    axs1.fill(x_lon,y_lat, color)
    
    if (x_lim != None) & (y_lim != None):     
        axs1.xlim(x_lim)
        axs1.ylim(y_lim)#
        axs1.plot_map_fill(0, sf, x_lim, y_lim, color='y')
        #axs1.plot_map_fill(13, sf,color='y') 

    ###########################
    shape_ex = sf.shape(id)#NP.ZERO initializes an array of rows and column with 0 in place of each elements 
    #an array will be generated where number of rows will be(len(shape_ex,point))and number of columns will be 1 and stored into the variable
    x_lon = np.zeros((len(shape_ex.points),1))#an array will be generated where number of rows will be(len(shape_ex,point))and number of columns will be 1 and stored into the variable
    y_lat = np.zeros((len(shape_ex.points),1))
    for ip in range(len(shape_ex.points)):
        x_lon[ip] = shape_ex.points[ip][0]
        y_lat[ip] = shape_ex.points[ip][1]#plotting using the derived coordinated stored in array created by numpy
    x0 = np.mean(x_lon)
    y0 = np.mean(y_lat)
    axs1.plot(x0,y0,'o', color='red', label=f'Mean point (Lon={round(x0,2)}; Lat={round(y0,2)})')
    #axs2.plot(x_lon,y_lat,label=f'{x0,y0}',color='y')
    axs1.grid()
    axs1.legend()
    #axs2.text(x0, y0, s, fontsize=10)# use bbox (bounding box) to set plot limits
    #plt.xlim(shape_ex.bbox[0],shape_ex.bbox[2])

    path=data
    ncf = netCDF4.Dataset(path, 'r')
    dataset = xr.open_dataset(path)
    #
    # all_times variable includes the time:units attribute
    lats = ncf.variables['latitude'][:] 
    lons = ncf.variables['longitude'][:]
    #
    indexlat = np.argmin( np.abs( lats - x0))
    indexlon = np.argmin( np.abs( lons - y0))
    if dataset.mx2t[0,0,0]>200:
        b=dataset.mx2t[:,indexlat,indexlon].sel(time=slice(startdate,enddate))-273.15
    else:
        b=dataset.mx2t[:,indexlat,indexlon].sel(time=slice(startdate,enddate))
    #plt.plot(dataset.time[:],b)
    axs2.boxplot(b.time,b)
    axs2.grid()
                                #random.seed(10)
                                #x1=range(100)
                                #random.seed(11)
                                #x2=np.random.normal(0, 0.8, 100)
                                #axs2.plot(x1,x2)
    #plt.show()
    #plt.tight_layout(pad=1.0, w_pad=1.0, h_pad=1.0)
    #fig.set_constrained_layout_pads() #pad=0.4, w_pad=0.5, h_pad=1.0
    return [x0, y0],SHOWPLT(fig=fig,conteneur=conteneur),

def TimeSeriesT(id, ShapeFilecontry,s,conteneur,data,startdate,enddate,listEnddate,listsartdate,VAR,x_lim = None,y_lim = None,figsize = (17,12),color = 'y'):
    cdo=Cdo()
    cdo.chname(VAR,'Var_xr', input=data, output='ERA5/outputERA5/dataLastTimeSeriesT.nc')
    path='ERA5/outputERA5/dataLastTimeSeriesT.nc'
    print(f'startdate={startdate}, enddate={enddate}')
    print(ShapeFilecontry)
    
            #plt.figure(figsize = figsize)
    fig = plt.figure(figsize=figsize, constrained_layout=True)
    gs = fig.add_gridspec(4, 12)

    #fig.suptitle(f'{nom}', fontweight='bold', fontsize=20)
   
    axs1= fig.add_subplot(gs[:, 0:3])
    axs2=fig.add_subplot(gs[:, 4:])
    for j in range(len(id)):
        sf = shp.Reader(ShapeFilecontry[j])
        

        #axs3=fig.add_subplot(gs[1, 0:7])
        for shape in sf.shapeRecords():
            x = [i[0] for i in shape.shape.points[:]]
            y = [i[1] for i in shape.shape.points[:]]
            axs1.plot(x, y, 'k')
            
        shape_ex = sf.shape(id[j])
        x_lon = np.zeros((len(shape_ex.points),1))
        y_lat = np.zeros((len(shape_ex.points),1))
        for ip in range(len(shape_ex.points)):
            x_lon[ip] = shape_ex.points[ip][0]
            y_lat[ip] = shape_ex.points[ip][1]
        axs1.fill(x_lon,y_lat, color)
        
        if (x_lim != None) & (y_lim != None):     
            axs1.xlim(x_lim)
            axs1.ylim(y_lim)#
            axs1.plot_map_fill(0, sf, x_lim, y_lim)
            #axs1.plot_map_fill(13, sf,color='y') 

        ###########################
        shape_ex = sf.shape(id[j])#NP.ZERO initializes an array of rows and column with 0 in place of each elements 
        #an array will be generated where number of rows will be(len(shape_ex,point))and number of columns will be 1 and stored into the variable
        x_lon = np.zeros((len(shape_ex.points),1))#an array will be generated where number of rows will be(len(shape_ex,point))and number of columns will be 1 and stored into the variable
        y_lat = np.zeros((len(shape_ex.points),1))
        for ip in range(len(shape_ex.points)):
            x_lon[ip] = shape_ex.points[ip][0]
            y_lat[ip] = shape_ex.points[ip][1]#plotting using the derived coordinated stored in array created by numpy
        x0 = np.mean(x_lon)
        y0 = np.mean(y_lat)
        axs1.plot(x0,y0,'o', label=f'{s[j]} (Lon={round(x0,2)}; Lat={round(y0,2)})')
        #axs2.plot(x_lon,y_lat,label=f'{x0,y0}',color='y')
        axs1.grid()
        axs1.legend()
        #axs2.text(x0, y0, s[j], fontsize=10)# use bbox (bounding box) to set plot limits
        #plt.xlim(shape_ex.bbox[0],shape_ex.bbox[2])

        
        ncf = netCDF4.Dataset(path, 'r')
        dataset = xr.open_dataset(path)
        #
        # all_times variable includes the time:units attribute
        
        varlL = ncf.variables['Var_xr']

        Lon_lat_notation=varlL.dimensions
        for i in Lon_lat_notation:
            if i=='lat':
                lats=ncf.variables["lat"][:]
            if i=='latitude':
                lats = ncf.variables["latitude"][:]
            if i=='lon':
                lons=ncf.variables["lon"][:]
            if i=='longitude':
                lons=ncf.variables["longitude"][:]
            else:
                lats= ncf.variables[Lon_lat_notation[-2]][:]
                lons=ncf.variables[Lon_lat_notation[-1]][:]
        #
        indexlat = np.argmin( np.abs( lats - x0))
        indexlon = np.argmin( np.abs( lons - y0))

        #if dataset.Var_xr[0,0,0]>200:
            #b=dataset.Var_xr[:,indexlat,indexlon].sel(time=slice(startdate,enddate))-273.15
        #else:
        print(listsartdate)
        print(listEnddate)
        #print(startdate2)
        #print(startdate3)
        #print(startdate4)
        #print(enddate1)
    #for i in range(len(listsartdate)) and i in range(len(listEnddate)):
        b1=dataset.Var_xr[:,indexlat,indexlon].sel(time=slice(listsartdate[0],listEnddate[0]))
        b2=dataset.Var_xr[:,indexlat,indexlon].sel(time=slice(listsartdate[1],listEnddate[1]))
        
        #b4=dataset.Var_xr[:,indexlat,indexlon].sel(time=slice(listsartdate[3],listEnddate[3]))
        #b5=dataset.Var_xr[:,indexlat,indexlon].sel(time=slice(listsartdate[4],listEnddate[4]))
    #plt.plot(dataset.time[:],b)
    
        data1=b2
        #Index=pd.date_range(startdate,enddate)
        #mx2t=pd.Series(data1,index=Index)
        #dataf=pd.DataFrame({'var':mx2t})
        #df=dataf['var']
        #dtmean=[np.mean(b) for i in range(len(b))]
   # labels = ['JAN','FEB','MAR','APR','MAY','JUN','JULY','AUG','SEP','OCT','NOV','DEC']startdate,enddate
        
        if len(listEnddate) ==2 and  len(listsartdate)==2:
            #if len(b.time)==1:
            if len(id)>1:
                if f'{startdate[5]}'==0 and f'{startdate[6]}'==1:
                    labels = ['JAN']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                if f'{startdate[6]}'=='1' and f'{startdate[5]}'=='0' and f'{enddate[6]}'=='2' and f'{enddate[5]}'=='0':
                    labels = ['JAN','FEB']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='1' and  f'{startdate[5]}'=='0' and f'{enddate[6]}'=='3':
                    labels = ['JAN','FEB','MAR']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='1' and f'{startdate[5]}'=='0' and f'{enddate[6]}'=='4':
                    labels = ['JAN','FEB','MAR','APR']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                if f'{startdate[6]}'=='1' and f'{startdate[5]}'=='0' and f'{enddate[6]}'=='5':
                    labels = ['JAN','FEB','MAR','APR','MAY']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='1' and f'{startdate[5]}'=='0' f'{enddate[6]}'=='6':
                    labels = ['JAN','FEB','MAR','APR','MAY','JUN']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='1' and f'{startdate[5]}'=='0' and f'{enddate[6]}'=='7':
                    labels = ['JAN','FEB','MAR','APR','MAY','JUN','JULY']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='1' and f'{startdate[5]}'=='0' and f'{enddate[6]}'=='8':
                    labels = ['JAN','FEB','MAR','APR','MAY','JUN','JULY','AUG']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='1' and  f'{startdate[5]}'=='0' and f'{enddate[6]}'=='9':
                    labels = ['JAN','FEB','MAR','APR','MAY','JUN','JULY','AUG','SEP']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='1'  and f'{startdate[5]}'=='0'and f'{enddate[6]}'=='0':
                    labels = ['JAN','FEB','MAR','APR','MAY','JUN','JULY','AUG','SEP','OCT']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='1'  and f'{startdate[5]}'=='0' and'{enddate[5]}'=='1' and f'{enddate[6]}'=='1':
                    labels = ['JAN','FEB','MAR','APR','MAY','JUN','JULY','AUG','SEP','OCT','NOV']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='1' and f'{startdate[5]}'=='0' and f'{enddate[5]}'=='1'  and f'{enddate[6]}'=='2':
                    labels = ['JAN','FEB','MAR','APR','MAY','JUN','JULY','AUG','SEP','OCT','NOV','DEC']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='2' and f'{enddate[6]}'=='3' and f'{startdate[5]}'=='0':
                    labels = ['FEB','MAR']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='2' and f'{enddate[6]}'=='4'and f'{startdate[5]}'=='0':
                    labels = ['FEB','MAR','APR']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='2' and f'{enddate[6]}'=='5' and f'{startdate[5]}'=='0':
                    labels = ['FEB','MAR','APR','MAY']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='2' and f'{enddate[6]}'=='6' and f'{startdate[5]}'=='0':
                    labels = ['FEB','MAR','APR','MAY','JUN']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='2' and f'{enddate[6]}'=='7' and f'{startdate[5]}'=='0':
                    labels = ['FEB','MAR','APR','MAY','JUN','JULY']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='2' and f'{enddate[6]}'=='8' and f'{startdate[5]}'=='0':
                    labels = ['FEB','MAR','APR','MAY','JUN','JULY','AUG']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='2' and f'{enddate[6]}'=='9' and f'{startdate[5]}'=='0':
                    labels = ['FEB','MAR','APR','MAY','JUN','JULY','AUG','SEP']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='2' and f'{enddate[6]}'=='0' and f'{startdate[5]}'=='0':
                    labels = ['FEB','MAR','APR','MAY','JUN','JULY','AUG','SEP','OCT']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='2' and f'{enddate[5]}'=='1' and f'{enddate[6]}'=='1'and f'{startdate[5]}'=='0':
                    labels = ['FEB','MAR','APR','MAY','JUN','JULY','AUG','SEP','OCT','NOV']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='2' and f'{enddate[5]}'=='1' and f'{enddate[6]}'=='2'and f'{startdate[5]}'=='0':
                    labels = ['FEB','MAR','APR','MAY','JUN','JULY','AUG','SEP','OCT','NOV','DEC']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='3' and f'{enddate[6]}'=='4':
                    labels = ['MAR','APR']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='3' and f'{enddate[6]}'=='5':
                    labels = ['MAR','APR','MAY']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='3' and f'{enddate[6]}'=='6':
                    labels = ['MAR','APR','MAY','JUN']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='3' and f'{enddate[6]}'=='7':
                    labels = ['MAR','APR','MAY','JUN','JULY']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='3' and f'{enddate[6]}'=='8':
                    labels = ['MAR','APR','MAY','JUN','JULY','AUG']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='3' and f'{enddate[6]}'=='9':
                    labels = ['MAR','APR','MAY','JUN','JULY','AUG','SEP']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')              
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='3'  and f'{enddate[6]}'=='0':
                    labels = ['MAR','APR','MAY','JUN','JULY','AUG','SEP','OCT']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='3' and f'{enddate[5]}'=='1' and f'{enddate[6]}'=='1':
                    labels = ['MAR','APR','MAY','JUN','JULY','AUG','SEP','OCT','NOV']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='3' and f'{enddate[5]}'=='1' and f'{enddate[6]}'=='2':
                    labels = ['MAR','APR','MAY','JUN','JULY','AUG','SEP','OCT','NOV','DEC']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='4' and f'{enddate[6]}'=='5':
                    labels = ['APR','MAY']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='4' and f'{enddate[6]}'=='6':
                    labels = ['APR','MAY','JUN']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='4' and f'{enddate[6]}'=='7':
                    labels = ['APR','MAY','JUN','JULY']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='4' and f'{enddate[6]}'=='8':
                    labels = ['APR','MAY','JUN','JULY','AUG']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='4' and f'{enddate[6]}'=='9':
                    labels = ['APR','MAY','JUN','JULY','AUG','SEP']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='4'  and f'{enddate[6]}'=='0':
                    labels = ['APR','MAY','JUN','JULY','AUG','SEP','OCT']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='4' and f'{enddate[5]}'=='1' and f'{enddate[6]}'=='1':
                    labels = ['APR','MAY','JUN','JULY','AUG','SEP','OCT','NOV']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='4' and f'{enddate[5]}'=='1' and f'{enddate[6]}'=='2':
                    labels = ['APR','MAY','JUN','JULY','AUG','SEP','OCT','NOV','DEC']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='5' and f'{enddate[6]}'=='6':
                    labels = ['MAY','JUN']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='5' and f'{enddate[6]}'=='7':
                    labels = ['MAY','JUN','JULY']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='5' and f'{enddate[6]}'=='8':
                    labels = ['MAY','JUN','JULY','AUG']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='5' and f'{enddate[6]}'=='9':
                    labels = ['MAY','JUN','JULY','AUG','SEP']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='5' and f'{enddate[6]}'=='0':
                    labels = ['MAY','JUN','JULY','AUG','SEP','OCT']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='5' and f'{enddate[5]}'=='1' and f'{enddate[6]}'=='1':
                    labels = ['MAY','JUN','JULY','AUG','SEP','OCT','NOV']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='5' and f'{enddate[5]}'=='1' and f'{enddate[6]}'=='2':
                    labels = ['MAY','JUN','JULY','AUG','SEP','OCT','NOV','DEC']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='6' and f'{enddate[6]}'=='7':
                    labels = ['JUN','JULY']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    ##axs2.plot(labels,b4,label=f'{startdate4[:4]}')
                    ##axs2.plot(labels,b5,label=f'{startdate5[:4]}')

                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='6' and f'{enddate[6]}'=='8':
                    labels = ['JUN','JULY','AUG']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='6' and f'{enddate[6]}'=='9':
                    labels = ['JUN','JULY','AUG','SEP']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='6'  and f'{enddate[6]}'=='0':
                    labels = ['JUN','JULY','AUG','SEP','OCT']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='6' and f'{enddate[5]}'=='1' and f'{enddate[6]}'=='1':
                    labels = ['JUN','JULY','AUG','SEP','OCT','NOV']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='6' and f'{enddate[5]}'=='1' and f'{enddate[6]}'=='2':
                    labels = ['JUN','JULY','AUG','SEP','OCT','NOV','DEC']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='7' and f'{enddate[6]}'=='8':
                    labels = ['JULY','AUG']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='7' and f'{enddate[6]}'=='9':
                    labels = ['JULY','AUG','SEP']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='7'  and f'{enddate[6]}'=='0':
                    labels = ['JULY','AUG','SEP','OCT']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='7' and f'{enddate[5]}'=='1' and f'{enddate[6]}'=='1':
                    labels = ['JULY','AUG','SEP','OCT','NOV']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='7' and f'{enddate[5]}'=='1' and f'{enddate[6]}'=='2':
                    labels = ['JULY','AUG','SEP','OCT','NOV','DEC']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='8' and f'{enddate[6]}'=='9':
                    labels = ['AUG','SEP']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='8' and f'{enddate[6]}'=='0':
                    labels = ['AUG','SEP','OCT']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='8' and f'{enddate[5]}'=='1' and f'{enddate[6]}'=='1':
                    labels = ['AUG','SEP','OCT','NOV']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='8' and f'{enddate[5]}'=='1' and f'{enddate[6]}'=='2':
                    labels = ['AUG','SEP','OCT','NOV','DEC']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='9' and f'{enddate[6]}'=='0':
                    labels = ['SEP','OCT']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='9' and f'{enddate[5]}'=='1' and f'{enddate[6]}'=='1':
                    labels = ['SEP','OCT','NOV']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='9' and f'{enddate[5]}'=='1' and f'{enddate[6]}'=='2':
                    labels = ['SEP','OCT','NOV','DEC']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='0' and f'{enddate[5]}'=='1' and f'{enddate[6]}'=='1':
                    labels = ['OCT','NOV']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='0' and f'{enddate[5]}'=='1' and f'{enddate[6]}'=='2':
                    labels = ['OCT','NOV','DEC']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[5]}'=='1' and f'{startdate[6]}'=='1' and f'{enddate[5]}'=='1' and f'{enddate[6]}'=='2':
                    labels = ['NOV','DEC']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
            #if len(id)<=1:
                #if f'{startdate[6]}'=='1':
                    #labels = ['JAN']
                    #axs2.plot(labels,b)
                  
                    ##axs2.plot(labels,b4,label=f'{startdate4[:4]}') 
                    ##axs2.plot(labels,b5,label=f'{startdate5[:4]}')

                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            #axs2.legend()
            #axs2.grid
            #plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='1' and f'{enddate[5]}'=='0' and f'{enddate[6]}'=='2':
                    labels = ['JAN','FEB']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='1' and f'{enddate[6]}'=='3' and f'{startdate[5]}'=='0':
                    labels = ['JAN','FEB','MAR']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='1' and f'{enddate[6]}'=='4' and f'{startdate[5]}'=='0':
                    labels = ['JAN','FEB','MAR','APR']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='1' and f'{enddate[6]}'=='5' and f'{startdate[5]}'=='0':
                    labels = ['JAN','FEB','MAR','APR','MAY']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='1' and f'{enddate[6]}'=='6' and f'{startdate[5]}'=='0':
                    labels = ['JAN','FEB','MAR','APR','MAY','JUN']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='1' and f'{enddate[6]}'=='7' and f'{startdate[5]}'=='0':
                    labels = ['JAN','FEB','MAR','APR','MAY','JUN','JULY']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='1' and f'{enddate[6]}'=='8' and f'{startdate[5]}'=='0':
                    labels = ['JAN','FEB','MAR','APR','MAY','JUN','JULY','AUG']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='1' and f'{enddate[6]}'=='9' and f'{startdate[5]}'=='0':
                    labels = ['JAN','FEB','MAR','APR','MAY','JUN','JULY','AUG','SEP']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='1' and f'{enddate[6]}'=='0' and f'{startdate[5]}'=='0':
                    labels = ['JAN','FEB','MAR','APR','MAY','JUN','JULY','AUG','SEP','OCT']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='1' and f'{enddate[5]}'=='1' and f'{enddate[6]}'=='1' and f'{startdate[5]}'=='0':
                    labels = ['JAN','FEB','MAR','APR','MAY','JUN','JULY','AUG','SEP','OCT','NOV']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='1' and f'{enddate[5]}'=='1' and f'{enddate[6]}'=='2' and f'{startdate[5]}'=='0':
                    labels = ['JAN','FEB','MAR','APR','MAY','JUN','JULY','AUG','SEP','OCT','NOV','DEC']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='2' and f'{enddate[6]}'=='3' and f'{startdate[5]}'=='0':
                    labels = ['FEB','MAR']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='2' and f'{enddate[6]}'=='4' and f'{startdate[5]}'=='0':
                    labels = ['FEB','MAR','APR']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='2' and f'{enddate[6]}'=='5' and f'{startdate[5]}'=='0':
                    labels = ['FEB','MAR','APR','MAY']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='2' and f'{enddate[6]}'=='6' and f'{startdate[5]}'=='0':
                    labels = ['FEB','MAR','APR','MAY','JUN']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='2' and f'{enddate[6]}'=='7' and f'{startdate[5]}'=='0':
                    labels = ['FEB','MAR','APR','MAY','JUN','JULY']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='2' and f'{enddate[6]}'=='8' and f'{startdate[5]}'=='0':
                    labels = ['FEB','MAR','APR','MAY','JUN','JULY','AUG']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='2' and f'{enddate[6]}'=='9' and f'{startdate[5]}'=='0':
                    labels = ['FEB','MAR','APR','MAY','JUN','JULY','AUG','SEP']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='2' and f'{enddate[6]}'=='0' and f'{startdate[5]}'=='0':
                    labels = ['FEB','MAR','APR','MAY','JUN','JULY','AUG','SEP','OCT']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='2' and f'{enddate[5]}'=='1' and f'{enddate[6]}'=='1' and f'{startdate[5]}'=='0':
                    labels = ['FEB','MAR','APR','MAY','JUN','JULY','AUG','SEP','OCT','NOV']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='2' and f'{enddate[5]}'=='1' and f'{enddate[6]}'=='2' and f'{startdate[5]}'=='0':
                    labels = ['FEB','MAR','APR','MAY','JUN','JULY','AUG','SEP','OCT','NOV','DEC']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='3' and f'{enddate[6]}'=='4':
                    labels = ['MAR','APR']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='3' and f'{enddate[6]}'=='5':
                    labels = ['MAR','APR','MAY']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='3' and f'{enddate[6]}'=='6':
                    labels = ['MAR','APR','MAY','JUN']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='3' and f'{enddate[6]}'=='7':
                    labels = ['MAR','APR','MAY','JUN','JULY']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='3' and f'{enddate[6]}'=='8':
                    labels = ['MAR','APR','MAY','JUN','JULY','AUG']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='3' and f'{enddate[6]}'=='9':
                    labels = ['MAR','APR','MAY','JUN','JULY','AUG','SEP']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='3'  and f'{enddate[6]}'=='0':
                    labels = ['MAR','APR','MAY','JUN','JULY','AUG','SEP','OCT']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='3' and f'{enddate[5]}'=='1' and f'{enddate[6]}'=='1':
                    labels = ['MAR','APR','MAY','JUN','JULY','AUG','SEP','OCT','NOV']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='3' and f'{enddate[5]}'=='1' and f'{enddate[6]}'=='2':
                    labels = ['MAR','APR','MAY','JUN','JULY','AUG','SEP','OCT','NOV','DEC']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='4' and f'{enddate[6]}'=='5':
                    labels = ['APR','MAY']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')

                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    #axs2.plot(labels,b4,label=f'{startdate4[:4]}')
                  

                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='4' and f'{enddate[6]}'=='6':
                    labels = ['APR','MAY','JUN']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='4' and f'{enddate[6]}'=='7':
                    labels = ['APR','MAY','JUN','JULY']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='4' and f'{enddate[6]}'=='8':
                    labels = ['APR','MAY','JUN','JULY','AUG']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='4' and f'{enddate[6]}'=='9':
                    labels = ['APR','MAY','JUN','JULY','AUG','SEP']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='4'and f'{enddate[6]}'=='0':
                    labels = ['APR','MAY','JUN','JULY','AUG','SEP','OCT']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='4' and f'{enddate[5]}'=='1' and f'{enddate[6]}'=='1':
                    labels = ['APR','MAY','JUN','JULY','AUG','SEP','OCT','NOV']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='4' and f'{enddate[5]}'=='1' and f'{enddate[6]}'=='2':
                    labels = ['APR','MAY','JUN','JULY','AUG','SEP','OCT','NOV','DEC']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='5' and f'{enddate[6]}'=='6':
                    labels = ['MAY','JUN']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='5' and f'{enddate[6]}'=='7':
                    labels = ['MAY','JUN','JULY']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='5' and f'{enddate[6]}'=='8':
                    labels = ['MAY','JUN','JULY','AUG']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='5' and f'{enddate[6]}'=='9':
                    labels = ['MAY','JUN','JULY','AUG','SEP']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='5' and f'{enddate[6]}'=='0':
                    labels = ['MAY','JUN','JULY','AUG','SEP','OCT']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='5' and f'{enddate[5]}'=='1' and f'{enddate[6]}'=='1':
                    labels = ['MAY','JUN','JULY','AUG','SEP','OCT','NOV']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='5' and f'{enddate[5]}'=='1' and f'{enddate[6]}'=='2':
                    labels = ['MAY','JUN','JULY','AUG','SEP','OCT','NOV','DEC']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='6' and f'{enddate[6]}'=='7':
                    labels = ['JUN','JULY']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='6' and f'{enddate[6]}'=='8':
                    labels = ['JUN','JULY','AUG']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='6' and f'{enddate[6]}'=='9':
                    labels = ['JUN','JULY','AUG','SEP']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='6'  and f'{enddate[6]}'=='0':
                    labels = ['JUN','JULY','AUG','SEP','OCT']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='6' and f'{enddate[5]}'=='1' and f'{enddate[6]}'=='1':
                    labels = ['JUN','JULY','AUG','SEP','OCT','NOV']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='6' and f'{enddate[5]}'=='1' and f'{enddate[6]}'=='2':
                    labels = ['JUN','JULY','AUG','SEP','OCT','NOV','DEC']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='7' and f'{enddate[6]}'=='8':
                    labels = ['JULY','AUG']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='7' and f'{enddate[6]}'=='9':
                    labels = ['JULY','AUG','SEP']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='7' and  f'{enddate[6]}'=='0':
                    labels = ['JULY','AUG','SEP','OCT']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='7' and f'{enddate[5]}'=='1' and f'{enddate[6]}'=='1':
                    labels = ['JULY','AUG','SEP','OCT','NOV']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='7' and f'{enddate[5]}'=='1' and f'{enddate[6]}'=='2':
                    labels = ['JULY','AUG','SEP','OCT','NOV','DEC']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='8' and f'{enddate[6]}'=='9':
                    labels = ['AUG','SEP']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='8'  and f'{enddate[6]}'=='0':
                    labels = ['AUG','SEP','OCT']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='8' and f'{enddate[5]}'=='1' and f'{enddate[6]}'=='1':
                    labels = ['AUG','SEP','OCT','NOV']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='8' and f'{enddate[5]}'=='1' and f'{enddate[6]}'=='2':
                    labels = ['AUG','SEP','OCT','NOV','DEC']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='9'  and f'{enddate[6]}'=='0':
                    labels = ['SEP','OCT']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='9' and f'{enddate[5]}'=='1' and f'{enddate[6]}'=='1':
                    labels = ['SEP','OCT','NOV']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='9' and f'{enddate[5]}'=='1' and f'{enddate[6]}'=='2':
                    labels = ['SEP','OCT','NOV','DEC']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if  f'{startdate[6]}'=='0' and f'{enddate[5]}'=='1' and f'{enddate[6]}'=='1':
                    labels = ['OCT','NOV']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='0' and f'{enddate[5]}'=='1' and f'{enddate[6]}'=='2':
                    labels = ['OCT','NOV','DEC']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[5]}'=='1' and f'{startdate[6]}'=='1' and f'{enddate[5]}'=='1' and f'{enddate[6]}'=='2':
                    labels = ['NOV','DEC']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            #if len(id)<=1:
                #labels = ['JAN','FEB','MAR','APR','MAY','JUN','JULY','AUG','SEP','OCT','NOV','DEC']
                #axs2.plot(labels,b,'-')#, label=f'{s[j]} (Lon={round(x0,2)}; Lat={round(y0,2)})')   #label=f'{VAR} at {s[j]}')
                ##df.resample('M').mean().plot(ax=axs2,label=f'{VAR} resample reports the average of previous Month')
                ##axs2.plot(labels,b4,label=f'{startdate4[:4]}') 
                ##axs2.plot(labels,b5,label=f'{startdate5[:4]}')

                #fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            #axs2.legend()
            #axs2.grid()
            #plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
                                        #random.seed(10)
                                        #x1=range(100)
                                        #random.seed(11)
                                        #x2=np.random.normal(0, 0.8, 100)
                                        #axs2.plot(x1,x2)
        #plt.show()
        #plt.tight_layout(pad=1.0, w_pad=1.0, h_pad=1.0)
        #fig.set_constrained_layout_pads() #pad=0.4, w_pad=0.5, h_pad=1.0
        if len(listEnddate) ==3 and  len(listsartdate)==3:
            b3=dataset.Var_xr[:,indexlat,indexlon].sel(time=slice(listsartdate[2],listEnddate[2]))
            if len(id)>1:
                if f'{startdate[5]}'==0 and f'{startdate[6]}'==1:
                    labels = ['JAN']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='1' and f'{startdate[5]}'=='0' and f'{enddate[6]}'=='2' and f'{enddate[5]}'=='0':
                    labels = ['JAN','FEB']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='1' and  f'{startdate[5]}'=='0' and f'{enddate[6]}'=='3':
                    labels = ['JAN','FEB','MAR']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='1' and f'{startdate[5]}'=='0' and f'{enddate[6]}'=='4':
                    labels = ['JAN','FEB','MAR','APR']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='1' and f'{startdate[5]}'=='0' and f'{enddate[6]}'=='5':
                    labels = ['JAN','FEB','MAR','APR','MAY']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='1' and f'{startdate[5]}'=='0' f'{enddate[6]}'=='6':
                    labels = ['JAN','FEB','MAR','APR','MAY','JUN']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='1' and f'{startdate[5]}'=='0' and f'{enddate[6]}'=='7':
                    labels = ['JAN','FEB','MAR','APR','MAY','JUN','JULY']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='1' and f'{startdate[5]}'=='0' and f'{enddate[6]}'=='8':
                    labels = ['JAN','FEB','MAR','APR','MAY','JUN','JULY','AUG']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='1' and  f'{startdate[5]}'=='0' and f'{enddate[6]}'=='9':
                    labels = ['JAN','FEB','MAR','APR','MAY','JUN','JULY','AUG','SEP']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='1'  and f'{startdate[5]}'=='0'and f'{enddate[6]}'=='0':
                    labels = ['JAN','FEB','MAR','APR','MAY','JUN','JULY','AUG','SEP','OCT']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='1'  and f'{startdate[5]}'=='0' and'{enddate[5]}'=='1' and f'{enddate[6]}'=='1':
                    labels = ['JAN','FEB','MAR','APR','MAY','JUN','JULY','AUG','SEP','OCT','NOV']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='1' and f'{enddate[5]}'=='1' and f'{startdate[5]}'=='0' and f'{enddate[6]}'=='2':
                    labels = ['JAN','FEB','MAR','APR','MAY','JUN','JULY','AUG','SEP','OCT','NOV','DEC']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='2' and f'{enddate[6]}'=='3' and f'{startdate[5]}'=='0':
                    labels = ['FEB','MAR']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='2' and f'{enddate[6]}'=='4'and f'{startdate[5]}'=='0':
                    labels = ['FEB','MAR','APR']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='2' and f'{enddate[6]}'=='5' and f'{startdate[5]}'=='0':
                    labels = ['FEB','MAR','APR','MAY']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='2' and f'{enddate[6]}'=='6' and f'{startdate[5]}'=='0':
                    labels = ['FEB','MAR','APR','MAY','JUN']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='2' and f'{enddate[6]}'=='7' and f'{startdate[5]}'=='0':
                    labels = ['FEB','MAR','APR','MAY','JUN','JULY']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='2' and f'{enddate[6]}'=='8' and f'{startdate[5]}'=='0':
                    labels = ['FEB','MAR','APR','MAY','JUN','JULY','AUG']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='2' and f'{enddate[6]}'=='9' and f'{startdate[5]}'=='0':
                    labels = ['FEB','MAR','APR','MAY','JUN','JULY','AUG','SEP']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='2' and f'{enddate[6]}'=='0' and f'{startdate[5]}'=='0':
                    labels = ['FEB','MAR','APR','MAY','JUN','JULY','AUG','SEP','OCT']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='2' and f'{enddate[5]}'=='1' and f'{enddate[6]}'=='1'and f'{startdate[5]}'=='0':
                    labels = ['FEB','MAR','APR','MAY','JUN','JULY','AUG','SEP','OCT','NOV']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='2' and f'{enddate[5]}'=='1' and f'{enddate[6]}'=='2'and f'{startdate[5]}'=='0':
                    labels = ['FEB','MAR','APR','MAY','JUN','JULY','AUG','SEP','OCT','NOV','DEC']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='3' and f'{enddate[6]}'=='4':
                    labels = ['MAR','APR']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='3' and f'{enddate[6]}'=='5':
                    labels = ['MAR','APR','MAY']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='3' and f'{enddate[6]}'=='6':
                    labels = ['MAR','APR','MAY','JUN']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='3' and f'{enddate[6]}'=='7':
                    labels = ['MAR','APR','MAY','JUN','JULY']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='3' and f'{enddate[6]}'=='8':
                    labels = ['MAR','APR','MAY','JUN','JULY','AUG']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='3' and f'{enddate[6]}'=='9':
                    labels = ['MAR','APR','MAY','JUN','JULY','AUG','SEP']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='3'  and f'{enddate[6]}'=='0':
                    labels = ['MAR','APR','MAY','JUN','JULY','AUG','SEP','OCT']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='3' and f'{enddate[5]}'=='1' and f'{enddate[6]}'=='1':
                    labels = ['MAR','APR','MAY','JUN','JULY','AUG','SEP','OCT','NOV']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='3' and f'{enddate[5]}'=='1' and f'{enddate[6]}'=='2':
                    labels = ['MAR','APR','MAY','JUN','JULY','AUG','SEP','OCT','NOV','DEC']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='4' and f'{enddate[6]}'=='5':
                    labels = ['APR','MAY']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='4' and f'{enddate[6]}'=='6':
                    labels = ['APR','MAY','JUN']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='4' and f'{enddate[6]}'=='7':
                    labels = ['APR','MAY','JUN','JULY']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='4' and f'{enddate[6]}'=='8':
                    labels = ['APR','MAY','JUN','JULY','AUG']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='4' and f'{enddate[6]}'=='9':
                    labels = ['APR','MAY','JUN','JULY','AUG','SEP']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='4'  and f'{enddate[6]}'=='0':
                    labels = ['APR','MAY','JUN','JULY','AUG','SEP','OCT']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='4' and f'{enddate[5]}'=='1' and f'{enddate[6]}'=='1':
                    labels = ['APR','MAY','JUN','JULY','AUG','SEP','OCT','NOV']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='4' and f'{enddate[5]}'=='1' and f'{enddate[6]}'=='2':
                    labels = ['APR','MAY','JUN','JULY','AUG','SEP','OCT','NOV','DEC']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='5' and f'{enddate[6]}'=='6':
                    labels = ['MAY','JUN']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='5' and f'{enddate[6]}'=='7':
                    labels = ['MAY','JUN','JULY']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='5' and f'{enddate[6]}'=='8':
                    labels = ['MAY','JUN','JULY','AUG']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='5' and f'{enddate[6]}'=='9':
                    labels = ['MAY','JUN','JULY','AUG','SEP']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='5' and f'{enddate[6]}'=='0':
                    labels = ['MAY','JUN','JULY','AUG','SEP','OCT']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='5' and f'{enddate[5]}'=='1' and f'{enddate[6]}'=='1':
                    labels = ['MAY','JUN','JULY','AUG','SEP','OCT','NOV']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='5' and f'{enddate[5]}'=='1' and f'{enddate[6]}'=='2':
                    labels = ['MAY','JUN','JULY','AUG','SEP','OCT','NOV','DEC']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='6' and f'{enddate[6]}'=='7':
                    labels = ['JUN','JULY']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='6' and f'{enddate[6]}'=='8':
                    labels = ['JUN','JULY','AUG']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='6' and f'{enddate[6]}'=='9':
                    labels = ['JUN','JULY','AUG','SEP']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='6'  and f'{enddate[6]}'=='0':
                    labels = ['JUN','JULY','AUG','SEP','OCT']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='6' and f'{enddate[5]}'=='1' and f'{enddate[6]}'=='1':
                    labels = ['JUN','JULY','AUG','SEP','OCT','NOV']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='6' and f'{enddate[5]}'=='1' and f'{enddate[6]}'=='2':
                    labels = ['JUN','JULY','AUG','SEP','OCT','NOV','DEC']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='7' and f'{enddate[6]}'=='8':
                    labels = ['JULY','AUG']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='7' and f'{enddate[6]}'=='9':
                    labels = ['JULY','AUG','SEP']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='7'  and f'{enddate[6]}'=='0':
                    labels = ['JULY','AUG','SEP','OCT']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='7' and f'{enddate[5]}'=='1' and f'{enddate[6]}'=='1':
                    labels = ['JULY','AUG','SEP','OCT','NOV']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='7' and f'{enddate[5]}'=='1' and f'{enddate[6]}'=='2':
                    labels = ['JULY','AUG','SEP','OCT','NOV','DEC']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='8' and f'{enddate[6]}'=='9':
                    labels = ['AUG','SEP']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='8' and f'{enddate[6]}'=='0':
                    labels = ['AUG','SEP','OCT']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='8' and f'{enddate[5]}'=='1' and f'{enddate[6]}'=='1':
                    labels = ['AUG','SEP','OCT','NOV']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='8' and f'{enddate[5]}'=='1' and f'{enddate[6]}'=='2':
                    labels = ['AUG','SEP','OCT','NOV','DEC']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='9' and f'{enddate[6]}'=='0':
                    labels = ['SEP','OCT']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='9' and f'{enddate[5]}'=='1' and f'{enddate[6]}'=='1':
                    labels = ['SEP','OCT','NOV']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='9' and f'{enddate[5]}'=='1' and f'{enddate[6]}'=='2':
                    labels = ['SEP','OCT','NOV','DEC']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='0' and f'{enddate[5]}'=='1' and f'{enddate[6]}'=='1':
                    labels = ['OCT','NOV']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='0' and f'{enddate[5]}'=='1' and f'{enddate[6]}'=='2':
                    labels = ['OCT','NOV','DEC']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[5]}'=='1' and f'{startdate[6]}'=='1' and f'{enddate[5]}'=='1' and f'{enddate[6]}'=='2':
                    labels = ['NOV','DEC']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
            #if len(id)<=1:
                #if f'{startdate[6]}'=='1':
                    #labels = ['JAN']
                    #axs2.plot(labels,b)
                  
                    ##axs2.plot(labels,b4,label=f'{startdate4[:4]}') 
                    ##axs2.plot(labels,b5,label=f'{startdate5[:4]}')

                    #fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            #axs2.legend()
            #axs2.grid
            #plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='1' and f'{enddate[5]}'=='0' and f'{enddate[6]}'=='2':
                    labels = ['JAN','FEB']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='1' and f'{enddate[6]}'=='3' and f'{startdate[5]}'=='0':
                    labels = ['JAN','FEB','MAR']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='1' and f'{enddate[6]}'=='4' and f'{startdate[5]}'=='0':
                    labels = ['JAN','FEB','MAR','APR']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='1' and f'{enddate[6]}'=='5' and f'{startdate[5]}'=='0':
                    labels = ['JAN','FEB','MAR','APR','MAY']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='1' and f'{enddate[6]}'=='6' and f'{startdate[5]}'=='0':
                    labels = ['JAN','FEB','MAR','APR','MAY','JUN']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='1' and f'{enddate[6]}'=='7' and f'{startdate[5]}'=='0':
                    labels = ['JAN','FEB','MAR','APR','MAY','JUN','JULY']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='1' and f'{enddate[6]}'=='8' and f'{startdate[5]}'=='0':
                    labels = ['JAN','FEB','MAR','APR','MAY','JUN','JULY','AUG']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='1' and f'{enddate[6]}'=='9' and f'{startdate[5]}'=='0':
                    labels = ['JAN','FEB','MAR','APR','MAY','JUN','JULY','AUG','SEP']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='1' and f'{enddate[6]}'=='0' and f'{startdate[5]}'=='0':
                    labels = ['JAN','FEB','MAR','APR','MAY','JUN','JULY','AUG','SEP','OCT']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='1' and f'{enddate[5]}'=='1' and f'{enddate[6]}'=='1' and f'{startdate[5]}'=='0':
                    labels = ['JAN','FEB','MAR','APR','MAY','JUN','JULY','AUG','SEP','OCT','NOV']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='1' and f'{enddate[5]}'=='1' and f'{enddate[6]}'=='2' and f'{startdate[5]}'=='0':
                    labels = ['JAN','FEB','MAR','APR','MAY','JUN','JULY','AUG','SEP','OCT','NOV','DEC']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='2' and f'{enddate[6]}'=='3' and f'{startdate[5]}'=='0':
                    labels = ['FEB','MAR']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='2' and f'{enddate[6]}'=='4' and f'{startdate[5]}'=='0':
                    labels = ['FEB','MAR','APR']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='2' and f'{enddate[6]}'=='5' and f'{startdate[5]}'=='0':
                    labels = ['FEB','MAR','APR','MAY']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='2' and f'{enddate[6]}'=='6' and f'{startdate[5]}'=='0':
                    labels = ['FEB','MAR','APR','MAY','JUN']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='2' and f'{enddate[6]}'=='7' and f'{startdate[5]}'=='0':
                    labels = ['FEB','MAR','APR','MAY','JUN','JULY']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='2' and f'{enddate[6]}'=='8' and f'{startdate[5]}'=='0':
                    labels = ['FEB','MAR','APR','MAY','JUN','JULY','AUG']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='2' and f'{enddate[6]}'=='9' and f'{startdate[5]}'=='0':
                    labels = ['FEB','MAR','APR','MAY','JUN','JULY','AUG','SEP']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='2' and f'{enddate[6]}'=='0' and f'{startdate[5]}'=='0':
                    labels = ['FEB','MAR','APR','MAY','JUN','JULY','AUG','SEP','OCT']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='2' and f'{enddate[5]}'=='1' and f'{enddate[6]}'=='1' and f'{startdate[5]}'=='0':
                    labels = ['FEB','MAR','APR','MAY','JUN','JULY','AUG','SEP','OCT','NOV']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='2' and f'{enddate[5]}'=='1' and f'{enddate[6]}'=='2' and f'{startdate[5]}'=='0':
                    labels = ['FEB','MAR','APR','MAY','JUN','JULY','AUG','SEP','OCT','NOV','DEC']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='3' and f'{enddate[6]}'=='4':
                    labels = ['MAR','APR']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='3' and f'{enddate[6]}'=='5':
                    labels = ['MAR','APR','MAY']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='3' and f'{enddate[6]}'=='6':
                    labels = ['MAR','APR','MAY','JUN']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='3' and f'{enddate[6]}'=='7':
                    labels = ['MAR','APR','MAY','JUN','JULY']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='3' and f'{enddate[6]}'=='8':
                    labels = ['MAR','APR','MAY','JUN','JULY','AUG']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='3' and f'{enddate[6]}'=='9':
                    labels = ['MAR','APR','MAY','JUN','JULY','AUG','SEP']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='3'  and f'{enddate[6]}'=='0':
                    labels = ['MAR','APR','MAY','JUN','JULY','AUG','SEP','OCT']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='3' and f'{enddate[5]}'=='1' and f'{enddate[6]}'=='1':
                    labels = ['MAR','APR','MAY','JUN','JULY','AUG','SEP','OCT','NOV']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='3' and f'{enddate[5]}'=='1' and f'{enddate[6]}'=='2':
                    labels = ['MAR','APR','MAY','JUN','JULY','AUG','SEP','OCT','NOV','DEC']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='4' and f'{enddate[6]}'=='5':
                    labels = ['APR','MAY']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='4' and f'{enddate[6]}'=='6':
                    labels = ['APR','MAY','JUN']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='4' and f'{enddate[6]}'=='7':
                    labels = ['APR','MAY','JUN','JULY']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='4' and f'{enddate[6]}'=='8':
                    labels = ['APR','MAY','JUN','JULY','AUG']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='4' and f'{enddate[6]}'=='9':
                    labels = ['APR','MAY','JUN','JULY','AUG','SEP']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='4'and f'{enddate[6]}'=='0':
                    labels = ['APR','MAY','JUN','JULY','AUG','SEP','OCT']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='4' and f'{enddate[5]}'=='1' and f'{enddate[6]}'=='1':
                    labels = ['APR','MAY','JUN','JULY','AUG','SEP','OCT','NOV']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='4' and f'{enddate[5]}'=='1' and f'{enddate[6]}'=='2':
                    labels = ['APR','MAY','JUN','JULY','AUG','SEP','OCT','NOV','DEC']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='5' and f'{enddate[6]}'=='6':
                    labels = ['MAY','JUN']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='5' and f'{enddate[6]}'=='7':
                    labels = ['MAY','JUN','JULY']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='5' and f'{enddate[6]}'=='8':
                    labels = ['MAY','JUN','JULY','AUG']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='5' and f'{enddate[6]}'=='9':
                    labels = ['MAY','JUN','JULY','AUG','SEP']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='5' and f'{enddate[6]}'=='0':
                    labels = ['MAY','JUN','JULY','AUG','SEP','OCT']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='5' and f'{enddate[5]}'=='1' and f'{enddate[6]}'=='1':
                    labels = ['MAY','JUN','JULY','AUG','SEP','OCT','NOV']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='5' and f'{enddate[5]}'=='1' and f'{enddate[6]}'=='2':
                    labels = ['MAY','JUN','JULY','AUG','SEP','OCT','NOV','DEC']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='6' and f'{enddate[6]}'=='7':
                    labels = ['JUN','JULY']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='6' and f'{enddate[6]}'=='8':
                    labels = ['JUN','JULY','AUG']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='6' and f'{enddate[6]}'=='9':
                    labels = ['JUN','JULY','AUG','SEP']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='6'  and f'{enddate[6]}'=='0':
                    labels = ['JUN','JULY','AUG','SEP','OCT']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='6' and f'{enddate[5]}'=='1' and f'{enddate[6]}'=='1':
                    labels = ['JUN','JULY','AUG','SEP','OCT','NOV']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='6' and f'{enddate[5]}'=='1' and f'{enddate[6]}'=='2':
                    labels = ['JUN','JULY','AUG','SEP','OCT','NOV','DEC']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='7' and f'{enddate[6]}'=='8':
                    labels = ['JULY','AUG']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='7' and f'{enddate[6]}'=='9':
                    labels = ['JULY','AUG','SEP']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='7' and  f'{enddate[6]}'=='0':
                    labels = ['JULY','AUG','SEP','OCT']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='7' and f'{enddate[5]}'=='1' and f'{enddate[6]}'=='1':
                    labels = ['JULY','AUG','SEP','OCT','NOV']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='7' and f'{enddate[5]}'=='1' and f'{enddate[6]}'=='2':
                    labels = ['JULY','AUG','SEP','OCT','NOV','DEC']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='8' and f'{enddate[6]}'=='9':
                    labels = ['AUG','SEP']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='8'  and f'{enddate[6]}'=='0':
                    labels = ['AUG','SEP','OCT']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='8' and f'{enddate[5]}'=='1' and f'{enddate[6]}'=='1':
                    labels = ['AUG','SEP','OCT','NOV']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='8' and f'{enddate[5]}'=='1' and f'{enddate[6]}'=='2':
                    labels = ['AUG','SEP','OCT','NOV','DEC']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='9'  and f'{enddate[6]}'=='0':
                    labels = ['SEP','OCT']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='9' and f'{enddate[5]}'=='1' and f'{enddate[6]}'=='1':
                    labels = ['SEP','OCT','NOV']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='9' and f'{enddate[5]}'=='1' and f'{enddate[6]}'=='2':
                    labels = ['SEP','OCT','NOV','DEC']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if  f'{startdate[6]}'=='0' and f'{enddate[5]}'=='1' and f'{enddate[6]}'=='1':
                    labels = ['OCT','NOV']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='0' and f'{enddate[5]}'=='1' and f'{enddate[6]}'=='2':
                    labels = ['OCT','NOV','DEC']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[5]}'=='1' and f'{startdate[6]}'=='1' and f'{enddate[5]}'=='1' and f'{enddate[6]}'=='2':
                    labels = ['NOV','DEC']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            
        if len(listEnddate) ==4 and  len(listsartdate)==4:
            b3=dataset.Var_xr[:,indexlat,indexlon].sel(time=slice(listsartdate[2],listEnddate[2]))
            b4=dataset.Var_xr[:,indexlat,indexlon].sel(time=slice(listsartdate[3],listEnddate[3]))
            if len(id)>1:
                if f'{startdate[5]}'==0 and f'{startdate[6]}'==1:
                    labels = ['JAN']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                if f'{startdate[6]}'=='1' and f'{startdate[5]}'=='0' and f'{enddate[6]}'=='2' and f'{enddate[5]}'=='0':
                    labels = ['JAN','FEB']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='1' and  f'{startdate[5]}'=='0' and f'{enddate[6]}'=='3':
                    labels = ['JAN','FEB','MAR']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='1' and f'{startdate[5]}'=='0' and f'{enddate[6]}'=='4':
                    labels = ['JAN','FEB','MAR','APR']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='1' and f'{startdate[5]}'=='0' and f'{enddate[6]}'=='5':
                    labels = ['JAN','FEB','MAR','APR','MAY']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='1' and f'{startdate[5]}'=='0' f'{enddate[6]}'=='6':
                    labels = ['JAN','FEB','MAR','APR','MAY','JUN']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='1' and f'{startdate[5]}'=='0' and f'{enddate[6]}'=='7':
                    labels = ['JAN','FEB','MAR','APR','MAY','JUN','JULY']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='1' and f'{startdate[5]}'=='0' and f'{enddate[6]}'=='8':
                    labels = ['JAN','FEB','MAR','APR','MAY','JUN','JULY','AUG']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='1' and  f'{startdate[5]}'=='0' and f'{enddate[6]}'=='9':
                    labels = ['JAN','FEB','MAR','APR','MAY','JUN','JULY','AUG','SEP']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='1'  and f'{startdate[5]}'=='0'and f'{enddate[6]}'=='0':
                    labels = ['JAN','FEB','MAR','APR','MAY','JUN','JULY','AUG','SEP','OCT']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='1'  and f'{startdate[5]}'=='0' and'{enddate[5]}'=='1' and f'{enddate[6]}'=='1':
                    labels = ['JAN','FEB','MAR','APR','MAY','JUN','JULY','AUG','SEP','OCT','NOV']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='1' and f'{enddate[5]}'=='1' and f'{startdate[5]}'=='0' and f'{enddate[6]}'=='2':
                    labels = ['JAN','FEB','MAR','APR','MAY','JUN','JULY','AUG','SEP','OCT','NOV','DEC']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='2' and f'{enddate[6]}'=='3' and f'{startdate[5]}'=='0':
                    labels = ['FEB','MAR']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='2' and f'{enddate[6]}'=='4'and f'{startdate[5]}'=='0':
                    labels = ['FEB','MAR','APR']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='2' and f'{enddate[6]}'=='5' and f'{startdate[5]}'=='0':
                    labels = ['FEB','MAR','APR','MAY']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='2' and f'{enddate[6]}'=='6' and f'{startdate[5]}'=='0':
                    labels = ['FEB','MAR','APR','MAY','JUN']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='2' and f'{enddate[6]}'=='7' and f'{startdate[5]}'=='0':
                    labels = ['FEB','MAR','APR','MAY','JUN','JULY']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='2' and f'{enddate[6]}'=='8' and f'{startdate[5]}'=='0':
                    labels = ['FEB','MAR','APR','MAY','JUN','JULY','AUG']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='2' and f'{enddate[6]}'=='9' and f'{startdate[5]}'=='0':
                    labels = ['FEB','MAR','APR','MAY','JUN','JULY','AUG','SEP']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='2' and f'{enddate[6]}'=='0' and f'{startdate[5]}'=='0':
                    labels = ['FEB','MAR','APR','MAY','JUN','JULY','AUG','SEP','OCT']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='2' and f'{enddate[5]}'=='1' and f'{enddate[6]}'=='1'and f'{startdate[5]}'=='0':
                    labels = ['FEB','MAR','APR','MAY','JUN','JULY','AUG','SEP','OCT','NOV']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='2' and f'{enddate[5]}'=='1' and f'{enddate[6]}'=='2'and f'{startdate[5]}'=='0':
                    labels = ['FEB','MAR','APR','MAY','JUN','JULY','AUG','SEP','OCT','NOV','DEC']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='3' and f'{enddate[6]}'=='4':
                    labels = ['MAR','APR']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='3' and f'{enddate[6]}'=='5':
                    labels = ['MAR','APR','MAY']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='3' and f'{enddate[6]}'=='6':
                    labels = ['MAR','APR','MAY','JUN']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='3' and f'{enddate[6]}'=='7':
                    labels = ['MAR','APR','MAY','JUN','JULY']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='3' and f'{enddate[6]}'=='8':
                    labels = ['MAR','APR','MAY','JUN','JULY','AUG']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='3' and f'{enddate[6]}'=='9':
                    labels = ['MAR','APR','MAY','JUN','JULY','AUG','SEP']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='3'  and f'{enddate[6]}'=='0':
                    labels = ['MAR','APR','MAY','JUN','JULY','AUG','SEP','OCT']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='3' and f'{enddate[5]}'=='1' and f'{enddate[6]}'=='1':
                    labels = ['MAR','APR','MAY','JUN','JULY','AUG','SEP','OCT','NOV']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='3' and f'{enddate[5]}'=='1' and f'{enddate[6]}'=='2':
                    labels = ['MAR','APR','MAY','JUN','JULY','AUG','SEP','OCT','NOV','DEC']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='4' and f'{enddate[6]}'=='5':
                    labels = ['APR','MAY']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='4' and f'{enddate[6]}'=='6':
                    labels = ['APR','MAY','JUN']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='4' and f'{enddate[6]}'=='7':
                    labels = ['APR','MAY','JUN','JULY']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='4' and f'{enddate[6]}'=='8':
                    labels = ['APR','MAY','JUN','JULY','AUG']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='4' and f'{enddate[6]}'=='9':
                    labels = ['APR','MAY','JUN','JULY','AUG','SEP']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='4'  and f'{enddate[6]}'=='0':
                    labels = ['APR','MAY','JUN','JULY','AUG','SEP','OCT']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='4' and f'{enddate[5]}'=='1' and f'{enddate[6]}'=='1':
                    labels = ['APR','MAY','JUN','JULY','AUG','SEP','OCT','NOV']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='4' and f'{enddate[5]}'=='1' and f'{enddate[6]}'=='2':
                    labels = ['APR','MAY','JUN','JULY','AUG','SEP','OCT','NOV','DEC']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='5' and f'{enddate[6]}'=='6':
                    labels = ['MAY','JUN']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='5' and f'{enddate[6]}'=='7':
                    labels = ['MAY','JUN','JULY']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='5' and f'{enddate[6]}'=='8':
                    labels = ['MAY','JUN','JULY','AUG']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='5' and f'{enddate[6]}'=='9':
                    labels = ['MAY','JUN','JULY','AUG','SEP']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='5' and f'{enddate[6]}'=='0':
                    labels = ['MAY','JUN','JULY','AUG','SEP','OCT']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='5' and f'{enddate[5]}'=='1' and f'{enddate[6]}'=='1':
                    labels = ['MAY','JUN','JULY','AUG','SEP','OCT','NOV']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='5' and f'{enddate[5]}'=='1' and f'{enddate[6]}'=='2':
                    labels = ['MAY','JUN','JULY','AUG','SEP','OCT','NOV','DEC']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='6' and f'{enddate[6]}'=='7':
                    labels = ['JUN','JULY']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='6' and f'{enddate[6]}'=='8':
                    labels = ['JUN','JULY','AUG']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='6' and f'{enddate[6]}'=='9':
                    labels = ['JUN','JULY','AUG','SEP']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='6'  and f'{enddate[6]}'=='0':
                    labels = ['JUN','JULY','AUG','SEP','OCT']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='6' and f'{enddate[5]}'=='1' and f'{enddate[6]}'=='1':
                    labels = ['JUN','JULY','AUG','SEP','OCT','NOV']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='6' and f'{enddate[5]}'=='1' and f'{enddate[6]}'=='2':
                    labels = ['JUN','JULY','AUG','SEP','OCT','NOV','DEC']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='7' and f'{enddate[6]}'=='8':
                    labels = ['JULY','AUG']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='7' and f'{enddate[6]}'=='9':
                    labels = ['JULY','AUG','SEP']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='7'  and f'{enddate[6]}'=='0':
                    labels = ['JULY','AUG','SEP','OCT']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='7' and f'{enddate[5]}'=='1' and f'{enddate[6]}'=='1':
                    labels = ['JULY','AUG','SEP','OCT','NOV']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='7' and f'{enddate[5]}'=='1' and f'{enddate[6]}'=='2':
                    labels = ['JULY','AUG','SEP','OCT','NOV','DEC']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='8' and f'{enddate[6]}'=='9':
                    labels = ['AUG','SEP']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='8' and f'{enddate[6]}'=='0':
                    labels = ['AUG','SEP','OCT']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='8' and f'{enddate[5]}'=='1' and f'{enddate[6]}'=='1':
                    labels = ['AUG','SEP','OCT','NOV']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='8' and f'{enddate[5]}'=='1' and f'{enddate[6]}'=='2':
                    labels = ['AUG','SEP','OCT','NOV','DEC']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='9' and f'{enddate[6]}'=='0':
                    labels = ['SEP','OCT']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='9' and f'{enddate[5]}'=='1' and f'{enddate[6]}'=='1':
                    labels = ['SEP','OCT','NOV']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='9' and f'{enddate[5]}'=='1' and f'{enddate[6]}'=='2':
                    labels = ['SEP','OCT','NOV','DEC']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='0' and f'{enddate[5]}'=='1' and f'{enddate[6]}'=='1':
                    labels = ['OCT','NOV']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='0' and f'{enddate[5]}'=='1' and f'{enddate[6]}'=='2':
                    labels = ['OCT','NOV','DEC']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[5]}'=='1' and f'{startdate[6]}'=='1' and f'{enddate[5]}'=='1' and f'{enddate[6]}'=='2':
                    labels = ['NOV','DEC']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
            #if len(id)<=1:
                #if f'{startdate[6]}'=='1':
                    #labels = ['JAN']
                    #axs2.plot(labels,b)
                  
                    ##axs2.plot(labels,b4,label=f'{startdate4[:4]}') 
                    ##axs2.plot(labels,b5,label=f'{startdate5[:4]}')

                    #fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            #axs2.legend()
            #axs2.grid
            #plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='1' and f'{enddate[5]}'=='0' and f'{enddate[6]}'=='2':
                    labels = ['JAN','FEB']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='1' and f'{enddate[6]}'=='3' and f'{startdate[5]}'=='0':
                    labels = ['JAN','FEB','MAR']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='1' and f'{enddate[6]}'=='4' and f'{startdate[5]}'=='0':
                    labels = ['JAN','FEB','MAR','APR']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='1' and f'{enddate[6]}'=='5' and f'{startdate[5]}'=='0':
                    labels = ['JAN','FEB','MAR','APR','MAY']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='1' and f'{enddate[6]}'=='6' and f'{startdate[5]}'=='0':
                    labels = ['JAN','FEB','MAR','APR','MAY','JUN']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='1' and f'{enddate[6]}'=='7' and f'{startdate[5]}'=='0':
                    labels = ['JAN','FEB','MAR','APR','MAY','JUN','JULY']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='1' and f'{enddate[6]}'=='8' and f'{startdate[5]}'=='0':
                    labels = ['JAN','FEB','MAR','APR','MAY','JUN','JULY','AUG']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='1' and f'{enddate[6]}'=='9' and f'{startdate[5]}'=='0':
                    labels = ['JAN','FEB','MAR','APR','MAY','JUN','JULY','AUG','SEP']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='1' and f'{enddate[6]}'=='0' and f'{startdate[5]}'=='0':
                    labels = ['JAN','FEB','MAR','APR','MAY','JUN','JULY','AUG','SEP','OCT']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='1' and f'{enddate[5]}'=='1' and f'{enddate[6]}'=='1' and f'{startdate[5]}'=='0':
                    labels = ['JAN','FEB','MAR','APR','MAY','JUN','JULY','AUG','SEP','OCT','NOV']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='1' and f'{enddate[5]}'=='1' and f'{enddate[6]}'=='2' and f'{startdate[5]}'=='0':
                    labels = ['JAN','FEB','MAR','APR','MAY','JUN','JULY','AUG','SEP','OCT','NOV','DEC']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='2' and f'{enddate[6]}'=='3' and f'{startdate[5]}'=='0':
                    labels = ['FEB','MAR']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='2' and f'{enddate[6]}'=='4' and f'{startdate[5]}'=='0':
                    labels = ['FEB','MAR','APR']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='2' and f'{enddate[6]}'=='5' and f'{startdate[5]}'=='0':
                    labels = ['FEB','MAR','APR','MAY']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='2' and f'{enddate[6]}'=='6' and f'{startdate[5]}'=='0':
                    labels = ['FEB','MAR','APR','MAY','JUN']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='2' and f'{enddate[6]}'=='7' and f'{startdate[5]}'=='0':
                    labels = ['FEB','MAR','APR','MAY','JUN','JULY']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='2' and f'{enddate[6]}'=='8' and f'{startdate[5]}'=='0':
                    labels = ['FEB','MAR','APR','MAY','JUN','JULY','AUG']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='2' and f'{enddate[6]}'=='9' and f'{startdate[5]}'=='0':
                    labels = ['FEB','MAR','APR','MAY','JUN','JULY','AUG','SEP']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='2' and f'{enddate[6]}'=='0' and f'{startdate[5]}'=='0':
                    labels = ['FEB','MAR','APR','MAY','JUN','JULY','AUG','SEP','OCT']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='2' and f'{enddate[5]}'=='1' and f'{enddate[6]}'=='1' and f'{startdate[5]}'=='0':
                    labels = ['FEB','MAR','APR','MAY','JUN','JULY','AUG','SEP','OCT','NOV']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='2' and f'{enddate[5]}'=='1' and f'{enddate[6]}'=='2' and f'{startdate[5]}'=='0':
                    labels = ['FEB','MAR','APR','MAY','JUN','JULY','AUG','SEP','OCT','NOV','DEC']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='3' and f'{enddate[6]}'=='4':
                    labels = ['MAR','APR']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='3' and f'{enddate[6]}'=='5':
                    labels = ['MAR','APR','MAY']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='3' and f'{enddate[6]}'=='6':
                    labels = ['MAR','APR','MAY','JUN']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='3' and f'{enddate[6]}'=='7':
                    labels = ['MAR','APR','MAY','JUN','JULY']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='3' and f'{enddate[6]}'=='8':
                    labels = ['MAR','APR','MAY','JUN','JULY','AUG']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='3' and f'{enddate[6]}'=='9':
                    labels = ['MAR','APR','MAY','JUN','JULY','AUG','SEP']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='3'  and f'{enddate[6]}'=='0':
                    labels = ['MAR','APR','MAY','JUN','JULY','AUG','SEP','OCT']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='3' and f'{enddate[5]}'=='1' and f'{enddate[6]}'=='1':
                    labels = ['MAR','APR','MAY','JUN','JULY','AUG','SEP','OCT','NOV']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='3' and f'{enddate[5]}'=='1' and f'{enddate[6]}'=='2':
                    labels = ['MAR','APR','MAY','JUN','JULY','AUG','SEP','OCT','NOV','DEC']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='4' and f'{enddate[6]}'=='5':
                    labels = ['APR','MAY']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='4' and f'{enddate[6]}'=='6':
                    labels = ['APR','MAY','JUN']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='4' and f'{enddate[6]}'=='7':
                    labels = ['APR','MAY','JUN','JULY']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='4' and f'{enddate[6]}'=='8':
                    labels = ['APR','MAY','JUN','JULY','AUG']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='4' and f'{enddate[6]}'=='9':
                    labels = ['APR','MAY','JUN','JULY','AUG','SEP']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='4'and f'{enddate[6]}'=='0':
                    labels = ['APR','MAY','JUN','JULY','AUG','SEP','OCT']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='4' and f'{enddate[5]}'=='1' and f'{enddate[6]}'=='1':
                    labels = ['APR','MAY','JUN','JULY','AUG','SEP','OCT','NOV']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='4' and f'{enddate[5]}'=='1' and f'{enddate[6]}'=='2':
                    labels = ['APR','MAY','JUN','JULY','AUG','SEP','OCT','NOV','DEC']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='5' and f'{enddate[6]}'=='6':
                    labels = ['MAY','JUN']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='5' and f'{enddate[6]}'=='7':
                    labels = ['MAY','JUN','JULY']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='5' and f'{enddate[6]}'=='8':
                    labels = ['MAY','JUN','JULY','AUG']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='5' and f'{enddate[6]}'=='9':
                    labels = ['MAY','JUN','JULY','AUG','SEP']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='5' and f'{enddate[6]}'=='0':
                    labels = ['MAY','JUN','JULY','AUG','SEP','OCT']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='5' and f'{enddate[5]}'=='1' and f'{enddate[6]}'=='1':
                    labels = ['MAY','JUN','JULY','AUG','SEP','OCT','NOV']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='5' and f'{enddate[5]}'=='1' and f'{enddate[6]}'=='2':
                    labels = ['MAY','JUN','JULY','AUG','SEP','OCT','NOV','DEC']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='6' and f'{enddate[6]}'=='7':
                    labels = ['JUN','JULY']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='6' and f'{enddate[6]}'=='8':
                    labels = ['JUN','JULY','AUG']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='6' and f'{enddate[6]}'=='9':
                    labels = ['JUN','JULY','AUG','SEP']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='6'  and f'{enddate[6]}'=='0':
                    labels = ['JUN','JULY','AUG','SEP','OCT']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='6' and f'{enddate[5]}'=='1' and f'{enddate[6]}'=='1':
                    labels = ['JUN','JULY','AUG','SEP','OCT','NOV']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='6' and f'{enddate[5]}'=='1' and f'{enddate[6]}'=='2':
                    labels = ['JUN','JULY','AUG','SEP','OCT','NOV','DEC']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='7' and f'{enddate[6]}'=='8':
                    labels = ['JULY','AUG']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='7' and f'{enddate[6]}'=='9':
                    labels = ['JULY','AUG','SEP']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='7' and  f'{enddate[6]}'=='0':
                    labels = ['JULY','AUG','SEP','OCT']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='7' and f'{enddate[5]}'=='1' and f'{enddate[6]}'=='1':
                    labels = ['JULY','AUG','SEP','OCT','NOV']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='7' and f'{enddate[5]}'=='1' and f'{enddate[6]}'=='2':
                    labels = ['JULY','AUG','SEP','OCT','NOV','DEC']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='8' and f'{enddate[6]}'=='9':
                    labels = ['AUG','SEP']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='8'  and f'{enddate[6]}'=='0':
                    labels = ['AUG','SEP','OCT']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='8' and f'{enddate[5]}'=='1' and f'{enddate[6]}'=='1':
                    labels = ['AUG','SEP','OCT','NOV']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='8' and f'{enddate[5]}'=='1' and f'{enddate[6]}'=='2':
                    labels = ['AUG','SEP','OCT','NOV','DEC']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='9'  and f'{enddate[6]}'=='0':
                    labels = ['SEP','OCT']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')                   
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='9' and f'{enddate[5]}'=='1' and f'{enddate[6]}'=='1':
                    labels = ['SEP','OCT','NOV']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')

                   
                    ##axs2.plot(labels,b5,label=f'{startdate5[:4]}')

                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='9' and f'{enddate[5]}'=='1' and f'{enddate[6]}'=='2':
                    labels = ['SEP','OCT','NOV','DEC']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if  f'{startdate[6]}'=='0' and f'{enddate[5]}'=='1' and f'{enddate[6]}'=='1':
                    labels = ['OCT','NOV']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='0' and f'{enddate[5]}'=='1' and f'{enddate[6]}'=='2':
                    labels = ['OCT','NOV','DEC']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[5]}'=='1' and f'{startdate[6]}'=='1' and f'{enddate[5]}'=='1' and f'{enddate[6]}'=='2':
                    labels = ['NOV','DEC']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
        if len(listEnddate) ==5 and  len(listsartdate)==5:
            b3=dataset.Var_xr[:,indexlat,indexlon].sel(time=slice(listsartdate[2],listEnddate[2]))
            b4=dataset.Var_xr[:,indexlat,indexlon].sel(time=slice(listsartdate[3],listEnddate[3]))
            b5=dataset.Var_xr[:,indexlat,indexlon].sel(time=slice(listsartdate[4],listEnddate[4]))
            if len(id)>1:
                if f'{startdate[5]}'==0 and f'{startdate[6]}'==1:
                    labels = ['JAN']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    axs2.plot(labels,b5,label=f'{listsartdate[4][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                if f'{startdate[6]}'=='1' and f'{startdate[5]}'=='0' and f'{enddate[6]}'=='2' and f'{enddate[5]}'=='0':
                    labels = ['JAN','FEB']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    axs2.plot(labels,b5,label=f'{listsartdate[4][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='1' and  f'{startdate[5]}'=='0' and f'{enddate[6]}'=='3':
                    labels = ['JAN','FEB','MAR']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    axs2.plot(labels,b5,label=f'{listsartdate[4][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='1' and f'{startdate[5]}'=='0' and f'{enddate[6]}'=='4':
                    labels = ['JAN','FEB','MAR','APR']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    axs2.plot(labels,b5,label=f'{listsartdate[4][:4]}')
                if f'{startdate[6]}'=='1' and f'{startdate[5]}'=='0' and f'{enddate[6]}'=='5':
                    labels = ['JAN','FEB','MAR','APR','MAY']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    axs2.plot(labels,b5,label=f'{listsartdate[4][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='1' and f'{startdate[5]}'=='0' f'{enddate[6]}'=='6':
                    labels = ['JAN','FEB','MAR','APR','MAY','JUN']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    axs2.plot(labels,b5,label=f'{listsartdate[4][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='1' and f'{startdate[5]}'=='0' and f'{enddate[6]}'=='7':
                    labels = ['JAN','FEB','MAR','APR','MAY','JUN','JULY']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    axs2.plot(labels,b5,label=f'{listsartdate[4][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='1' and f'{startdate[5]}'=='0' and f'{enddate[6]}'=='8':
                    labels = ['JAN','FEB','MAR','APR','MAY','JUN','JULY','AUG']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    axs2.plot(labels,b5,label=f'{listsartdate[4][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='1' and  f'{startdate[5]}'=='0' and f'{enddate[6]}'=='9':
                    labels = ['JAN','FEB','MAR','APR','MAY','JUN','JULY','AUG','SEP']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    axs2.plot(labels,b5,label=f'{listsartdate[4][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='1'  and f'{startdate[5]}'=='0'and f'{enddate[6]}'=='0':
                    labels = ['JAN','FEB','MAR','APR','MAY','JUN','JULY','AUG','SEP','OCT']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    axs2.plot(labels,b5,label=f'{listsartdate[4][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='1'  and f'{startdate[5]}'=='0' and'{enddate[5]}'=='1' and f'{enddate[6]}'=='1':
                    labels = ['JAN','FEB','MAR','APR','MAY','JUN','JULY','AUG','SEP','OCT','NOV']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    axs2.plot(labels,b5,label=f'{listsartdate[4][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='1' and f'{enddate[5]}'=='1' and f'{startdate[5]}'=='0' and f'{enddate[6]}'=='2':
                    labels = ['JAN','FEB','MAR','APR','MAY','JUN','JULY','AUG','SEP','OCT','NOV','DEC']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    axs2.plot(labels,b5,label=f'{listsartdate[4][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='2' and f'{enddate[6]}'=='3' and f'{startdate[5]}'=='0':
                    labels = ['FEB','MAR']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    axs2.plot(labels,b5,label=f'{listsartdate[4][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='2' and f'{enddate[6]}'=='4'and f'{startdate[5]}'=='0':
                    labels = ['FEB','MAR','APR']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    axs2.plot(labels,b5,label=f'{listsartdate[4][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='2' and f'{enddate[6]}'=='5' and f'{startdate[5]}'=='0':
                    labels = ['FEB','MAR','APR','MAY']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    axs2.plot(labels,b5,label=f'{listsartdate[4][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='2' and f'{enddate[6]}'=='6' and f'{startdate[5]}'=='0':
                    labels = ['FEB','MAR','APR','MAY','JUN']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    axs2.plot(labels,b5,label=f'{listsartdate[4][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='2' and f'{enddate[6]}'=='7' and f'{startdate[5]}'=='0':
                    labels = ['FEB','MAR','APR','MAY','JUN','JULY']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    axs2.plot(labels,b5,label=f'{listsartdate[4][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='2' and f'{enddate[6]}'=='8' and f'{startdate[5]}'=='0':
                    labels = ['FEB','MAR','APR','MAY','JUN','JULY','AUG']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    axs2.plot(labels,b5,label=f'{listsartdate[4][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='2' and f'{enddate[6]}'=='9' and f'{startdate[5]}'=='0':
                    labels = ['FEB','MAR','APR','MAY','JUN','JULY','AUG','SEP']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    axs2.plot(labels,b5,label=f'{listsartdate[4][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='2' and f'{enddate[6]}'=='0' and f'{startdate[5]}'=='0':
                    labels = ['FEB','MAR','APR','MAY','JUN','JULY','AUG','SEP','OCT']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    axs2.plot(labels,b5,label=f'{listsartdate[4][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='2' and f'{enddate[5]}'=='1' and f'{enddate[6]}'=='1'and f'{startdate[5]}'=='0':
                    labels = ['FEB','MAR','APR','MAY','JUN','JULY','AUG','SEP','OCT','NOV']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    axs2.plot(labels,b5,label=f'{listsartdate[4][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='2' and f'{enddate[5]}'=='1' and f'{enddate[6]}'=='2'and f'{startdate[5]}'=='0':
                    labels = ['FEB','MAR','APR','MAY','JUN','JULY','AUG','SEP','OCT','NOV','DEC']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    axs2.plot(labels,b5,label=f'{listsartdate[4][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='3' and f'{enddate[6]}'=='4':
                    labels = ['MAR','APR']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    axs2.plot(labels,b5,label=f'{listsartdate[4][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='3' and f'{enddate[6]}'=='5':
                    labels = ['MAR','APR','MAY']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    axs2.plot(labels,b5,label=f'{listsartdate[4][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='3' and f'{enddate[6]}'=='6':
                    labels = ['MAR','APR','MAY','JUN']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    axs2.plot(labels,b5,label=f'{listsartdate[4][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='3' and f'{enddate[6]}'=='7':
                    labels = ['MAR','APR','MAY','JUN','JULY']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    axs2.plot(labels,b5,label=f'{listsartdate[4][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='3' and f'{enddate[6]}'=='8':
                    labels = ['MAR','APR','MAY','JUN','JULY','AUG']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    axs2.plot(labels,b5,label=f'{listsartdate[4][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='3' and f'{enddate[6]}'=='9':
                    labels = ['MAR','APR','MAY','JUN','JULY','AUG','SEP']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    axs2.plot(labels,b5,label=f'{listsartdate[4][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='3'  and f'{enddate[6]}'=='0':
                    labels = ['MAR','APR','MAY','JUN','JULY','AUG','SEP','OCT']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    axs2.plot(labels,b5,label=f'{listsartdate[4][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='3' and f'{enddate[5]}'=='1' and f'{enddate[6]}'=='1':
                    labels = ['MAR','APR','MAY','JUN','JULY','AUG','SEP','OCT','NOV']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    axs2.plot(labels,b5,label=f'{listsartdate[4][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='3' and f'{enddate[5]}'=='1' and f'{enddate[6]}'=='2':
                    labels = ['MAR','APR','MAY','JUN','JULY','AUG','SEP','OCT','NOV','DEC']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    axs2.plot(labels,b5,label=f'{listsartdate[4][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='4' and f'{enddate[6]}'=='5':
                    labels = ['APR','MAY']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    axs2.plot(labels,b5,label=f'{listsartdate[4][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='4' and f'{enddate[6]}'=='6':
                    labels = ['APR','MAY','JUN']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    axs2.plot(labels,b5,label=f'{listsartdate[4][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='4' and f'{enddate[6]}'=='7':
                    labels = ['APR','MAY','JUN','JULY']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    axs2.plot(labels,b5,label=f'{listsartdate[4][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='4' and f'{enddate[6]}'=='8':
                    labels = ['APR','MAY','JUN','JULY','AUG']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    axs2.plot(labels,b5,label=f'{listsartdate[4][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='4' and f'{enddate[6]}'=='9':
                    labels = ['APR','MAY','JUN','JULY','AUG','SEP']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    axs2.plot(labels,b5,label=f'{listsartdate[4][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='4'  and f'{enddate[6]}'=='0':
                    labels = ['APR','MAY','JUN','JULY','AUG','SEP','OCT']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    axs2.plot(labels,b5,label=f'{listsartdate[4][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='4' and f'{enddate[5]}'=='1' and f'{enddate[6]}'=='1':
                    labels = ['APR','MAY','JUN','JULY','AUG','SEP','OCT','NOV']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    axs2.plot(labels,b5,label=f'{listsartdate[4][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='4' and f'{enddate[5]}'=='1' and f'{enddate[6]}'=='2':
                    labels = ['APR','MAY','JUN','JULY','AUG','SEP','OCT','NOV','DEC']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    axs2.plot(labels,b5,label=f'{listsartdate[4][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='5' and f'{enddate[6]}'=='6':
                    labels = ['MAY','JUN']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    axs2.plot(labels,b5,label=f'{listsartdate[4][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='5' and f'{enddate[6]}'=='7':
                    labels = ['MAY','JUN','JULY']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    axs2.plot(labels,b5,label=f'{listsartdate[4][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='5' and f'{enddate[6]}'=='8':
                    labels = ['MAY','JUN','JULY','AUG']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    axs2.plot(labels,b5,label=f'{listsartdate[4][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='5' and f'{enddate[6]}'=='9':
                    labels = ['MAY','JUN','JULY','AUG','SEP']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    axs2.plot(labels,b5,label=f'{listsartdate[4][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='5' and f'{enddate[6]}'=='0':
                    labels = ['MAY','JUN','JULY','AUG','SEP','OCT']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    axs2.plot(labels,b5,label=f'{listsartdate[4][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='5' and f'{enddate[5]}'=='1' and f'{enddate[6]}'=='1':
                    labels = ['MAY','JUN','JULY','AUG','SEP','OCT','NOV']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    axs2.plot(labels,b5,label=f'{listsartdate[4][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='5' and f'{enddate[5]}'=='1' and f'{enddate[6]}'=='2':
                    labels = ['MAY','JUN','JULY','AUG','SEP','OCT','NOV','DEC']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    axs2.plot(labels,b5,label=f'{listsartdate[4][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='6' and f'{enddate[6]}'=='7':
                    labels = ['JUN','JULY']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    axs2.plot(labels,b5,label=f'{listsartdate[4][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='6' and f'{enddate[6]}'=='8':
                    labels = ['JUN','JULY','AUG']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    axs2.plot(labels,b5,label=f'{listsartdate[4][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='6' and f'{enddate[6]}'=='9':
                    labels = ['JUN','JULY','AUG','SEP']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    axs2.plot(labels,b5,label=f'{listsartdate[4][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='6'  and f'{enddate[6]}'=='0':
                    labels = ['JUN','JULY','AUG','SEP','OCT']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    axs2.plot(labels,b5,label=f'{listsartdate[4][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='6' and f'{enddate[5]}'=='1' and f'{enddate[6]}'=='1':
                    labels = ['JUN','JULY','AUG','SEP','OCT','NOV']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    axs2.plot(labels,b5,label=f'{listsartdate[4][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='6' and f'{enddate[5]}'=='1' and f'{enddate[6]}'=='2':
                    labels = ['JUN','JULY','AUG','SEP','OCT','NOV','DEC']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    axs2.plot(labels,b5,label=f'{listsartdate[4][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='7' and f'{enddate[6]}'=='8':
                    labels = ['JULY','AUG']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    axs2.plot(labels,b5,label=f'{listsartdate[4][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='7' and f'{enddate[6]}'=='9':
                    labels = ['JULY','AUG','SEP']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    axs2.plot(labels,b5,label=f'{listsartdate[4][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='7'  and f'{enddate[6]}'=='0':
                    labels = ['JULY','AUG','SEP','OCT']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    axs2.plot(labels,b5,label=f'{listsartdate[4][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='7' and f'{enddate[5]}'=='1' and f'{enddate[6]}'=='1':
                    labels = ['JULY','AUG','SEP','OCT','NOV']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    axs2.plot(labels,b5,label=f'{listsartdate[4][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='7' and f'{enddate[5]}'=='1' and f'{enddate[6]}'=='2':
                    labels = ['JULY','AUG','SEP','OCT','NOV','DEC']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    axs2.plot(labels,b5,label=f'{listsartdate[4][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='8' and f'{enddate[6]}'=='9':
                    labels = ['AUG','SEP']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    axs2.plot(labels,b5,label=f'{listsartdate[4][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='8' and f'{enddate[6]}'=='0':
                    labels = ['AUG','SEP','OCT']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    axs2.plot(labels,b5,label=f'{listsartdate[4][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='8' and f'{enddate[5]}'=='1' and f'{enddate[6]}'=='1':
                    labels = ['AUG','SEP','OCT','NOV']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    axs2.plot(labels,b5,label=f'{listsartdate[4][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='8' and f'{enddate[5]}'=='1' and f'{enddate[6]}'=='2':
                    labels = ['AUG','SEP','OCT','NOV','DEC']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    axs2.plot(labels,b5,label=f'{listsartdate[4][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='9' and f'{enddate[6]}'=='0':
                    labels = ['SEP','OCT']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    axs2.plot(labels,b5,label=f'{listsartdate[4][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='9' and f'{enddate[5]}'=='1' and f'{enddate[6]}'=='1':
                    labels = ['SEP','OCT','NOV']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    axs2.plot(labels,b5,label=f'{listsartdate[4][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='9' and f'{enddate[5]}'=='1' and f'{enddate[6]}'=='2':
                    labels = ['SEP','OCT','NOV','DEC']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    axs2.plot(labels,b5,label=f'{listsartdate[4][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='0' and f'{enddate[5]}'=='1' and f'{enddate[6]}'=='1':
                    labels = ['OCT','NOV']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    axs2.plot(labels,b5,label=f'{listsartdate[4][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[6]}'=='0' and f'{enddate[5]}'=='1' and f'{enddate[6]}'=='2':
                    labels = ['OCT','NOV','DEC']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    axs2.plot(labels,b5,label=f'{listsartdate[4][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
                if f'{startdate[5]}'=='1' and f'{startdate[6]}'=='1' and f'{enddate[5]}'=='1' and f'{enddate[6]}'=='2':
                    labels = ['NOV','DEC']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    axs2.plot(labels,b5,label=f'{listsartdate[4][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=20)
                    plt.setp(axs2.xaxis.get_majorticklabels(), rotation=30)
            #if len(id)<=1:
                #if f'{startdate[6]}'=='1':
                    #labels = ['JAN']
                    #axs2.plot(labels,b)
                  
                    ##axs2.plot(labels,b4,label=f'{startdate4[:4]}') 
                    ##axs2.plot(labels,b5,label=f'{startdate5[:4]}')

                    #fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            #axs2.legend()
            #axs2.grid
            #plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='1' and f'{enddate[5]}'=='0' and f'{enddate[6]}'=='2':
                    labels = ['JAN','FEB']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    axs2.plot(labels,b5,label=f'{listsartdate[4][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='1' and f'{enddate[6]}'=='3' and f'{startdate[5]}'=='0':
                    labels = ['JAN','FEB','MAR']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    axs2.plot(labels,b5,label=f'{listsartdate[4][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='1' and f'{enddate[6]}'=='4' and f'{startdate[5]}'=='0':
                    labels = ['JAN','FEB','MAR','APR']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    axs2.plot(labels,b5,label=f'{listsartdate[4][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='1' and f'{enddate[6]}'=='5' and f'{startdate[5]}'=='0':
                    labels = ['JAN','FEB','MAR','APR','MAY']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    axs2.plot(labels,b5,label=f'{listsartdate[4][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='1' and f'{enddate[6]}'=='6' and f'{startdate[5]}'=='0':
                    labels = ['JAN','FEB','MAR','APR','MAY','JUN']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    axs2.plot(labels,b5,label=f'{listsartdate[4][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='1' and f'{enddate[6]}'=='7' and f'{startdate[5]}'=='0':
                    labels = ['JAN','FEB','MAR','APR','MAY','JUN','JULY']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    axs2.plot(labels,b5,label=f'{listsartdate[4][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='1' and f'{enddate[6]}'=='8' and f'{startdate[5]}'=='0':
                    labels = ['JAN','FEB','MAR','APR','MAY','JUN','JULY','AUG']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    axs2.plot(labels,b5,label=f'{listsartdate[4][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='1' and f'{enddate[6]}'=='9' and f'{startdate[5]}'=='0':
                    labels = ['JAN','FEB','MAR','APR','MAY','JUN','JULY','AUG','SEP']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    axs2.plot(labels,b5,label=f'{listsartdate[4][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='1' and f'{enddate[6]}'=='0' and f'{startdate[5]}'=='0':
                    labels = ['JAN','FEB','MAR','APR','MAY','JUN','JULY','AUG','SEP','OCT']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    axs2.plot(labels,b5,label=f'{listsartdate[4][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='1' and f'{enddate[5]}'=='1' and f'{enddate[6]}'=='1' and f'{startdate[5]}'=='0':
                    labels = ['JAN','FEB','MAR','APR','MAY','JUN','JULY','AUG','SEP','OCT','NOV']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    axs2.plot(labels,b5,label=f'{listsartdate[4][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='1' and f'{enddate[5]}'=='1' and f'{enddate[6]}'=='2' and f'{startdate[5]}'=='0':
                    labels = ['JAN','FEB','MAR','APR','MAY','JUN','JULY','AUG','SEP','OCT','NOV','DEC']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    axs2.plot(labels,b5,label=f'{listsartdate[4][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='2' and f'{enddate[6]}'=='3' and f'{startdate[5]}'=='0':
                    labels = ['FEB','MAR']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    axs2.plot(labels,b5,label=f'{listsartdate[4][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='2' and f'{enddate[6]}'=='4' and f'{startdate[5]}'=='0':
                    labels = ['FEB','MAR','APR']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    axs2.plot(labels,b5,label=f'{listsartdate[4][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='2' and f'{enddate[6]}'=='5' and f'{startdate[5]}'=='0':
                    labels = ['FEB','MAR','APR','MAY']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    axs2.plot(labels,b5,label=f'{listsartdate[4][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='2' and f'{enddate[6]}'=='6' and f'{startdate[5]}'=='0':
                    labels = ['FEB','MAR','APR','MAY','JUN']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    axs2.plot(labels,b5,label=f'{listsartdate[4][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='2' and f'{enddate[6]}'=='7' and f'{startdate[5]}'=='0':
                    labels = ['FEB','MAR','APR','MAY','JUN','JULY']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    axs2.plot(labels,b5,label=f'{listsartdate[4][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='2' and f'{enddate[6]}'=='8' and f'{startdate[5]}'=='0':
                    labels = ['FEB','MAR','APR','MAY','JUN','JULY','AUG']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    axs2.plot(labels,b5,label=f'{listsartdate[4][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='2' and f'{enddate[6]}'=='9' and f'{startdate[5]}'=='0':
                    labels = ['FEB','MAR','APR','MAY','JUN','JULY','AUG','SEP']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    axs2.plot(labels,b5,label=f'{listsartdate[4][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='2' and f'{enddate[6]}'=='0' and f'{startdate[5]}'=='0':
                    labels = ['FEB','MAR','APR','MAY','JUN','JULY','AUG','SEP','OCT']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    axs2.plot(labels,b5,label=f'{listsartdate[4][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='2' and f'{enddate[5]}'=='1' and f'{enddate[6]}'=='1' and f'{startdate[5]}'=='0':
                    labels = ['FEB','MAR','APR','MAY','JUN','JULY','AUG','SEP','OCT','NOV']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    axs2.plot(labels,b5,label=f'{listsartdate[4][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='2' and f'{enddate[5]}'=='1' and f'{enddate[6]}'=='2' and f'{startdate[5]}'=='0':
                    labels = ['FEB','MAR','APR','MAY','JUN','JULY','AUG','SEP','OCT','NOV','DEC']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    axs2.plot(labels,b5,label=f'{listsartdate[4][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='3' and f'{enddate[6]}'=='4':
                    labels = ['MAR','APR']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    axs2.plot(labels,b5,label=f'{listsartdate[4][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='3' and f'{enddate[6]}'=='5':
                    labels = ['MAR','APR','MAY']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    axs2.plot(labels,b5,label=f'{listsartdate[4][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='3' and f'{enddate[6]}'=='6':
                    labels = ['MAR','APR','MAY','JUN']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    axs2.plot(labels,b5,label=f'{listsartdate[4][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='3' and f'{enddate[6]}'=='7':
                    labels = ['MAR','APR','MAY','JUN','JULY']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    axs2.plot(labels,b5,label=f'{listsartdate[4][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='3' and f'{enddate[6]}'=='8':
                    labels = ['MAR','APR','MAY','JUN','JULY','AUG']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    axs2.plot(labels,b5,label=f'{listsartdate[4][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='3' and f'{enddate[6]}'=='9':
                    labels = ['MAR','APR','MAY','JUN','JULY','AUG','SEP']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    axs2.plot(labels,b5,label=f'{listsartdate[4][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='3'  and f'{enddate[6]}'=='0':
                    labels = ['MAR','APR','MAY','JUN','JULY','AUG','SEP','OCT']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    axs2.plot(labels,b5,label=f'{listsartdate[4][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='3' and f'{enddate[5]}'=='1' and f'{enddate[6]}'=='1':
                    labels = ['MAR','APR','MAY','JUN','JULY','AUG','SEP','OCT','NOV']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    axs2.plot(labels,b5,label=f'{listsartdate[4][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='3' and f'{enddate[5]}'=='1' and f'{enddate[6]}'=='2':
                    labels = ['MAR','APR','MAY','JUN','JULY','AUG','SEP','OCT','NOV','DEC']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    axs2.plot(labels,b5,label=f'{listsartdate[4][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='4' and f'{enddate[6]}'=='5':
                    labels = ['APR','MAY']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    axs2.plot(labels,b5,label=f'{listsartdate[4][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='4' and f'{enddate[6]}'=='6':
                    labels = ['APR','MAY','JUN']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    axs2.plot(labels,b5,label=f'{listsartdate[4][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='4' and f'{enddate[6]}'=='7':
                    labels = ['APR','MAY','JUN','JULY']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    axs2.plot(labels,b5,label=f'{listsartdate[4][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='4' and f'{enddate[6]}'=='8':
                    labels = ['APR','MAY','JUN','JULY','AUG']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    axs2.plot(labels,b5,label=f'{listsartdate[4][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='4' and f'{enddate[6]}'=='9':
                    labels = ['APR','MAY','JUN','JULY','AUG','SEP']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    axs2.plot(labels,b5,label=f'{listsartdate[4][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='4'and f'{enddate[6]}'=='0':
                    labels = ['APR','MAY','JUN','JULY','AUG','SEP','OCT']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    axs2.plot(labels,b5,label=f'{listsartdate[4][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='4' and f'{enddate[5]}'=='1' and f'{enddate[6]}'=='1':
                    labels = ['APR','MAY','JUN','JULY','AUG','SEP','OCT','NOV']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    axs2.plot(labels,b5,label=f'{listsartdate[4][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='4' and f'{enddate[5]}'=='1' and f'{enddate[6]}'=='2':
                    labels = ['APR','MAY','JUN','JULY','AUG','SEP','OCT','NOV','DEC']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    axs2.plot(labels,b5,label=f'{listsartdate[4][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='5' and f'{enddate[6]}'=='6':
                    labels = ['MAY','JUN']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    axs2.plot(labels,b5,label=f'{listsartdate[4][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='5' and f'{enddate[6]}'=='7':
                    labels = ['MAY','JUN','JULY']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    axs2.plot(labels,b5,label=f'{listsartdate[4][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='5' and f'{enddate[6]}'=='8':
                    labels = ['MAY','JUN','JULY','AUG']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    axs2.plot(labels,b5,label=f'{listsartdate[4][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='5' and f'{enddate[6]}'=='9':
                    labels = ['MAY','JUN','JULY','AUG','SEP']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    axs2.plot(labels,b5,label=f'{listsartdate[4][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='5' and f'{enddate[6]}'=='0':
                    labels = ['MAY','JUN','JULY','AUG','SEP','OCT']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    axs2.plot(labels,b5,label=f'{listsartdate[4][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='5' and f'{enddate[5]}'=='1' and f'{enddate[6]}'=='1':
                    labels = ['MAY','JUN','JULY','AUG','SEP','OCT','NOV']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    axs2.plot(labels,b5,label=f'{listsartdate[4][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='5' and f'{enddate[5]}'=='1' and f'{enddate[6]}'=='2':
                    labels = ['MAY','JUN','JULY','AUG','SEP','OCT','NOV','DEC']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    axs2.plot(labels,b5,label=f'{listsartdate[4][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='6' and f'{enddate[6]}'=='7':
                    labels = ['JUN','JULY']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    axs2.plot(labels,b5,label=f'{listsartdate[4][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='6' and f'{enddate[6]}'=='8':
                    labels = ['JUN','JULY','AUG']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    axs2.plot(labels,b5,label=f'{listsartdate[4][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='6' and f'{enddate[6]}'=='9':
                    labels = ['JUN','JULY','AUG','SEP']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    axs2.plot(labels,b5,label=f'{listsartdate[4][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='6'  and f'{enddate[6]}'=='0':
                    labels = ['JUN','JULY','AUG','SEP','OCT']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    axs2.plot(labels,b5,label=f'{listsartdate[4][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='6' and f'{enddate[5]}'=='1' and f'{enddate[6]}'=='1':
                    labels = ['JUN','JULY','AUG','SEP','OCT','NOV']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    axs2.plot(labels,b5,label=f'{listsartdate[4][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='6' and f'{enddate[5]}'=='1' and f'{enddate[6]}'=='2':
                    labels = ['JUN','JULY','AUG','SEP','OCT','NOV','DEC']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    axs2.plot(labels,b5,label=f'{listsartdate[4][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='7' and f'{enddate[6]}'=='8':
                    labels = ['JULY','AUG']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    axs2.plot(labels,b5,label=f'{listsartdate[4][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='7' and f'{enddate[6]}'=='9':
                    labels = ['JULY','AUG','SEP']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    axs2.plot(labels,b5,label=f'{listsartdate[4][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='7' and  f'{enddate[6]}'=='0':
                    labels = ['JULY','AUG','SEP','OCT']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    axs2.plot(labels,b5,label=f'{listsartdate[4][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='7' and f'{enddate[5]}'=='1' and f'{enddate[6]}'=='1':
                    labels = ['JULY','AUG','SEP','OCT','NOV']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    axs2.plot(labels,b5,label=f'{listsartdate[4][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='7' and f'{enddate[5]}'=='1' and f'{enddate[6]}'=='2':
                    labels = ['JULY','AUG','SEP','OCT','NOV','DEC']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    axs2.plot(labels,b5,label=f'{listsartdate[4][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='8' and f'{enddate[6]}'=='9':
                    labels = ['AUG','SEP']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    axs2.plot(labels,b5,label=f'{listsartdate[4][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='8'  and f'{enddate[6]}'=='0':
                    labels = ['AUG','SEP','OCT']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    axs2.plot(labels,b5,label=f'{listsartdate[4][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='8' and f'{enddate[5]}'=='1' and f'{enddate[6]}'=='1':
                    labels = ['AUG','SEP','OCT','NOV']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    axs2.plot(labels,b5,label=f'{listsartdate[4][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='8' and f'{enddate[5]}'=='1' and f'{enddate[6]}'=='2':
                    labels = ['AUG','SEP','OCT','NOV','DEC']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    axs2.plot(labels,b5,label=f'{listsartdate[4][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='9'  and f'{enddate[6]}'=='0':
                    labels = ['SEP','OCT']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    axs2.plot(labels,b5,label=f'{listsartdate[4][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='9' and f'{enddate[5]}'=='1' and f'{enddate[6]}'=='1':
                    labels = ['SEP','OCT','NOV']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    axs2.plot(labels,b5,label=f'{listsartdate[4][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='9' and f'{enddate[5]}'=='1' and f'{enddate[6]}'=='2':
                    labels = ['SEP','OCT','NOV','DEC']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    axs2.plot(labels,b5,label=f'{listsartdate[4][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if  f'{startdate[6]}'=='0' and f'{enddate[5]}'=='1' and f'{enddate[6]}'=='1':
                    labels = ['OCT','NOV']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    axs2.plot(labels,b5,label=f'{listsartdate[4][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[6]}'=='0' and f'{enddate[5]}'=='1' and f'{enddate[6]}'=='2':
                    labels = ['OCT','NOV','DEC']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    axs2.plot(labels,b5,label=f'{listsartdate[4][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
            if len(id)<=1:
                if f'{startdate[5]}'=='1' and f'{startdate[6]}'=='1' and f'{enddate[5]}'=='1' and f'{enddate[6]}'=='2':
                    labels = ['NOV','DEC']
                    axs2.plot(labels,b1,label=f'{listsartdate[0][:4]}')
                    axs2.plot(labels,b2,label=f'{listsartdate[1][:4]}')
                    axs2.plot(labels,b3,label=f'{listsartdate[2][:4]}')
                    axs2.plot(labels,b4,label=f'{listsartdate[3][:4]}')
                    axs2.plot(labels,b5,label=f'{listsartdate[4][:4]}')
                    fig.suptitle(f'{VAR}', fontweight='bold', fontsize=16)
            axs2.legend()
            axs2.grid()
            plt.setp(axs2.xaxis.get_majorticklabels(), rotation=50)
        return [x0, y0],SHOWPLT(fig=fig,conteneur=conteneur),
  
