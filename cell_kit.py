import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
import plotly.express as px
import plotly.graph_objects as go
import os
import glob
from re import search
from scipy import stats
import datetime
import math
pd.options.mode.chained_assignment = None  # default='warn'


color_palette=['tab:purple','palevioletred','thistle','tab:blue','lightsteelblue','skyblue','cornflowerblue','tab:cyan','tab:green','tab:olive','mediumspringgreen','tab:gray','silver','yellowgreen','tab:brown','tab:orange','goldenrod','tab:pink','lightcoral','tab:red','maroon','sienna','peachpuff','darksalmon']

plotly_color_palette=['darkkhaki','darkolivegreen','darkorchid', 'darkred', 'darksalmon', 'darkseagreen','darkslateblue', 'darkslategray', 'darkslategrey','aliceblue', 'antiquewhite', 'aqua', 'aquamarine', 'azure','beige', 'bisque', 'black', 'blanchedalmond','blue','blueviolet', 'brown', 'burlywood', 'cadetblue','chartreuse', 'chocolate', 'coral', 'cornflowerblue','cornsilk', 'crimson', 'cyan', 'darkblue', 'darkcyan','darkgoldenrod', 'darkgray', 'darkgrey', 'darkgreen','darkmagenta',  'darkorange']

line_style = ["solid","dashed","dotted","dashdot",(0, (1, 10)), (0, (3, 10, 1, 10))]
fig_title_size=20
title_fontsize=16#title_size
axis_fontsize=14.5#label_size
legend_fontsize=14#legend_size=15
cell_fontsize=14

def import_neware_data(file_name,sheet_name):
    data = pd.read_excel( file_name, sheet_name = sheet_name, index_col=0, 
                  converters={"Relative Time(h:min:s.ms)":pd.to_timedelta,"Real time(h:min:s.ms)":pd.to_datetime })
    data["Relative Time(h:min:s.ms)"] = data["Relative Time(h:min:s.ms)"] / np.timedelta64(1, 's')
    data.rename(columns={"Relative Time(h:min:s.ms)":"Relative Time(s)"}, inplace=True)
    data_with_cycle_time=add_cycle_time(data)
    
    return data_with_cycle_time

def import_formatted_data(file_name):
    data = pd.concat(pd.read_excel(file_name, sheet_name=None), ignore_index=True)
    data["Relative Time(h:min:s.ms)"]=pd.to_timedelta(data["Relative Time(h:min:s.ms)"])
    data["Real time(h:min:s.ms)"]=pd.to_datetime(data["Real time(h:min:s.ms)"])
    data["Relative Time(h:min:s.ms)"] = data["Relative Time(h:min:s.ms)"] / np.timedelta64(1, 's')
    data.rename(columns={"Relative Time(h:min:s.ms)":"Relative Time(s)"}, inplace=True)
    state={'CC_DChg':'CC DChg','CC_Chg':'CC Chg','CV_Chg':'CV Chg','CCCV_Chg':'CCCV Chg'}
    df.replace({'State':state},inplace=True)
    data_with_cycle_time=add_cycle_time(data)
    
    return data_with_cycle_time

def get_neware_data(path):
    path = os.getcwd()+path
    files = glob.glob(path + "/*.xlsx")
    df = pd.DataFrame()
    for file in files:
        xl = pd.ExcelFile(file)
        for idx, name in enumerate(xl.sheet_names):
            if search("Detail",name) or search("record",name):
                sheet = xl.parse(name)
                df = df.append(sheet)
    df["Relative Time(h:min:s.ms)"]=pd.to_timedelta(df["Relative Time(h:min:s.ms)"])
    df["Real time(h:min:s.ms)"]=pd.to_datetime(df["Real time(h:min:s.ms)"])
    df["Relative Time(h:min:s.ms)"] = df["Relative Time(h:min:s.ms)"] / np.timedelta64(1, 's')
    df.rename(columns={"Relative Time(h:min:s.ms)":"Relative Time(s)"}, inplace=True)
    state={'CC_DChg':'CC DChg','CC_Chg':'CC Chg','CV_Chg':'CV Chg','CCCV_Chg':'CCCV Chg'}
    df.replace({'State':state},inplace=True)
    data_with_cycle_time=add_cycle_time(df)
    return data_with_cycle_time

def get_neware530_data(path):
    path = os.getcwd()+path
    files = glob.glob(path + "/*.xlsx")
    df = pd.DataFrame()
    for file in files:
        xl = pd.ExcelFile(file)
        for idx, name in enumerate(xl.sheet_names):
            if search("record",name):
                sheet = xl.parse(name)
                df = df.append(sheet)
    df["Time"]=pd.to_timedelta(df["Time"])
    df["Time"] = df["Time"] / np.timedelta64(1, 's')
    df["Real time"]=pd.to_datetime(df["Real time"])
    df.rename(columns={"Step Type":"State",'Cycle ID':'Cycle','Step ID':'Steps','Time':'Relative Time(s)','Real time':'Real time(h:min:s.ms)'}, inplace=True)
    state={'CC_DChg':'CC DChg','CC_Chg':'CC Chg','CV_Chg':'CV Chg','CCCV_Chg':'CCCV Chg'}
    df.replace({'State':state},inplace=True)
    data_with_cycle_time=add_cycle_time(df)
    return data_with_cycle_time

def get_xwell_data(path):
    path = os.getcwd()+path
    files = glob.glob(path + "/*.xlsx")
    df = pd.DataFrame()
    for file in files:
        xl = pd.ExcelFile(file)
        for idx, name in enumerate(xl.sheet_names):
            if search("TestData",name):
                sheet = xl.parse(name)
                df = df.append(sheet)
    df["SampleTime"]=pd.to_timedelta(df["SampleTime"])
    df["SampleTime"] = df["SampleTime"] / np.timedelta64(1, 's')
    df["RealTime"]=pd.to_datetime(df["RealTime"])
    df.rename(columns={"StepType":"State",'CycleCount':'Cycle','StepNo.':'Steps','SampleTime':'Relative Time(s)','RealTime':'Real time(h:min:s.ms)','SampleVoltage(V)':'Voltage(V)','SampleCurrent(A)':'Current(A)',}, inplace=True)
    state={'ConstCurrentDischarge':'CC DChg','IDLE':'Rest','ConstCurrentCharge':'CCCV Chg','ConstVoltageCharge':'CCCV Chg'}
    df.replace({'State':state},inplace=True)
    data_with_cycle_time=add_cycle_time(df)
    return data_with_cycle_time

def add_cycle_time(data):
    #n_cycles = data["Cycle"].max()
    cycles=data["Cycle"].unique()
    data_with_cy_time=pd.DataFrame()
    for i in cycles:
        data_cy_i=data[data["Cycle"]==i]
        data_cy_i["dt"]=data_cy_i["Real time(h:min:s.ms)"].diff().fillna(pd.Timedelta(0))
        data_cy_i["cycle_time(s)"]=data_cy_i["dt"].cumsum()
        data_cy_i["cycle_time(s)"] = data_cy_i["cycle_time(s)"] / np.timedelta64(1, 's')
        data_with_cy_time=data_with_cy_time.append(data_cy_i)
    data_with_cy_time.drop(['dt'], inplace=True, axis = 1)
    return data_with_cy_time

def get_dcir(file, max_cap=0):
    details = pd.DataFrame()
    data = pd.DataFrame()
    xl = pd.ExcelFile(file)
    for idx, name in enumerate(xl.sheet_names):
        if search("Statis",name):
            sheet = xl.parse(name)
            data = data.append(sheet)
        if search("Detail",name):
            sheet = xl.parse(name)
            details = details.append(sheet)
    data["Relative Time(h:min:s.ms)"]=pd.to_timedelta(data["Relative Time(h:min:s.ms)"])
    data["Relative Time(h:min:s.ms)"] = data["Relative Time(h:min:s.ms)"] / np.timedelta64(1, 's')
    data.rename(columns={"Relative Time(h:min:s.ms)":"Relative Time(s)"}, inplace=True)
    
    if max_cap==0:
        max_cap=data["Capacity(Ah)"].max()
    data["Capacity(Ah)"]=np.where(data["State"]=="CC DChg",-data["Capacity(Ah)"],data["Capacity(Ah)"])
    data["charge"]=data["Capacity(Ah)"].cumsum()
    data["SoC"]=data["charge"]/max_cap
    n_cycles=data["Cycle"].max()
    
    details["Relative Time(h:min:s.ms)"]=pd.to_timedelta(details["Relative Time(h:min:s.ms)"])
    details["Relative Time(h:min:s.ms)"] = details["Relative Time(h:min:s.ms)"] / np.timedelta64(1, 's')
    details.rename(columns={"Relative Time(h:min:s.ms)":"Relative Time(s)"}, inplace=True)
    details["Capacity(Ah)"]=np.where(details["State"]=="CC DChg",-details["Capacity(Ah)"],details["Capacity(Ah)"])
    #details["charge"]=details["Capacity(Ah)"].cumsum()
    #details["SoC"]=details["charge"]/max_cap
    
    soc_dcir=pd.DataFrame()
    for c in range(1,n_cycles+1,1):
        
        cy_data=data[data["Cycle"]==c]
        if cy_data[(cy_data["State"]=="CC DChg")&(cy_data["Relative Time(s)"]==10.0)]["State"].unique() and cy_data[(cy_data["State"]=="CC DChg")&(cy_data["Relative Time(s)"]==1.0)]["State"].unique():
            prev_step = cy_data[(cy_data["State"]=="CC DChg")&(cy_data["Relative Time(s)"]==10.0)]["Steps"].item() - 2
            v_prev = data[(data["Steps"]==prev_step)]["End voltage(V)"].item()
            recovery_v = data[(data["Steps"]==(prev_step+1))]["End voltage(V)"].item()
            #vi1= data[(data["Cycle"]==c)&(data["State"]=="CC DChg")&(data["Relative Time(s)"]>11.0)]["Start Volt(V)"].item()
            #vi2= data[(data["Cycle"]==c)&(data["State"]=="CC DChg")&(data["Relative Time(s)"]>11.0)]["End voltage(V)"].item()
            #v0 = data[(data["Cycle"]==c)&(data["State"]=="CC DChg")&(data["Relative Time(s)"]==10.0)]["Start Volt(V)"].item()
            v1 = cy_data[(cy_data["State"]=="CC DChg")&(cy_data["Relative Time(s)"]==10.0)]["End voltage(V)"].item()
            v2 = cy_data[(cy_data["State"]=="CC DChg")&(cy_data["Relative Time(s)"]==1.0)]["End voltage(V)"].item()
            i1 = cy_data[(cy_data["State"]=="CC DChg")&(cy_data["Relative Time(s)"]==10.0)]["Starting current(A)"].item()
            i2 = cy_data[(cy_data["State"]=="CC DChg")&(cy_data["Relative Time(s)"]==1.0)]["Starting current(A)"].item()
            dc_ir=(v1-v2)/(i1-i2)*1000
            soc = (cy_data[(cy_data["State"]=="CC DChg")&(cy_data["Relative Time(s)"]==10.0)]["charge"].item() - 
                   cy_data[(cy_data["State"]=="CC DChg")&(cy_data["Relative Time(s)"]==10.0)]["Capacity(Ah)"].item())/max_cap
            df=pd.DataFrame({"SoC":[soc],"DC_IR":[dc_ir],"Load Volt":[v_prev],"Recovery Volt":[recovery_v]})
            soc_dcir=soc_dcir.append(df)
    
    soc_dcir["SoC"]=soc_dcir["SoC"]*100
    soc_dcir.reset_index(inplace=True)
    #print(soc_dcir.columns)
    soc_dcir.drop(["index"],axis=1, inplace=True)
    soc_dcir.index=soc_dcir.index+1
    soc_dcir.sort_values(by="SoC", inplace=True, ignore_index=True)
    #print(soc_dcir.iloc[:,1:])
    
    fig, ((plt1,plt2),(plt3,plt4))=plt.subplots(2,2,figsize=(24, 18))

    plt1.set_title("DC Internal Resistance vs State of Charge (Acc. to IEC 61960-2330)", fontsize=title_fontsize)
    plt1.set_xlim([0,100])
    plt1.set_xlabel("State of Charge(%)", fontsize=axis_fontsize)
    plt1.set_ylabel("DC Internal Resistance (mΩ)", fontsize=axis_fontsize)
    plt1.minorticks_on()
    plt1.plot(soc_dcir["SoC"],soc_dcir["DC_IR"])
    plt1.grid(visible=True, which='major', axis='both')
    
    """plt2.set_title("DC Internal Resistance vs Voltage")
    plt2.set_xlim([4.2,2.75])
    plt2.set_xlabel("Voltage(V)")
    plt2.set_ylabel("DC Internal Resistance (mΩ)")
    plt2.minorticks_on()
    plt2.plot(soc_dcir["Voltage"],soc_dcir["DC_IR"])
    plt2.grid(visible=True, which='major', axis='both')"""
    
    plt2.set_title("DC Internal Resistance vs Voltage", fontsize=title_fontsize)
    plt2.set_xlim(left=soc_dcir["Load Volt"].min(),right=soc_dcir["Load Volt"].max())
    plt2.set_xlabel("Voltage(V)", fontsize=axis_fontsize)
    plt2.set_ylabel("DC Internal Resistance (mΩ)", fontsize=axis_fontsize)
    plt2.minorticks_on()
    plt2.plot(soc_dcir["Load Volt"],soc_dcir["DC_IR"], label="vs Load Voltage")
    plt2.plot(soc_dcir["Recovery Volt"],soc_dcir["DC_IR"], label="vs Recovery Voltage")
    plt2.grid(visible=True, which='major', axis='both')
    plt2.legend(bbox_to_anchor=(0.5,-0.07),loc='upper center', ncol=4, fontsize=legend_fontsize)
    #figure(figsize=(10, 7), dpi=80)
    
    plt3.set_axis_off()
    plt3.set_title("SoC-DCIR-Load Volt-Recovery Volt", fontsize=title_fontsize)
    if not soc_dcir.empty:
        soc_dcir.columns = ["SoC(%)","DC IR (mΩ)","Load Voltage(V)","Recovery Voltage(V)"]
        soc_dcir=round(soc_dcir,2)
        #display(extract[["DoD","Voltage(V)","Capacity(Ah)","Relative Time(s)"]])
        tbl3=plt3.table(cellText=soc_dcir.values, colLabels =soc_dcir.columns, rowLabels=soc_dcir.index, rowLoc='left', colLoc='center', cellLoc ='right', loc ='upper left')
        tbl3.set_fontsize(cell_fontsize)
        tbl3.scale(1,2)
    
    
    plt4.set_title("Voltage vs State of Charge", fontsize=title_fontsize)
    plt4.set_xlim([0,100])
    plt4.set_xlabel("State of Charge(%)", fontsize=axis_fontsize)
    plt4.set_ylabel("Load Voltage(V)", fontsize=axis_fontsize)
    plt4.minorticks_on()
    
    n_steps=details["Steps"].max()
    max_current=details["Current(A)"].max()
    prev_cap=0
    for s in range(1,n_steps+1,1):
        step_data=details[details["Steps"]==s]
        step_data["charge"]=prev_cap+step_data["Capacity(Ah)"]
        step_data["SoC"] = step_data["charge"]/max_cap
        step_data["size"] = (abs(step_data["Current(A)"]*50/max_current)).clip(lower=0.5)
        #plt2.plot(data["SoC"]*100,data["End voltage(V)"])
        plt4.scatter(step_data["SoC"]*100,step_data["Voltage(V)"],s=step_data["size"])
        prev_cap = step_data["charge"].iat[-1]
        
    plt4.grid(visible=True, which='major', axis='both')
    

def extract_cycle_state(data,cycle,state="All"):
    if state=="All":
        return data[data["Cycle"]==cycle]
    else:
        return data[(data["Cycle"]==cycle) & (data["State"]==state)]

def cycle_summary(data,save_to_file=True,file_name="Cell Summaries/summary.xlsx"):
    n_cycles = data["Cycle"].max()
    cy_summ=pd.DataFrame()
    for i in range(1,n_cycles+1):
        
        cy_data=data[data["Cycle"]==i]
        
        data_cy_i_dchg = cy_data[(cy_data["State"]=="CC DChg")]
        data_cy_i_dchg_grouped = data_cy_i_dchg.groupby(["Cycle"]).agg({"Current(A)":["min"],"Voltage(V)":["min"],
                                                         "Capacity(Ah)":["max"],"Energy(Wh)":["max"],
                                                         "Relative Time(s)":"max"})
        data_cy_i_dchg_grouped.columns=["discharge_current(A)","lower_cutoff_voltage(V)",
                              "discharge_capacity(Ah)","discharge_energy(Wh)","discharge_time(s)"]
        
        data_cy_i_chg_cc=cy_data[(cy_data["State"]=="CC Chg")]
        data_cy_i_chg_cc_grouped=data_cy_i_chg_cc.groupby(["Cycle"]).agg({"Current(A)":["max"],"Voltage(V)":["max"],
                                                         "Capacity(Ah)":["max"],"Energy(Wh)":["max"],
                                                         "Relative Time(s)":"max"})
        data_cy_i_chg_cc_grouped.columns=["cc_charge_current(A)","cc_cutoff_voltage(V)","cc_charge_capacity(Ah)",
                       "cc_charge_energy(Wh)","cc_charge_time(s)"]
        
        data_cy_i_chg_cv=cy_data[(cy_data["State"]=="CV Chg")]
        data_cy_i_chg_cv_grouped=data_cy_i_chg_cv.groupby(["Cycle"]).agg({"Current(A)":["min"],
                                                         "Capacity(Ah)":["max"],"Energy(Wh)":["max"],
                                                         "Relative Time(s)":"max"})
        data_cy_i_chg_cv_grouped.columns=["cv_cutoff_current(A)","cv_charge_capacity(Ah)",
                       "cv_charge_energy(Wh)","cv_charge_time(s)"]
        
        data_cy_i_chg=cy_data[((cy_data["State"]=="CCCV Chg"))]
        data_cy_i_chg_grouped=data_cy_i_chg.groupby(["Cycle"]).agg({"Current(A)":["max"],"Voltage(V)":["max"],
                                                         "Capacity(Ah)":["max"],"Energy(Wh)":["max"],
                                                         "Relative Time(s)":"max"})
        data_cy_i_chg_grouped.columns=["charge_current(A)","upper_cutoff_voltage(V)","charge_capacity(Ah)",
                       "charge_energy(Wh)","charge_time(s)"]
        
        if (not data_cy_i_chg.empty) and (data_cy_i_chg_cc.empty) and (data_cy_i_chg_cv.empty):
            prds=max(int(len(data_cy_i_chg)/250),1)
            data_cy_i_chg["dV"]=data_cy_i_chg["Voltage(V)"].diff(periods=prds)
            data_cy_i_chg["dt"]=data_cy_i_chg["Relative Time(s)"].diff(periods=prds)
            data_cy_i_chg["dI"]=data_cy_i_chg["Current(A)"].diff(periods=prds)
            
            data_cy_i_chg_cv=data_cy_i_chg[(abs(data_cy_i_chg["dV"]/data_cy_i_chg["dt"])<=0.00001)&(abs(data_cy_i_chg["dI"]/data_cy_i_chg["dt"])>=0.0001)]
            if not data_cy_i_chg_cv.empty:
                cv_start=data_cy_i_chg_cv.index[0] - prds+1
                data_cy_i_chg_cv=data_cy_i_chg[data_cy_i_chg.index>=cv_start]
                data_cy_i_chg_cv_grouped=data_cy_i_chg_cv.groupby(["Cycle"]).agg({"Current(A)":["min"],
                                                         "Capacity(Ah)":["max"],"Energy(Wh)":["max"],
                                                         "Relative Time(s)":"max"})
                data_cy_i_chg_cv_grouped.columns=["cv_cutoff_current(A)","cv_charge_capacity(Ah)",
                       "cv_charge_energy(Wh)","cv_charge_time(s)"]
            
                data_cy_i_chg_cc=data_cy_i_chg[data_cy_i_chg.index<cv_start]
                data_cy_i_chg_cc_grouped=data_cy_i_chg_cc.groupby(["Cycle"]).agg({"Current(A)":["max"],"Voltage(V)":["max"],
                                                         "Capacity(Ah)":["max"],"Energy(Wh)":["max"],
                                                         "Relative Time(s)":"max"})
                data_cy_i_chg_cc_grouped.columns=["cc_charge_current(A)","cc_cutoff_voltage(V)","cc_charge_capacity(Ah)",
                       "cc_charge_energy(Wh)","cc_charge_time(s)"]
                
                data_cy_i_chg_cv_grouped["cv_charge_capacity(Ah)"]=data_cy_i_chg_cv_grouped["cv_charge_capacity(Ah)"]-data_cy_i_chg_cc_grouped["cc_charge_capacity(Ah)"]
                data_cy_i_chg_cv_grouped["cv_charge_energy(Wh)"]=data_cy_i_chg_cv_grouped["cv_charge_energy(Wh)"]-data_cy_i_chg_cc_grouped["cc_charge_energy(Wh)"]
                data_cy_i_chg_cv_grouped["cv_charge_time(s)"]=data_cy_i_chg_cv_grouped["cv_charge_time(s)"]-data_cy_i_chg_cc_grouped["cc_charge_time(s)"]
                
        data_cy_i_grouped=cy_data.groupby(["Cycle"]).agg({"cycle_time(s)":["max"],"Real time(h:min:s.ms)":["min","max"]})
        data_cy_i_grouped.columns=["cycle_time(s)","start_time","end_time"]
         
        temp=pd.concat([data_cy_i_chg_grouped,data_cy_i_chg_cc_grouped,data_cy_i_chg_cv_grouped,data_cy_i_dchg_grouped,data_cy_i_grouped],axis=1)
        
        temp["charge_current(A)"]=np.where(temp["charge_current(A)"].isna(),temp["cc_charge_current(A)"],temp["charge_current(A)"])
        temp["upper_cutoff_voltage(V)"]=np.where(temp["upper_cutoff_voltage(V)"].isna(),temp["cc_cutoff_voltage(V)"],temp["upper_cutoff_voltage(V)"])
        temp["charge_capacity(Ah)"]=np.where(temp["charge_capacity(Ah)"].isna(),temp["cc_charge_capacity(Ah)"]+temp["cv_charge_capacity(Ah)"],temp["charge_capacity(Ah)"])
        temp["charge_energy(Wh)"]=np.where(temp["charge_energy(Wh)"].isna(),temp["cc_charge_energy(Wh)"]+temp["cv_charge_energy(Wh)"],temp["charge_energy(Wh)"])
        temp["charge_time(s)"]=np.where(temp["charge_time(s)"].isna(),temp["cc_charge_time(s)"]+temp["cv_charge_time(s)"],temp["charge_time(s)"])
        
        #For Voltage Recovery after Discharging
        
        if cy_data[cy_data["State"].str.contains("DChg")]["Steps"].max():
            Recovery_Step=cy_data[cy_data["State"].str.contains("DChg")]["Steps"].max()+1
            temp["recovery_voltage(V)"]=cy_data[cy_data["Steps"]==Recovery_Step]["Voltage(V)"].max()
        
        cy_summ=cy_summ.append(temp)
        
        #cy_summ = cy_summ.replace(r'^\s*$', np.nan, regex=True)
        cy_summ.fillna(0, inplace=True)
    cy_summ["charge_throughput(Ah)"]=cy_summ["charge_capacity(Ah)"].cumsum()
    cy_summ["charge_output(Ah)"]=cy_summ["discharge_capacity(Ah)"].cumsum()
    cy_summ["energy_throughput(Wh)"]=cy_summ["charge_energy(Wh)"].cumsum()
    cy_summ["energy_output(Wh)"]=cy_summ["discharge_energy(Wh)"].cumsum()
    cy_summ["energy_efficiency"]=cy_summ["discharge_energy(Wh)"]/(cy_summ["charge_energy(Wh)"])
    cy_summ["charge_efficiency"]=cy_summ["discharge_capacity(Ah)"]/(cy_summ["charge_capacity(Ah)"])
    if save_to_file:
        cy_summ.to_excel(file_name,sheet_name = "summary")
    return cy_summ    

    
def plot_voltage(data,cycle=None,label="",save_image=1):
    if (cycle==None):
        if (len(data['Cycle'].unique())>=3):
            cycle = [3,int(data["Cycle"].max()/2),data["Cycle"].max()-1] #range(3,data["Cycle"].max(),int((data["Cycle"].max()-3)/3))
        else:
            cycle = data['Cycle'].unique()
    
    fig, ((plt1,plt2,plt3),(plt4,plt5,plt6))=plt.subplots(2,3,figsize=(24, 21))
    
    #fig.suptitle("Voltage")
    #fig.tight_layout(pad=3)
    
    plt1.set_xlabel("Depth of Discharge(%)", fontsize=axis_fontsize)
    plt1.set_ylabel("Discharge Voltage(V)", fontsize=axis_fontsize)
    plt1.set_title("Discharge Voltage vs Depth of Discharge", fontsize=title_fontsize)
    #plt1.set_xlim([0,100])
    plt1.minorticks_on()
    for i in cycle:
        cycle_data=data[(data["Cycle"]==i) & ((data["State"]=="CC DChg"))]
        max_capacity=cycle_data["Capacity(Ah)"].max()
        cycle_data.loc[:,"DoD"]=100*cycle_data.loc[:,"Capacity(Ah)"]/max_capacity
        if not cycle_data.empty:
            plt1.plot(cycle_data["DoD"],cycle_data["Voltage(V)"], label="Cycle "+str(i) )
    plt1.legend(bbox_to_anchor=(0.5,-0.07),loc='upper center', ncol=4, fontsize=legend_fontsize)
    plt1.grid(visible=True, which='major', axis='both')
    
    plt2.set_xlabel("Discharge Capacity(Ah)", fontsize=axis_fontsize)
    plt2.set_ylabel("Discharge Voltage(V)", fontsize=axis_fontsize)
    plt2.set_title("Discharge Voltage vs Discharge Capacity", fontsize=title_fontsize)
    #plt2.set_xlim([0,1.2*capacity])
    plt2.minorticks_on()
    for i in cycle:
        cycle_data=data[(data["Cycle"]==i) & ((data["State"]=="CC DChg"))]
        if not cycle_data.empty:
            plt2.plot(cycle_data["Capacity(Ah)"],cycle_data["Voltage(V)"], label="Cycle "+str(i))
    plt2.legend(bbox_to_anchor=(0.5,-0.07),loc='upper center', ncol=4, fontsize=legend_fontsize)
    plt2.grid(visible=True, which='major', axis='both')
    
    plt3.set_xlabel("Discharge Time(s)", fontsize=axis_fontsize)
    plt3.set_ylabel("Discharge Voltage(V)", fontsize=axis_fontsize)
    plt3.set_title("Discharge Voltage vs Discharge Time", fontsize=title_fontsize)
    plt3.minorticks_on()
    #plt3.set_xlim(left=0)
    for i in cycle:
        cycle_data=data[(data["Cycle"]==i) & ((data["State"]=="CC DChg"))]
        if not cycle_data.empty:
            plt3.plot(cycle_data["Relative Time(s)"],cycle_data["Voltage(V)"], label="Cycle "+str(i))
    plt3.legend(bbox_to_anchor=(0.5,-0.07),loc='upper center', ncol=4, fontsize=legend_fontsize)
    plt3.grid(visible=True, which='major', axis='both')
    
    plt4.set_xlabel("State of Charge(%)", fontsize=axis_fontsize)
    plt4.set_ylabel("Charge Voltage(V)", fontsize=axis_fontsize)
    plt4.set_title("Charge Voltage vs State of Charge", fontsize=title_fontsize)
    plt4.minorticks_on()
    #plt4.set_xlim([0,100])
    for i in cycle:
        cycle_data=data[(data["Cycle"]==i) & ((data["State"]=="CCCV Chg"))]
        if not cycle_data.empty:
            max_capacity=cycle_data["Capacity(Ah)"].max()
            cycle_data["SoC"]=100*cycle_data["Capacity(Ah)"]/max_capacity
            plt4.plot(cycle_data["SoC"],cycle_data["Voltage(V)"], label="Cycle "+str(i))
        #For separated CC CV
        cycle_data=data[(data["Cycle"]==i) & ((data["State"]=="CC Chg")|(data["State"]=="CV Chg"))]
        if not cycle_data.empty:
            cc_max = cycle_data[cycle_data["State"]=="CC Chg"]["Capacity(Ah)"].max()
            cv_max = cycle_data[cycle_data["State"]=="CV Chg"]["Capacity(Ah)"].max()
            max_capacity = cc_max + cv_max
            cycle_data["SoC"]=np.where(cycle_data["State"]=="CC Chg",100*cycle_data["Capacity(Ah)"]/max_capacity,100*(cc_max+cycle_data["Capacity(Ah)"])/max_capacity)
            plt4.plot(cycle_data["SoC"],cycle_data["Voltage(V)"], label="Cycle "+str(i))
    plt4.legend(bbox_to_anchor=(0.5,-0.07),loc='upper center', ncol=4, fontsize=legend_fontsize)
    plt4.grid(visible=True, which='major', axis='both')
    
    plt5.set_xlabel("Charge Capacity(Ah)", fontsize=axis_fontsize)
    plt5.set_ylabel("Charge Voltage(V)", fontsize=axis_fontsize)
    plt5.set_title("Charge Voltage vs Charge Capacity", fontsize=title_fontsize)
    plt5.minorticks_on()
    #plt5.set_xlim([0,1.2*capacity])
    for i in cycle:
        cycle_data=data[(data["Cycle"]==i) & ((data["State"]=="CCCV Chg"))]
        if not cycle_data.empty:
            plt5.plot(cycle_data["Capacity(Ah)"],cycle_data["Voltage(V)"], label="Cycle "+str(i))
        #For separated CC CV
        cycle_data=data[(data["Cycle"]==i) & ((data["State"]=="CC Chg")|(data["State"]=="CV Chg"))]
        if not cycle_data.empty:
            cc_max = cycle_data[cycle_data["State"]=="CC Chg"]["Capacity(Ah)"].max()
            cycle_data["CCCV_Capacity"]=np.where(cycle_data["State"]=="CC Chg",cycle_data["Capacity(Ah)"],cc_max+cycle_data["Capacity(Ah)"])
            plt5.plot(cycle_data["CCCV_Capacity"],cycle_data["Voltage(V)"], label="Cycle "+str(i))
    plt5.legend(bbox_to_anchor=(0.5,-0.07),loc='upper center', ncol=4, fontsize=legend_fontsize)
    plt5.grid(visible=True, which='major', axis='both')
    
    plt6.set_xlabel("Charge Time(s)", fontsize=axis_fontsize)
    plt6.set_ylabel("Charge Voltage(V)", fontsize=axis_fontsize)
    plt6.set_title("Charge Voltage vs Time", fontsize=title_fontsize)
    plt6.minorticks_on()
    #plt6.set_xlim([0,])
    for i in cycle:
        cycle_data=data[(data["Cycle"]==i) & ((data["State"]=="CCCV Chg"))]
        if not cycle_data.empty:
            plt6.plot(cycle_data["Relative Time(s)"],cycle_data["Voltage(V)"], label="Cycle "+str(i))
        #For separated CC CV
        cycle_data=data[(data["Cycle"]==i) & ((data["State"]=="CC Chg")|(data["State"]=="CV Chg"))]
        if not cycle_data.empty:
            cc_time = cycle_data[cycle_data["State"]=="CC Chg"]["Relative Time(s)"].max()
            cycle_data["CCCV_Time"]=np.where(cycle_data["State"]=="CC Chg",cycle_data["Relative Time(s)"],cc_time+cycle_data["Relative Time(s)"])
            plt6.plot(cycle_data["CCCV_Time"],cycle_data["Voltage(V)"], label="Cycle "+str(i))
    plt6.legend(bbox_to_anchor=(0.5,-0.07),loc='upper center', ncol=4, fontsize=legend_fontsize)
    plt6.grid(visible=True, which='major', axis='both')
    
    if save_image==1:
        fig.savefig('Output/'+str(label)+'Voltage.png')
    
def soc_dod_data(data,cycle=[1],label=""):
    
    cycle.sort()
    if cycle==[1]:
        cycle = [3,data["Cycle"].max()-1]
    
    DoD=pd.Series([0.0,10.0,20.0,30.0,40.0,50.0,60.0,70.0,80.0,90.0,100.0], name="DoD")
    extract_volt=DoD
    
    fig, ((plt1,plt2),(plt3,plt4))=plt.subplots(2,2,figsize=(24, 12))
    
    plt1.set_axis_off()
    plt1.set_title("Discharge Voltage(V)", fontsize=title_fontsize)
    for i in cycle:
        cycle_data=data[(data["Cycle"]==i) & (data["State"]=="CC DChg")]
        max_capacity=cycle_data["Capacity(Ah)"].max()
        cycle_data.loc[:,"DoD"]=100*cycle_data.loc[:,"Capacity(Ah)"]/max_capacity
        extract = pd.merge_asof(left=DoD,right=cycle_data, direction="nearest", on="DoD", allow_exact_matches=True)
        #extract.style.set_table_attributes("style='display:inline'")
        extract_volt=pd.merge(left=extract_volt,right=extract[["DoD","Voltage(V)"]],on="DoD")
        extract_volt["Voltage(V)"]=round(extract_volt["Voltage(V)"],2)
        extract_volt.columns = [*extract_volt.columns[:-1], "Cycle "+str(i)]
    if not extract_volt.empty:
        extract_volt.columns = ["DoD(%)",*extract_volt.columns[1:]]
        extract_volt["Change(%)"]=round((extract_volt.iloc[:,-1]-extract_volt.iloc[:,1])*100/extract_volt.iloc[:,1],2)
        #display(extract[["DoD","Voltage(V)","Capacity(Ah)","Relative Time(s)"]])
        tbl1=plt1.table(cellText=extract_volt.values, colLabels =extract_volt.columns, rowLoc='left', colLoc='center', cellLoc ='right', loc ='upper left')
        tbl1.set_fontsize(cell_fontsize)
        tbl1.scale(1,2)
    
    extract_cap=DoD
        
    plt2.set_axis_off()
    plt2.set_title("Discharge Capacity(Ah)", fontsize=title_fontsize)
    for i in cycle:
        cycle_data=data[(data["Cycle"]==i) & (data["State"]=="CC DChg")]
        max_capacity=cycle_data["Capacity(Ah)"].max()
        cycle_data.loc[:,"DoD"]=100*cycle_data.loc[:,"Capacity(Ah)"]/max_capacity
        extract = pd.merge_asof(left=DoD,right=cycle_data, direction="nearest", on="DoD", allow_exact_matches=True)
        extract_cap=pd.merge(left=extract_cap,right=extract[["DoD","Capacity(Ah)"]],on="DoD")
        extract_cap["Capacity(Ah)"]=round(extract_cap["Capacity(Ah)"],2)
        extract_cap.columns = [*extract_cap.columns[:-1], "Cycle "+str(i)]
    if not extract_cap.empty:
        extract_cap.columns = ["DoD(%)",*extract_cap.columns[1:]]
        extract_cap["Change(%)"]=round((extract_cap.iloc[:,-1]-extract_cap.iloc[:,1])*100/extract_cap.iloc[:,1],2)
        #display(extract[["DoD","Voltage(V)","Capacity(Ah)","Relative Time(s)"]])
        tbl2=plt2.table(cellText=extract_cap.values, colLabels =extract_cap.columns, rowLoc='left', colLoc='center', cellLoc ='right', loc ='upper left')
        tbl2.set_fontsize(cell_fontsize)
        tbl2.scale(1,2)
    
    
    SoC=pd.Series([0.0,10.0,20.0,30.0,40.0,50.0,60.0,70.0,80.0,90.0,100.0], name="SoC")
    extract_volt=SoC
    
    plt3.set_axis_off()
    plt3.set_title("Charge Voltage(V)", fontsize=title_fontsize)
    for i in cycle:
        cycle_data=data[(data["Cycle"]==i) & ((data["State"]=="CCCV Chg"))]
        if not cycle_data.empty:
            max_capacity=cycle_data["Capacity(Ah)"].max()
            cycle_data["SoC"]=100*cycle_data["Capacity(Ah)"]/max_capacity
            extract = pd.merge_asof(left=SoC,right=cycle_data, direction="nearest", on="SoC", allow_exact_matches=True)
            extract_volt=pd.merge(left=extract_volt,right=extract[["SoC","Voltage(V)"]],on="SoC")
            extract_volt["Voltage(V)"]=round(extract_volt["Voltage(V)"],2)
            extract_volt.columns = [*extract_volt.columns[:-1], "Cycle "+str(i)]
        #For separated CC CV
        cycle_data=data[(data["Cycle"]==i) & ((data["State"]=="CC Chg")|(data["State"]=="CV Chg"))]
        if not cycle_data.empty:
            cc_max = cycle_data[cycle_data["State"]=="CC Chg"]["Capacity(Ah)"].max()
            cv_max = cycle_data[cycle_data["State"]=="CV Chg"]["Capacity(Ah)"].max()
            max_capacity = cc_max + cv_max
            cycle_data["SoC"]=np.where(cycle_data["State"]=="CC Chg",100*cycle_data["Capacity(Ah)"]/max_capacity,100*(cc_max+cycle_data["Capacity(Ah)"])/max_capacity)
            extract = pd.merge_asof(left=SoC,right=cycle_data, direction="nearest", on="SoC", allow_exact_matches=True)
            extract_volt=pd.merge(left=extract_volt,right=extract[["SoC","Voltage(V)"]],on="SoC")
            extract_volt["Voltage(V)"]=round(extract_volt["Voltage(V)"],2)
            extract_volt.columns = [*extract_volt.columns[:-1], "Cycle "+str(i)]
    if not extract_volt.empty:
        extract_volt.columns = ["SoC(%)",*extract_volt.columns[1:]]
        extract_volt["Change(%)"]=round((extract_volt.iloc[:,-1]-extract_volt.iloc[:,1])*100/extract_volt.iloc[:,1],2)
        tbl3=plt3.table(cellText=extract_volt.values, colLabels =extract_volt.columns, rowLoc='left', colLoc='center', cellLoc ='right', loc ='upper left')
        tbl3.set_fontsize(cell_fontsize)
        tbl3.scale(1,2)
   
    extract_cap=SoC
    
    plt4.set_axis_off()
    plt4.set_title("Charge Capacity(Ah)", fontsize=title_fontsize)
    for i in cycle:
        cycle_data=data[(data["Cycle"]==i) & ((data["State"]=="CCCV Chg"))]
        if not cycle_data.empty:
            max_capacity=cycle_data["Capacity(Ah)"].max()
            cycle_data["SoC"]=100*cycle_data["Capacity(Ah)"]/max_capacity
            extract = pd.merge_asof(left=SoC,right=cycle_data, direction="nearest", on="SoC", allow_exact_matches=True)
            extract_cap=pd.merge(left=extract_cap,right=extract[["SoC","Capacity(Ah)"]],on="SoC")
            extract_cap["Capacity(Ah)"]=round(extract_cap["Capacity(Ah)"],2)
            extract_cap.columns = [*extract_cap.columns[:-1], "Cycle "+str(i)]
        #For separated CC CV
        cycle_data=data[(data["Cycle"]==i) & ((data["State"]=="CC Chg")|(data["State"]=="CV Chg"))]
        if not cycle_data.empty:
            cc_max = cycle_data[cycle_data["State"]=="CC Chg"]["Capacity(Ah)"].max()
            cv_max = cycle_data[cycle_data["State"]=="CV Chg"]["Capacity(Ah)"].max()
            max_capacity = cc_max + cv_max
            cycle_data["SoC"]=np.where(cycle_data["State"]=="CC Chg",100*cycle_data["Capacity(Ah)"]/max_capacity,100*(cc_max+cycle_data["Capacity(Ah)"])/max_capacity)
            extract = pd.merge_asof(left=SoC,right=cycle_data, direction="nearest", on="SoC", allow_exact_matches=True)
            extract_cap=pd.merge(left=extract_cap,right=extract[["SoC","Capacity(Ah)"]],on="SoC")
            extract_cap["Capacity(Ah)"]=round(extract_cap["Capacity(Ah)"],2)
            extract_cap.columns = [*extract_cap.columns[:-1], "Cycle "+str(i)]
    if not extract_cap.empty:
        extract_cap.columns = ["SoC(%)",*extract_cap.columns[1:]]
        extract_cap["Change(%)"]=round((extract_cap.iloc[:,-1]-extract_cap.iloc[:,1])*100/extract_cap.iloc[:,1],2)
        tbl4=plt4.table(cellText=extract_cap.values, colLabels =extract_cap.columns, rowLoc='left', colLoc='center', cellLoc ='right', loc ='upper left')
        tbl4.set_fontsize(cell_fontsize)
        tbl4.scale(1,2)
    
    fig.savefig('Output/'+str(label)+'_soc_dod.png')
   
    
def plot_current(data,cycle=[1],label=""):
    
    fig, ((plt1,plt2,plt3),(plt4,plt5,plt6))=plt.subplots(2,3,figsize=(24, 21))
    
    #fig.suptitle("Voltage")
    #fig.tight_layout(pad=3)
    
    plt1.set_xlabel("Depth of Discharge(%)", fontsize=axis_fontsize)
    plt1.set_ylabel("Discharge Current(A)", fontsize=axis_fontsize)
    plt1.set_title("Discharge Current vs Depth of Discharge", fontsize=title_fontsize)
    #plt1.set_xlim([0,100])
    plt1.minorticks_on()
    for i in cycle:
        cycle_data=data[(data["Cycle"]==i) & (data["State"]=="CC DChg")]
        max_capacity=cycle_data["Capacity(Ah)"].max()
        cycle_data.loc[:,"DoD"]=100*cycle_data.loc[:,"Capacity(Ah)"]/max_capacity
        if not cycle_data.empty:
            plt1.scatter(cycle_data["DoD"],cycle_data["Current(A)"], label="Cycle "+str(i))
    plt1.legend(bbox_to_anchor=(0.5,-0.07),loc='upper center', ncol=3, fontsize=legend_fontsize)
    
    plt2.set_xlabel("Discharge Capacity(Ah)", fontsize=axis_fontsize)
    plt2.set_ylabel("Discharge Current(A)", fontsize=axis_fontsize)
    plt2.set_title("Discharge Current vs Discharge Capacity", fontsize=title_fontsize)
    #plt2.set_xlim([0,1.2*capacity])
    plt2.minorticks_on()
    for i in cycle:
        cycle_data=data[(data["Cycle"]==i) & (data["State"]=="CC DChg")]
        if not cycle_data.empty:
            plt2.scatter(cycle_data["Capacity(Ah)"],cycle_data["Current(A)"], label="Cycle "+str(i))
    plt2.legend(bbox_to_anchor=(0.5,-0.07),loc='upper center', ncol=3, fontsize=legend_fontsize)
    
    plt3.set_xlabel("Discharge Time(s)", fontsize=axis_fontsize)
    plt3.set_ylabel("Discharge Current(A)", fontsize=axis_fontsize)
    plt3.set_title("Discharge Current vs Discharge Time", fontsize=title_fontsize)
    plt3.minorticks_on()
    #plt3.set_xlim(left=0)
    for i in cycle:
        cycle_data=data[(data["Cycle"]==i) & (data["State"]=="CC DChg")]
        if not cycle_data.empty:
            plt3.scatter(cycle_data["Relative Time(s)"],cycle_data["Current(A)"], label="Cycle "+str(i))
    plt3.legend(bbox_to_anchor=(0.5,-0.07),loc='upper center', ncol=3, fontsize=legend_fontsize)

    plt4.set_xlabel("State of Charge(%)", fontsize=axis_fontsize)
    plt4.set_ylabel("Charge Current(A)", fontsize=axis_fontsize)
    plt4.set_title("Charge Current vs State of Charge", fontsize=title_fontsize)
    plt4.minorticks_on()
    #plt4.set_xlim([0,100])
    for i in cycle:
        cycle_data=data[(data["Cycle"]==i) & (data["State"]=="CCCV Chg")]
        max_capacity=cycle_data["Capacity(Ah)"].max()
        cycle_data["SoC"]=100*cycle_data["Capacity(Ah)"]/max_capacity
        if not cycle_data.empty:
            plt4.scatter(cycle_data["SoC"],cycle_data["Current(A)"], label="Cycle "+str(i))
    plt4.legend(bbox_to_anchor=(0.5,-0.07),loc='upper center', ncol=3, fontsize=legend_fontsize)
    
    plt5.set_xlabel("Charge Capacity(Ah)", fontsize=axis_fontsize)
    plt5.set_ylabel("Charge Current(A)", fontsize=axis_fontsize)
    plt5.set_title("Charge Current vs Charge Capacity", fontsize=title_fontsize)
    plt5.minorticks_on()
    #plt5.set_xlim([0,1.2*capacity])
    for i in cycle:
        cycle_data=data[(data["Cycle"]==i) & (data["State"]=="CCCV Chg")]
        if not cycle_data.empty:
            plt5.scatter(cycle_data["Capacity(Ah)"],cycle_data["Current(A)"], label="Cycle "+str(i))
    plt5.legend(bbox_to_anchor=(0.5,-0.07),loc='upper center', ncol=3, fontsize=legend_fontsize)
    
    plt6.set_xlabel("Charge Time(s)", fontsize=axis_fontsize)
    plt6.set_ylabel("Charge Current(A)", fontsize=axis_fontsize)
    plt6.set_title("Charge Current vs Time", fontsize=title_fontsize)
    plt6.minorticks_on()
    #plt6.set_xlim([0,])
    for i in cycle:
        cycle_data=data[(data["Cycle"]==i) & (data["State"]=="CCCV Chg")]
        if not cycle_data.empty:
            plt6.scatter(cycle_data["Relative Time(s)"],cycle_data["Current(A)"], label="Cycle "+str(i))
    plt6.legend(bbox_to_anchor=(0.5,-0.07),loc='upper center', ncol=3, fontsize=legend_fontsize)
    
    fig.savefig('Output/'+str(label)+'Current.png')
    
    
def plot_dQ_dV_Chg(data,cycle=[1],label=""):
    
    if cycle==[1]:
        cycle = [3,int(data["Cycle"].max()/2),data["Cycle"].max()-1]
    
    fig, ((plt1,plt2),(plt3,plt4),(plt5,plt6))=plt.subplots(3,2,figsize=(24,27))
    
    figure(figsize=(24, 18), dpi=80)
    
    plt1.set_xlabel("Voltage(V)", fontsize=axis_fontsize)
    plt1.set_ylabel("Differential Capacity(dQ/dV)(Ah/V)", fontsize=axis_fontsize)
    plt1.set_title("Differential Capacity versus Voltage", fontsize=title_fontsize)
    plt1.set_xlim(left=data["Voltage(V)"].min(), right=data["Voltage(V)"].max())
    plt1.set_ylim([-1,12])
    plt1.minorticks_on()
    
    plt2.set_xlabel("State of Charge(%)", fontsize=axis_fontsize)
    plt2.set_ylabel("Differential Capacity(dQ/dV)(Ah/V)", fontsize=axis_fontsize)
    plt2.set_title("Differential Capacity vs SoC", fontsize=title_fontsize)
    plt2.set_xlim(left=0, right=100)
    plt2.set_ylim([-1,12])
    plt2.minorticks_on()

    plt3.set_xlabel("Capacity(Ah)", fontsize=axis_fontsize)
    plt3.set_ylabel("Differential Capacity(dQ/dV)(Ah/V)", fontsize=axis_fontsize)
    plt3.set_title("Differential Capacity vs Charge Capacity", fontsize=title_fontsize)
    plt3.set_xlim(left=data["Capacity(Ah)"].min(), right=data["Capacity(Ah)"].max())
    plt3.set_ylim([-1,12])
    plt3.minorticks_on()
    
    plt4.set_xlabel("Voltage(V)", fontsize=axis_fontsize)
    plt4.set_ylabel("Differential Voltage(dV/dQ)(V/Ah)", fontsize=axis_fontsize)
    plt4.set_title("Differential Voltage versus Voltage", fontsize=title_fontsize)
    plt4.set_xlim(left=data[data["State"]=="CCCV Chg"]["Voltage(V)"].min(), right=data[data["State"]=="CCCV Chg"]["Voltage(V)"].max())
    plt4.set_ylim([-1,15])
    plt4.minorticks_on()
    
    plt5.set_xlabel("State of Charge(%)", fontsize=axis_fontsize)
    plt5.set_ylabel("Differential Voltage(dV/dQ)(V/Ah)", fontsize=axis_fontsize)
    plt5.set_title("Differential Voltage vs SoC", fontsize=title_fontsize)
    #plt5.set_ylim([-1,12])
    plt5.minorticks_on()
    plt5.set_xlim(left=0, right=100)
    plt5.set_ylim([-0.25,1])
    
    plt6.set_xlabel("Capacity(Ah)", fontsize=axis_fontsize)
    plt6.set_ylabel("Differential Voltage(dV/dQ)(V/Ah)", fontsize=axis_fontsize)
    plt6.set_title("Differential Voltage vs Charge Capacity", fontsize=title_fontsize)
    plt6.set_xlim(left=data["Capacity(Ah)"].min(), right=data["Capacity(Ah)"].max())
    plt6.set_ylim([-0.25,1])
    plt6.minorticks_on()
    
    for i in cycle:
        cycle_data=data[(data["Cycle"]==i) & (data["State"]=="CCCV Chg")]
        if not cycle_data.empty:
            #periods=int(len(cycle_data)/300)
            periods=5
            cycle_data["dQ"]=cycle_data["Capacity(Ah)"].rolling(50,min_periods=1).mean().diff(periods)
            cycle_data["dV"]=cycle_data["Voltage(V)"].rolling(50,min_periods=1).mean().diff(periods)
            cycle_data["dQ/dV"]=cycle_data["dQ"]/cycle_data["dV"]
            cycle_data["dV/dQ"]=cycle_data["dV"]/cycle_data["dQ"]
            max_capacity=cycle_data["Capacity(Ah)"].max()
            cycle_data["SoC"]=100*cycle_data["Capacity(Ah)"]/max_capacity
            
            plt1.scatter(cycle_data["Voltage(V)"],cycle_data["dQ/dV"], label="Cycle "+str(i))
            plt2.scatter(cycle_data["SoC"],cycle_data["dQ/dV"], label="Cycle "+str(i))
            plt3.scatter(cycle_data["Capacity(Ah)"],cycle_data["dQ/dV"], label="Cycle "+str(i))
            plt4.scatter(cycle_data["Voltage(V)"],cycle_data["dV/dQ"], label="Cycle "+str(i))
            plt5.scatter(cycle_data["SoC"],cycle_data["dV/dQ"], label="Cycle "+str(i))
            plt6.scatter(cycle_data["Capacity(Ah)"],cycle_data["dV/dQ"], label="Cycle "+str(i))
    
    plt1.legend(bbox_to_anchor=(0.5,-0.07),loc='upper center', ncol=3, fontsize=legend_fontsize)
    plt2.legend(bbox_to_anchor=(0.5,-0.07),loc='upper center', ncol=3, fontsize=legend_fontsize)
    plt3.legend(bbox_to_anchor=(0.5,-0.07),loc='upper center', ncol=3, fontsize=legend_fontsize)
    plt4.legend(bbox_to_anchor=(0.5,-0.07),loc='upper center', ncol=3, fontsize=legend_fontsize)
    plt5.legend(bbox_to_anchor=(0.5,-0.07),loc='upper center', ncol=3, fontsize=legend_fontsize)
    plt6.legend(bbox_to_anchor=(0.5,-0.07),loc='upper center', ncol=3, fontsize=legend_fontsize)
    
    
    fig.savefig('Output/'+str(label)+'dQ_dV_Chg.png')
        
def plot_dQ_dV_DChg(data,cycle=[1],label=""):
    
    if cycle==[1]:
        cycle = [3,int(data["Cycle"].max()/2),data["Cycle"].max()-1]
        
    fig, ((plt1,plt2),(plt3,plt4),(plt5,plt6))=plt.subplots(3,2,figsize=(24, 27))
    
    figure(figsize=(24, 18), dpi=80)
    
    plt1.set_xlabel("Voltage(V)", fontsize=axis_fontsize)
    plt1.set_ylabel("Differential Capacity(dQ/dV)(Ah/V)", fontsize=axis_fontsize)
    plt1.set_title("Differential Capacity versus Voltage", fontsize=title_fontsize)
    plt1.set_xlim(left=data["Voltage(V)"].max(), right=data["Voltage(V)"].min())
    plt1.set_ylim([-12,1])
    plt1.minorticks_on()
    
    plt2.set_xlabel("Depth of Discharge(%)", fontsize=axis_fontsize)
    plt2.set_ylabel("Differential Capacity(dQ/dV)(Ah/V)", fontsize=axis_fontsize)
    plt2.set_title("Differential Capacity vs DoD", fontsize=title_fontsize)
    plt2.set_xlim(left=0, right=100)
    plt2.set_ylim([-12,1])
    plt2.minorticks_on()
    
    plt3.set_xlabel("Discharge Capacity(Ah)", fontsize=axis_fontsize)
    plt3.set_ylabel("Differential Capacity(dQ/dV)(Ah/V)", fontsize=axis_fontsize)
    plt3.set_title("Differential Capacity vs Discharge Capacity", fontsize=title_fontsize)
    plt3.set_xlim(left=data["Capacity(Ah)"].min(), right=data["Capacity(Ah)"].max())
    plt3.set_ylim([-12,1])
    plt3.minorticks_on()
    
    plt4.set_xlabel("Voltage(V)", fontsize=axis_fontsize)
    plt4.set_ylabel("Differential Voltage(dV/dQ)(V/Ah)", fontsize=axis_fontsize)
    plt4.set_title("Differential Voltage versus Voltage", fontsize=title_fontsize)
    plt4.set_xlim(left=data["Voltage(V)"].max(), right=data["Voltage(V)"].min())
    plt4.set_ylim([-12,1])
    plt4.minorticks_on()
    
    plt5.set_xlabel("Depth of Discharge(%)", fontsize=axis_fontsize)
    plt5.set_ylabel("Differential Voltage(dV/dQ)(V/Ah)", fontsize=axis_fontsize)
    plt5.set_title("Differential Voltage vs DoD", fontsize=title_fontsize)
    plt5.set_ylim([-1,0.25])
    plt5.minorticks_on()
    plt5.set_xlim(left=0, right=100)
    
    plt6.set_xlabel("Discharge Capacity(Ah)", fontsize=axis_fontsize)
    plt6.set_ylabel("Differential Voltage(dV/dQ)(V/Ah)", fontsize=axis_fontsize)
    plt6.set_title("Differential Voltage vs Discharge Capacity", fontsize=title_fontsize)
    plt6.set_xlim(left=data["Capacity(Ah)"].min(), right=data["Capacity(Ah)"].max())
    plt6.set_ylim([-1,0.25])
    plt6.minorticks_on()
    
    for i in cycle:
        cycle_data=data[(data["Cycle"]==i) & (data["State"]=="CC DChg")]
        if not cycle_data.empty:
            #periods=max(int(len(cycle_data)/300),1)
            periods=5
            max_capacity=cycle_data["Capacity(Ah)"].max()
            cycle_data["DoD"]=100*cycle_data["Capacity(Ah)"]/max_capacity
            cycle_data["dQ"]=cycle_data["Capacity(Ah)"].rolling(50,min_periods=1).mean().diff(periods)
            cycle_data["dV"]=cycle_data["Voltage(V)"].rolling(50,min_periods=1).mean().diff(periods)
            cycle_data["dQ/dV"]=cycle_data["dQ"]/cycle_data["dV"]
            cycle_data["dV/dQ"]=cycle_data["dV"]/cycle_data["dQ"]
            
            plt1.scatter(cycle_data["Voltage(V)"],cycle_data["dQ/dV"], label="Cycle "+str(i))
            plt2.scatter(cycle_data["DoD"],cycle_data["dQ/dV"], label="Cycle "+str(i))
            plt3.scatter(cycle_data["Capacity(Ah)"],cycle_data["dQ/dV"], label="Cycle "+str(i))
            plt4.scatter(cycle_data["Voltage(V)"],cycle_data["dV/dQ"], label="Cycle "+str(i))
            plt5.scatter(cycle_data["DoD"],cycle_data["dV/dQ"], label="Cycle "+str(i))
            plt6.scatter(cycle_data["Capacity(Ah)"],cycle_data["dV/dQ"], label="Cycle "+str(i))
            
    
    plt1.legend(bbox_to_anchor=(0.5,-0.07),loc='upper center', ncol=3, fontsize=legend_fontsize)
    plt2.legend(bbox_to_anchor=(0.5,-0.07),loc='upper center', ncol=3, fontsize=legend_fontsize)
    plt3.legend(bbox_to_anchor=(0.5,-0.07),loc='upper center', ncol=3, fontsize=legend_fontsize)
    plt4.legend(bbox_to_anchor=(0.5,-0.07),loc='upper center', ncol=3, fontsize=legend_fontsize)
    plt5.legend(bbox_to_anchor=(0.5,-0.07),loc='upper center', ncol=3, fontsize=legend_fontsize)
    plt6.legend(bbox_to_anchor=(0.5,-0.07),loc='upper center', ncol=3, fontsize=legend_fontsize)
    
    fig.savefig('Output/'+str(label)+'dQ_dV_DChg.png')

    
def plot_volt_curr_cap(data,cycle=[1],cap=2.6,label=""):
    figure(figsize=(12, 6), dpi=80)
    plt.xlabel("Cycle Time(s)", fontsize=axis_fontsize)
    #plt.ylabel("")
    plt.title("Voltage(V), Current(A), Capacity(Ah) vs Time(s)", fontsize=title_fontsize)
    #plt.xlim([4.2,2.75])
    plt.minorticks_on()
    for i in cycle:
        cycle_data=data[(data["Cycle"]==i)]
        plt.plot(cycle_data["cycle_time(s)"], cycle_data["Voltage(V)"], label="Voltage - Cycle "+str(i))
        plt.plot(cycle_data["cycle_time(s)"], cycle_data["Current(A)"], label="Current - Cycle "+str(i))
        plt.plot(cycle_data["cycle_time(s)"], cycle_data["Capacity(Ah)"], label="Capacity - Cycle "+str(i))
    if len(cycle)<3:
        plt.legend(loc="upper left", fontsize=legend_fontsize)
    plt.savefig('Output/'+str(label)+'vol_curr_cap.png')
    plt.show()

def plot_cycle_stats(data,label=""):
    summary = cycle_summary(data,False)
    fig, ((plt1,plt2),(plt3,plt4),(plt5,plt6),(plt7,plt8))=plt.subplots(4,2,figsize=(24, 26))
    
    plt1.set_xlabel('Cycle', fontsize=axis_fontsize)
    plt1.set_ylabel('Capacity(Ah)', fontsize=axis_fontsize)
    plt1.set_title("Capacity", fontsize=title_fontsize)
    #ax1.set_ylim([38.5, 58.8])
    plt1.scatter(summary.index,summary["charge_capacity(Ah)"], label="Charge Capacity")
    plt1.scatter(summary.index,summary["discharge_capacity(Ah)"], label="Discharge Capacity")
    plt1.minorticks_on()
    plt1.legend(loc="center", fontsize=legend_fontsize)
    
    plt2.set_xlabel('Cycle', fontsize=axis_fontsize)
    plt2.set_ylabel('Energy(Wh)', fontsize=axis_fontsize)
    plt2.scatter(summary.index,summary["charge_energy(Wh)"], label="Charge Energy")
    plt2.scatter(summary.index,summary["discharge_energy(Wh)"], label="Discharge Energy")
    plt2.minorticks_on()
    plt2.set_title("Energy", fontsize=title_fontsize)
    plt2.legend(loc="center", fontsize=legend_fontsize)
    
    plt3.set_title("Charge Throughput & Output", fontsize=title_fontsize)
    plt3.set_xlabel('Cycle', fontsize=axis_fontsize)
    plt3.set_ylabel('Charge(Ah)', fontsize=axis_fontsize)
    #plt3.set_xlim(left=0)
    #ax1.set_ylim([38.5, 58.8])
    plt3.scatter(summary.index,summary["charge_throughput(Ah)"], label="Charge Throughput")
    plt3.scatter(summary.index,summary["charge_output(Ah)"], label="Charge Output")
    plt3.minorticks_on()
    plt3.legend(loc="upper left", fontsize=legend_fontsize)
    
    plt4.set_title("Energy Throughput & Output", fontsize=title_fontsize)
    plt4.set_xlabel('Cycle', fontsize=axis_fontsize)
    plt4.set_ylabel('Energy(Wh)', fontsize=axis_fontsize)
    #plt4.set_xlim(left=0)
    plt4.scatter(summary.index,summary["energy_throughput(Wh)"], label="Energy Throughput")
    plt4.scatter(summary.index,summary["energy_output(Wh)"], label="Energy Output")
    plt4.minorticks_on()
    plt4.legend(loc="upper left", fontsize=legend_fontsize)
    
    plt5.set_xlabel("Cycle", fontsize=axis_fontsize)
    plt5.set_ylabel("Efficiency(%)", fontsize=axis_fontsize)
    plt5.set_title("Efficiency", fontsize=title_fontsize)
    plt5.set_ylim([75,110])
    plt5.minorticks_on()
    plt5.scatter(summary.index,summary["charge_efficiency"]*100, label="Charge Efficiency")
    plt5.scatter(summary.index,summary["energy_efficiency"]*100, label="Energy Efficiency")
    plt5.legend(loc="lower center", fontsize=legend_fontsize)
    
    plt6.set_xlabel("Cycle", fontsize=axis_fontsize)
    plt6.set_ylabel("Charge Capacity(Ah)", fontsize=axis_fontsize)
    plt6.set_title("Charge Capacity", fontsize=title_fontsize)
    #plt4.set_ylim([0,3])
    plt6.minorticks_on()
    plt6.bar(summary.index,summary["cc_charge_capacity(Ah)"], label="CC Charge Capacity")
    plt6.bar(summary.index,summary["cv_charge_capacity(Ah)"], bottom=summary["cc_charge_capacity(Ah)"], label="CV Charge Capacity")
    plt6.legend(loc="lower center", fontsize=legend_fontsize)
    
    plt7.set_xlabel("Cycle", fontsize=axis_fontsize)
    plt7.set_ylabel("Current(A)", fontsize=axis_fontsize)
    plt7.set_title("Charge and Discharge Currents", fontsize=title_fontsize)
    #plt4.set_ylim([0,3])
    plt7.minorticks_on()
    plt7.scatter(summary.index,summary["cc_charge_current(A)"], label="CC Charge Current")
    plt7.scatter(summary.index,summary["cv_cutoff_current(A)"], label="CV Cut-off Current")
    plt7.scatter(summary.index,summary["discharge_current(A)"], label="Discharge Current")
    plt7.legend(loc="center", fontsize=legend_fontsize)
    
    plt8.set_xlabel("Cycle", fontsize=axis_fontsize)
    plt8.set_ylabel("Cut-off Voltage(V)", fontsize=axis_fontsize)
    plt8.set_title("Upper and Lower Cut-off Voltages", fontsize=title_fontsize)
    #plt8.set_ylim([0,3])
    plt8.minorticks_on()
    plt8.scatter(summary.index,summary["lower_cutoff_voltage(V)"], label="Lower Cut-off Voltage")
    plt8.scatter(summary.index,summary["upper_cutoff_voltage(V)"], label="Upper Cut-off Voltage")
    plt8.legend(loc="lower center", fontsize=legend_fontsize)    
    
    fig.savefig('Output/'+str(label)+'Cycle_Stats.png')

def summary_data(data,label=""):
    
    #cycle= cycle.sort()
    #cycle=range(0,2000,10)
    
    summary = cycle_summary(data,False)
    summary.reset_index(inplace=True)
    
    #summary=pd.read_excel("Cell Summaries/BAK#1_Chg_0.5C_DChg_1C_summary.xlsx", header=0)
    cycle=range(0,int(len(summary))+1,math.ceil(len(summary)/10))
    
    fig, ((plt1),(plt2))=plt.subplots(2,1,figsize=(22, 10))
    
    extract=pd.Series(cycle,name="Cycle" )
    plt1.set_axis_off()
    plt1.set_title("Capacity", fontsize=title_fontsize)
    extract=pd.merge(left=extract,right=summary[["Cycle","charge_capacity(Ah)","cc_charge_capacity(Ah)","cv_charge_capacity(Ah)","discharge_capacity(Ah)","charge_efficiency"]],on="Cycle")
    extract["charge_efficiency"]=extract["charge_efficiency"]*100
    extract["Change in Capacity(%)"]=round((extract.iloc[:,4]-extract.iloc[0,4])*100/extract.iloc[0,4],2)
    extract=round(extract,2)
    extract["Cycle"]=extract["Cycle"].astype(int)
    tbl1=plt1.table(colLabels=extract.columns, cellText=extract.values, rowLoc='left', colLoc='center', cellLoc ='right', loc ='upper left')
    tbl1.set_fontsize(cell_fontsize)
    tbl1.scale(1,2)    
    
    extract=pd.Series(cycle,name="Cycle" )
    plt2.set_axis_off()
    plt2.set_title("Energy", fontsize=title_fontsize)
    extract=pd.merge(left=extract,right=summary[["Cycle","charge_energy(Wh)","cc_charge_energy(Wh)","cv_charge_energy(Wh)","discharge_energy(Wh)","energy_efficiency"]],on="Cycle")
    extract["energy_efficiency"]=extract["energy_efficiency"]*100
    extract["Change in Energy(%)"]=round((extract.iloc[:,4]-extract.iloc[0,4])*100/extract.iloc[0,4],2)
    extract=round(extract,2)
    extract["Cycle"]=extract["Cycle"].astype(int)
    tbl2=plt2.table(colLabels=extract.columns, cellText=extract.values, rowLoc='left', colLoc='center', cellLoc ='right', loc ='upper left')
    tbl2.set_fontsize(cell_fontsize)
    tbl2.scale(1,2) 
    
    fig.savefig('Output/'+str(label)+'_summary.png')
 
def plot_time_series(data,label=""):
    summary = cycle_summary(data,False)
    summary_grouped = summary.groupby(summary['end_time'].dt.date).size().reset_index(name='Cycles')
    fig, ((plt1,plt2),(plt3,plt4))=plt.subplots(2,2,figsize=(24, 12))
    plt1.set_xlabel("Date", fontsize=axis_fontsize)
    plt1.set_ylabel("Cycles", fontsize=axis_fontsize)
    #plt.xlim([datetime.date(2021, 6, 1), datetime.date(2022, 2, 1)])
    #plt.ylim([2.2,2.8])
    plt1.minorticks_on()
    plt1.set_title("Cycles vs Date", fontsize=title_fontsize)
    #plt.ylim([0,3])
    plt1.scatter(summary_grouped['end_time'],summary_grouped["Cycles"],label="Cycles")
    #plt1.plot(summary_grouped['end_time'],summary_grouped["Cycles"], linewidth=1,label="Cycles Trend")
    plt1.legend(loc="lower center", fontsize=legend_fontsize)
    
    plt2.set_xlabel("Time", fontsize=axis_fontsize)
    plt2.set_ylabel("Discharge Capacity(Ah)", fontsize=axis_fontsize)
    #plt.xlim([datetime.date(2021, 6, 1), datetime.date(2022, 2, 1)])
    #plt.ylim([2.2,2.8])
    plt2.minorticks_on()
    plt2.set_title("Discharge Capacity vs Date", fontsize=title_fontsize)
    #plt.ylim([0,3])
    plt2.scatter(summary["end_time"],summary["discharge_capacity(Ah)"], label="Discharge Capacity")
    #plt2.scatter(summary["end_time"],summary["discharge_capacity(Ah)"], linewidth=1,label="Discharge Capacity Trend")
    plt2.legend(loc="lower center", fontsize=legend_fontsize)

    plt3.set_xlabel('Date/Time', fontsize=axis_fontsize)
    plt3.set_ylabel('Discharge Capacity(Ah)', fontsize=axis_fontsize, color="blue")
    plt3.minorticks_on()
    #plt3.set_xlim([datetime.date(2021, 6, 1), datetime.date(2022, 2, 1)])
    #plt3.set_ylim([2.2,2.8])
    plt3.scatter(summary["end_time"],summary["discharge_capacity(Ah)"], label="Discharge Capacity", color="blue")
    plt3.plot(summary["end_time"],summary["discharge_capacity(Ah)"], linewidth=1,label="Discharge Capacity Trend", color="blue")
    plt3.tick_params(axis ='y', labelcolor = "blue")
    plt31 = plt3.twinx()
    plt31.set_ylabel('Cycles', color = "orange")
    #plt31.set_ylim([0,12])
    plt31.scatter(summary_grouped['end_time'],summary_grouped["Cycles"], label="Cycles", color="orange")
    plt31.plot(summary_grouped['end_time'],summary_grouped["Cycles"], linewidth=1,label="Cycles Trend", color = "orange")
    plt31.tick_params(axis ='y', labelcolor = "orange")
    plt31.minorticks_on()
    plt3.set_title("Capacity and Cycles", fontsize=title_fontsize)
    #plt.legend(loc="lower center", fontsize=legend_fontsize)
    
    plt4.set_xlabel("Time", fontsize=axis_fontsize)
    plt4.set_ylabel("Charge Capacity(Ah)", fontsize=axis_fontsize)
    plt4.set_title("Charge Capacity", fontsize=title_fontsize)
    #plt4.set_ylim([0,3])
    plt4.minorticks_on()
    plt4.bar(summary["end_time"],summary["cc_charge_capacity(Ah)"], label="CC Charge Capacity")
    plt4.bar(summary["end_time"],summary["cv_charge_capacity(Ah)"], bottom=summary["cc_charge_capacity(Ah)"], label="CV Charge Capacity")
    plt4.legend(loc="upper right", fontsize=legend_fontsize)
    
    fig.savefig('Output/'+str(label)+'Time_Series.png')

def compare_charge_voltage(cells_data, cycles=[1]):
    
    fig, ((plt1,plt2))=plt.subplots(1,2,figsize=(24, 9))
    fig_name=''
    
    plt1.set_xlabel("State of Charge(%)", fontsize=axis_fontsize)
    plt1.set_ylabel("Voltage(V)", fontsize=axis_fontsize)
    plt1.set_title("Voltage vs State of Charge Comparison", fontsize=title_fontsize)
    plt1.set_xlim([0,100])
    plt1.minorticks_on()
    
    j=0
    for cell in cells_data:
        cell_data = cells_data[cell]["data"]
        for i in cycles:
            cycle_data=cell_data[(cell_data["Cycle"]==i) & (cell_data["State"]=="CCCV Chg")]
            if not cycle_data.empty:
                max_capacity=cycle_data["Capacity(Ah)"].max()
                cycle_data["SoC"]=100*cycle_data["Capacity(Ah)"]/max_capacity #cells_data[cell]["capacity"]
                plt1.plot(cycle_data["SoC"],cycle_data["Voltage(V)"], linestyle=line_style[j], label=str(cell)+" Cycle "+str(i)+" Chg @ "+cells_data[cell]["chg_rate"])
            #For separated CC CV
            cycle_data=cell_data[(cell_data["Cycle"]==i) & ((cell_data["State"]=="CC Chg")|(cell_data["State"]=="CV Chg"))]
            if not cycle_data.empty:
                cc_max = cycle_data[cycle_data["State"]=="CC Chg"]["Capacity(Ah)"].max()
                cv_max = cycle_data[cycle_data["State"]=="CV Chg"]["Capacity(Ah)"].max()
                max_capacity = cc_max + cv_max
                cycle_data["SoC"]=np.where(cycle_data["State"]=="CC Chg",100*cycle_data["Capacity(Ah)"]/max_capacity,100*(cc_max+cycle_data["Capacity(Ah)"])/max_capacity)
                plt1.plot(cycle_data["SoC"],cycle_data["Voltage(V)"], linestyle=line_style[j], label=str(cell)+" Cycle "+str(i)+" Chg @ "+cells_data[cell]["chg_rate"])
        fig_name=fig_name+str(cell)+'_'
        j=j+1
    plt1.legend(bbox_to_anchor=(0.5,-0.07),loc='upper center', ncol=len(cells_data), fontsize=legend_fontsize)
    
    plt2.set_xlabel("Charge Capacity(Ah)", fontsize=axis_fontsize)
    plt2.set_ylabel("Voltage(V)", fontsize=axis_fontsize)
    plt2.set_title("Voltage vs Charge Capacity Comparison", fontsize=title_fontsize)
    #plt.xlim([0,100])
    plt2.minorticks_on()
    
    j=0
    for cell in cells_data:
        cell_data = cells_data[cell]["data"]
        for i in cycles:
            cycle_data=cell_data[(cell_data["Cycle"]==i) & (cell_data["State"]=="CCCV Chg")]
            if not cycle_data.empty:
                plt2.plot(cycle_data["Capacity(Ah)"],cycle_data["Voltage(V)"], linestyle=line_style[j], label=str(cell)+" Cycle "+str(i)+" Chg @ "+cells_data[cell]["chg_rate"])
            #For separated CC CV
            cycle_data=cell_data[(cell_data["Cycle"]==i) & ((cell_data["State"]=="CC Chg")|(cell_data["State"]=="CV Chg"))]
            if not cycle_data.empty:
                cc_max = cycle_data[cycle_data["State"]=="CC Chg"]["Capacity(Ah)"].max()
                cycle_data["CCCV_Capacity"]=np.where(cycle_data["State"]=="CC Chg",cycle_data["Capacity(Ah)"],cc_max+cycle_data["Capacity(Ah)"])
                plt2.plot(cycle_data["CCCV_Capacity"],cycle_data["Voltage(V)"], linestyle=line_style[j], label=str(cell)+" Cycle "+str(i)+" Chg @ "+cells_data[cell]["chg_rate"])
        j=j+1
    plt2.legend(bbox_to_anchor=(0.5,-0.07),loc='upper center', ncol=len(cells_data), fontsize=legend_fontsize)
    #plt.grid()
    
    fig.savefig('Output/'+fig_name+'Volt_Charging.png')
    
def compare_discharge_voltage(cells_data, cycles=[1]):
    
    fig, ((plt1,plt2))=plt.subplots(1,2,figsize=(24, 9))
    fig_name=''
    
    plt1.set_xlabel("Depth of Discharge(%)", fontsize=axis_fontsize)
    plt1.set_ylabel("Voltage(V)", fontsize=axis_fontsize)
    plt1.set_title("Voltage vs Depth of Discharge Comparison", fontsize=title_fontsize)
    plt1.set_xlim([0,100])
    plt1.minorticks_on()
    
    j=0
    for cell in cells_data:
        cell_data = cells_data[cell]["data"]
        for i in cycles:
            cycle_data=cell_data[(cell_data["Cycle"]==i) & (cell_data["State"]=="CC DChg")]
            if not cycle_data.empty:
                max_capacity=cycle_data["Capacity(Ah)"].max()
                cycle_data["DoD"]=100*cycle_data["Capacity(Ah)"]/max_capacity#cells_data[cell]["capacity"]
                plt1.plot(cycle_data["DoD"],cycle_data["Voltage(V)"], linestyle=line_style[j], label=str(cell)+" Cycle "+str(i)+" DChg @ "+cells_data[cell]["dchg_rate"])
        fig_name=fig_name+str(cell)+'_'
        j=j+1
    plt1.legend(bbox_to_anchor=(0.5,-0.07),loc='upper center', ncol=len(cells_data), fontsize=legend_fontsize) 
    
    plt2.set_xlabel("Discharge Capacity(Ah)", fontsize=axis_fontsize)
    plt2.set_ylabel("Voltage(V)", fontsize=axis_fontsize)
    plt2.set_title("Voltage vs Discharge Capacity Comparison", fontsize=title_fontsize)
    plt2.minorticks_on()
    j=0
    for cell in cells_data:
        cell_data = cells_data[cell]["data"]
        for i in cycles:
            cycle_data=cell_data[(cell_data["Cycle"]==i) & (cell_data["State"]=="CC DChg")]
            if not cycle_data.empty:
                plt2.plot(cycle_data["Capacity(Ah)"],cycle_data["Voltage(V)"], linestyle=line_style[j], label=str(cell)+" Cycle "+str(i)+" DChg @ "+cells_data[cell]["dchg_rate"])
        j=j+1
    #if len(cycles)*len(cells_data)<10:
    plt2.legend(bbox_to_anchor=(0.5,-0.07),loc='upper center', ncol=len(cells_data), fontsize=legend_fontsize)
    fig.savefig('Output/'+fig_name+'Volt_Discharging.png')

def compare_charge_current(cells_data, cycles=[1]):
    
    fig, ((plt1,plt2,plt3))=plt.subplots(1,3,figsize=(24, 9))
    fig_name=''
    
    plt1.set_xlabel("State of Charge(%)", fontsize=axis_fontsize)
    plt1.set_ylabel("Current(A)", fontsize=axis_fontsize)
    plt1.set_title("Current vs State of Charge Comparison", fontsize=title_fontsize)
    plt1.set_xlim([0,100])
    plt1.minorticks_on()
    
    j=0
    for cell in cells_data:
        cell_data = cells_data[cell]["data"]
        for i in cycles:
            cycle_data=cell_data[(cell_data["Cycle"]==i) & (cell_data["State"]=="CCCV Chg")]
            if not cycle_data.empty:
                max_capacity=cycle_data["Capacity(Ah)"].max()
                cycle_data["SoC"]=100*cycle_data["Capacity(Ah)"]/max_capacity #cells_data[cell]["capacity"]
                plt1.plot(cycle_data["SoC"],cycle_data["Current(A)"], linestyle=line_style[j], label=str(cell)+"Cycle "+str(i)+" Chg @ "+cells_data[cell]["chg_rate"])
        fig_name=fig_name+str(cell)+'_'
        j=j+1
    plt1.legend(bbox_to_anchor=(0.5,-0.07),loc='upper center', ncol=len(cells_data), fontsize=legend_fontsize)
    
    plt2.set_xlabel("Charge Capacity(Ah)", fontsize=axis_fontsize)
    plt2.set_ylabel("Current(A)", fontsize=axis_fontsize)
    plt2.set_title("Current vs Charge Capacity Comparison", fontsize=title_fontsize)
    #plt.xlim([0,100])
    plt2.minorticks_on()
    j=0
    for cell in cells_data:
        cell_data = cells_data[cell]["data"]
        for i in cycles:
            cycle_data=cell_data[(cell_data["Cycle"]==i) & (cell_data["State"]=="CCCV Chg")]
            if not cycle_data.empty:
                plt2.plot(cycle_data["Capacity(Ah)"],cycle_data["Current(A)"], linestyle=line_style[j], label=str(cell)+"Cycle "+str(i)+" Chg @ "+cells_data[cell]["chg_rate"])
        j=j+1
    plt2.legend(bbox_to_anchor=(0.5,-0.07),loc='upper center', ncol=len(cells_data), fontsize=legend_fontsize)
    #plt.grid()
    
    plt3.set_xlabel("Charge Time(s)", fontsize=axis_fontsize)
    plt3.set_ylabel("Charge Current(A)", fontsize=axis_fontsize)
    plt3.set_title("Charge Current vs Time", fontsize=title_fontsize)
    plt3.minorticks_on()
    #plt6.set_xlim([0,])
    j=0
    for cell in cells_data:
        cell_data = cells_data[cell]["data"]
        for i in cycles:
            cycle_data=cell_data[(cell_data["Cycle"]==i) & (cell_data["State"]=="CCCV Chg")]
            if not cycle_data.empty:
                plt3.plot(cycle_data["Relative Time(s)"],cycle_data["Current(A)"], linestyle=line_style[j], label=str(cell)+"Cycle "+str(i)+" Chg @ "+cells_data[cell]["chg_rate"])
        j=j+1
    plt3.legend(bbox_to_anchor=(0.5,-0.07),loc='upper center', ncol=len(cells_data), fontsize=legend_fontsize)
    
    fig.savefig('Output/'+fig_name+'Current_Charging.png')

def compare_capacity(cells_data):
    
    for cell in cells_data:
        cell_data = cells_data[cell]["data"]
        summary = cycle_summary(cell_data,True,'Cell Summaries/'+str(cell)+'_Chg_'+cells_data[cell]["chg_rate"]+'_DChg_'+cells_data[cell]["dchg_rate"]+'_summary.xlsx')
    
    fig, ((plt1,plt2))=plt.subplots(1,2,figsize=(24, 9))
    fig_name=''

    plt1.set_xlabel("Cycle", fontsize=axis_fontsize)
    plt1.set_ylabel("Discharge Capacity(Ah)", fontsize=axis_fontsize)
    plt1.set_title("Discharge Capacity Comparison", fontsize=title_fontsize)
    #plt.ylim([0,3])
    plt1.minorticks_on()
    j=0
    for cell in cells_data:
        cell_data = cells_data[cell]["data"]
        summary = pd.read_excel('Cell Summaries/'+str(cell)+'_Chg_'+cells_data[cell]["chg_rate"]+'_DChg_'+cells_data[cell]["dchg_rate"]+'_summary.xlsx')
        plt1.scatter(summary["Cycle"],summary["discharge_capacity(Ah)"],linestyle=line_style[j], label=str(cell)+" DChg @ "+cells_data[cell]["dchg_rate"])
        fig_name=fig_name+str(cell)+'_'
        j=j+1
    plt1.legend(bbox_to_anchor=(0.5,-0.07),loc='upper center', ncol=len(cells_data), fontsize=legend_fontsize)
    
    plt2.set_xlabel("Cycle", fontsize=axis_fontsize)
    plt2.set_ylabel("Discharge Energy(Wh)", fontsize=axis_fontsize)
    plt2.set_title("Discharge Energy Comparison", fontsize=title_fontsize)
    #plt.ylim([0,3])
    plt2.minorticks_on()
    j=0
    for cell in cells_data:
        cell_data = cells_data[cell]["data"]
        summary = pd.read_excel('Cell Summaries/'+str(cell)+'_Chg_'+cells_data[cell]["chg_rate"]+'_DChg_'+cells_data[cell]["dchg_rate"]+'_summary.xlsx')
        plt2.scatter(summary["Cycle"],summary["discharge_energy(Wh)"],linestyle=line_style[j], label=str(cell)+" DChg @ "+cells_data[cell]["dchg_rate"])
        j=j+1
    plt2.legend(bbox_to_anchor=(0.5,-0.07),loc='upper center', ncol=len(cells_data), fontsize=legend_fontsize)
     
    fig.savefig('Output/'+fig_name+'Capacity.png')

def compare_efficiency(cells_data):
    
    for cell in cells_data:
        cell_data = cells_data[cell]["data"]
        summary = cycle_summary(cell_data,True,'Cell Summaries/'+str(cell)+'_Chg_'+cells_data[cell]["chg_rate"]+'_DChg_'+cells_data[cell]["dchg_rate"]+'_summary.xlsx')
    
    fig, ((plt1,plt2))=plt.subplots(1,2,figsize=(24, 9))
    fig_name=''
    
    plt1.set_xlabel("Cycle", fontsize=axis_fontsize)
    plt1.set_ylabel("Charge Efficiency(%)", fontsize=axis_fontsize)
    plt1.set_title("Charge Efficiency Comparison", fontsize=title_fontsize)
    plt1.set_ylim([90,110])
    plt1.minorticks_on()

    for cell in cells_data:
        cell_data = cells_data[cell]["data"]
        summary = pd.read_excel('Cell Summaries/'+str(cell)+'_Chg_'+cells_data[cell]["chg_rate"]+'_DChg_'+cells_data[cell]["dchg_rate"]+'_summary.xlsx')
        plt1.scatter(summary["Cycle"],summary["charge_efficiency"]*100, label=str(cell)+" Chg @ "+cells_data[cell]["chg_rate"]+" DChg @ "+cells_data[cell]["dchg_rate"])
        fig_name=fig_name+str(cell)+'_'
    plt1.legend(bbox_to_anchor=(0.5,-0.07),loc='upper center', ncol=len(cells_data), fontsize=legend_fontsize)
    
    plt2.set_xlabel("Cycle", fontsize=axis_fontsize)
    plt2.set_ylabel("Energy Efficiency(%)", fontsize=axis_fontsize)
    plt2.set_title("Energy Efficiency Comparison", fontsize=title_fontsize)
    plt2.set_ylim([90,100])
    plt2.minorticks_on()
    for cell in cells_data:
        cell_data = cells_data[cell]["data"]
        summary = pd.read_excel('Cell Summaries/'+str(cell)+'_Chg_'+cells_data[cell]["chg_rate"]+'_DChg_'+cells_data[cell]["dchg_rate"]+'_summary.xlsx')
        plt2.scatter(summary["Cycle"],summary["energy_efficiency"]*100, label=str(cell)+" Chg @ "+cells_data[cell]["chg_rate"]+" DChg @ "+cells_data[cell]["dchg_rate"])
    plt2.legend(bbox_to_anchor=(0.5,-0.07),loc='upper center', ncol=len(cells_data), fontsize=legend_fontsize)
    fig.savefig('Output/'+fig_name+'Efficiency.png')

def compare_cc_cv_capacity(cells_data):
    
    for cell in cells_data:
        cell_data = cells_data[cell]["data"]
        summary = cycle_summary(cell_data,True,'Cell Summaries/'+str(cell)+'_Chg_'+cells_data[cell]["chg_rate"]+'_DChg_'+cells_data[cell]["dchg_rate"]+'_summary.xlsx')
        
    # Figure size
    #plt.figure(figsize=(10,5))
    figure(figsize=(21, 12), dpi=80)
    fig_name=''

    plt.xlabel("Cycle", fontsize=axis_fontsize)
    plt.ylabel("Charge Capacity(Ah)", fontsize=axis_fontsize)
    plt.title("CC CV Charge Capacity Comparison", fontsize=title_fontsize)
    #plt1.set_ylim([90,110])
    plt.minorticks_on()
    
    # Width of a bar 
    width = 0.3

    # xticks()
    # First argument - A list of positions at which ticks should be placed
    # Second argument -  A list of labels to place at the given locations
    #plt.xticks(ind + width / 2, ('Xtick1', 'Xtick3', 'Xtick3'))
    
    j=0
    for cell in cells_data:
        cell_data = cells_data[cell]["data"]
        summary = pd.read_excel('Cell Summaries/'+str(cell)+'_Chg_'+cells_data[cell]["chg_rate"]+'_DChg_'+cells_data[cell]["dchg_rate"]+'_summary.xlsx')
        N = len(summary) # Numbers of pairs of bars you want
        ind = np.arange(N) # Position of bars on x-axis
        ind=ind+1
        ind=ind+(j*width)
        plt.bar(ind, summary["cc_charge_capacity(Ah)"] , width, label=str(cell)+' CC Charge Capacity')
        plt.bar(ind, summary["cv_charge_capacity(Ah)"], width,bottom=summary["cc_charge_capacity(Ah)"],label=str(cell)+" CV Charge Capacity")
        fig_name=fig_name+str(cell)+'_'
        j=j+1
    plt.xlim(left=1)
    plt.legend(bbox_to_anchor=(0.5,-0.07),loc='upper center', ncol=len(cells_data), fontsize=legend_fontsize)
    plt.savefig('Output/'+fig_name+'CC_CV_Capacity.png')


def compare_DiffCap_Voltage(cells_data, cycles=[1]):    
    
    figure(figsize=(12, 12), dpi=80)
    plt.xlabel("Voltage(V)", fontsize=axis_fontsize)
    plt.ylabel("Differential Capacity(dQ/dV)(Ah/V)", fontsize=axis_fontsize)
    plt.title("Comparison of Differential Capacity", fontsize=title_fontsize)
    plt.xlim([2.5,4.2])
    plt.ylim([-10,15])
    plt.minorticks_on()
    fig_name=''
    j=0
    for cell in cells_data:
        cell_data = cells_data[cell]["data"]
        for i in cycles:
            cycle_chg_data=extract_cycle_state(cell_data,i,"CCCV Chg")
            cycle_chg_data["dQ"]=cycle_chg_data["Capacity(Ah)"].diff(periods=50)
            cycle_chg_data["dV"]=cycle_chg_data["Voltage(V)"].diff(periods=50)
            cycle_chg_data["dQ/dV"]=cycle_chg_data["dQ"]/cycle_chg_data["dV"]
            plt.plot(cycle_chg_data["Voltage(V)"],cycle_chg_data["dQ/dV"], linestyle=line_style[j], label=str(cell)+"Chg Cycle "+str(i))
            
            cycle_dchg_data=extract_cycle_state(cell_data,i,"CC DChg")
            cycle_dchg_data["dQ"]=cycle_dchg_data["Capacity(Ah)"].diff(periods=25)
            cycle_dchg_data["dV"]=cycle_dchg_data["Voltage(V)"].diff(periods=25)
            cycle_dchg_data["dQ/dV"]=cycle_dchg_data["dQ"]/cycle_dchg_data["dV"]
            plt.plot(cycle_dchg_data["Voltage(V)"],cycle_dchg_data["dQ/dV"], linestyle=line_style[j], label=str(cell)+"DChg Cycle "+str(i))
            
        fig_name=fig_name+str(cell)+'_'
        j=j+1
    plt.legend(bbox_to_anchor=(0.5,-0.07),loc='upper center', ncol=len(cells_data), fontsize=legend_fontsize)   
    plt.savefig('Output/'+fig_name[:-1]+'-ChgDiffCap.png')
    plt.show()


def plot_di_dt(data,cycle=[1],capacity=2.6):
    figure(figsize=(12, 6), dpi=80)
    plt.xlabel("State of Charge(%)", fontsize=axis_fontsize)
    plt.ylabel("di/dt", fontsize=axis_fontsize)
    plt.title("di/dt vs State of Charge", fontsize=title_fontsize)
    plt.xlim([0,100])
    for i in cycle:
        cycle_chg_data=data[(data["Cycle"]==i) & (data["State"]=="CCCV Chg")]
        cycle_chg_data["SoC"]=100*cycle_chg_data["Capacity(Ah)"]/capacity
        cycle_chg_data["di"]=cycle_chg_data["Current(A)"].diff(periods=45)
        cycle_chg_data["dt_for_di"]=cycle_chg_data["Relative Time(s)"].diff(periods=45)
        cycle_chg_data["di_dt"]=cycle_chg_data["di"]/cycle_chg_data["dt_for_di"]
        plt.plot(cycle_chg_data["SoC"],cycle_chg_data["di_dt"], label="Cycle "+str(i))
    
    plt.legend(bbox_to_anchor=(0.5,-0.07),loc='upper center', ncol=5, fontsize=legend_fontsize)
    plt.savefig('Output/di_dt.png')
    plt.show()

def compare_di_dt(cells_data, cycles=[1]):    
    figure(figsize=(12, 6), dpi=80)
    plt.xlabel("State of Charge(%)", fontsize=axis_fontsize)
    plt.ylabel("di/dt", fontsize=axis_fontsize)
    plt.title("di/dt vs State of Charge", fontsize=title_fontsize)
    plt.xlim([0,100])
    plt.minorticks_on()
    fig_name=''
    for cell in cells_data:
        cell_data = cells_data[cell]["data"]
        for i in cycles:
            cycle_chg_data=cell_data[(cell_data["Cycle"]==i) & (cell_data["State"]=="CCCV Chg")]
            cycle_chg_data["SoC"]=100*cycle_chg_data["Capacity(Ah)"]/cells_data[cell]["capacity"]
            cycle_chg_data["di"]=cycle_chg_data["Current(A)"].diff(periods=45)
            cycle_chg_data["dt_for_di"]=cycle_chg_data["Relative Time(s)"].diff(periods=45)
            cycle_chg_data["di_dt"]=cycle_chg_data["di"]/cycle_chg_data["dt_for_di"]
            plt.plot(cycle_chg_data["SoC"],cycle_chg_data["di_dt"], label=str(cell)+" Cycle "+str(i))
        fig_name=fig_name+str(cell)+'_'
    plt.legend(bbox_to_anchor=(0.5,-0.07),loc='upper center', ncol=len(cells_data), fontsize=legend_fontsize)
    plt.savefig('Output/'+fig_name+'di_dt.png')
    plt.show()
    
def plot_cband(data,step=[1],label=""):
    
    if step==[1]:
        step = data['Steps'].unique()
    
    fig, ((plt1,plt2,plt3),(plt4,plt5,plt6))=plt.subplots(2,3,figsize=(24, 30))
    
    #fig.suptitle("Voltage")
    #fig.tight_layout(pad=3)
    
    plt1.set_xlabel("Depth of Discharge(%)", fontsize=axis_fontsize)
    plt1.set_ylabel("Discharge Voltage(V)", fontsize=axis_fontsize)
    plt1.set_title("Discharge Voltage vs Depth of Discharge", fontsize=title_fontsize)
    #plt1.set_xlim([0,100])
    plt1.minorticks_on()
    for i in step:
        #steps=data[(data["Steps"]==i)]["Steps"].unique()
        step_data=data[(data["Steps"]==i) & (data["State"]=="CC DChg")]
        max_capacity=step_data["Capacity(Ah)"].max()
        step_data.loc[:,"DoD"]=100*step_data.loc[:,"Capacity(Ah)"]/max_capacity
        step_data.loc[:,"SoC"]=100*(1-step_data.loc[:,"Capacity(Ah)"]/max_capacity)
        step_label=round(step_data["Current(A)"].mean()/max_capacity,1)
        if not step_data.empty:
            plt1.plot(step_data["DoD"],step_data["Voltage(V)"], label=str(step_label)+"C" )
            plt4.plot(step_data["SoC"],step_data["Voltage(V)"], label=str(step_label)+"C" )
    plt1.legend(bbox_to_anchor=(0.5,-0.07),loc='upper center', ncol=4, fontsize=legend_fontsize)
    
    plt2.set_xlabel("Discharge Capacity(Ah)", fontsize=axis_fontsize)
    plt2.set_ylabel("Discharge Voltage(V)", fontsize=axis_fontsize)
    plt2.set_title("Discharge Voltage vs Discharge Capacity", fontsize=title_fontsize)
    #plt2.set_xlim([0,1.2*capacity])
    plt2.minorticks_on()
    for i in step:
        step_data=data[(data["Steps"]==i) & (data["State"]=="CC DChg")]
        max_capacity=step_data["Capacity(Ah)"].max()
        step_label=round(step_data["Current(A)"].mean()/max_capacity,1)
        if not step_data.empty:
            plt2.plot(step_data["Capacity(Ah)"],step_data["Voltage(V)"], label=str(step_label)+"C")
    plt2.legend(bbox_to_anchor=(0.5,-0.07),loc='upper center', ncol=4, fontsize=legend_fontsize)
    
    plt3.set_xlabel("Discharge Time(s)", fontsize=axis_fontsize)
    plt3.set_ylabel("Discharge Voltage(V)", fontsize=axis_fontsize)
    plt3.set_title("Discharge Voltage vs Discharge Time", fontsize=title_fontsize)
    plt3.minorticks_on()
    #plt3.set_xlim(left=0)
    for i in step:
        step_data=data[(data["Steps"]==i) & (data["State"]=="CC DChg")]
        max_capacity=step_data["Capacity(Ah)"].max()
        step_label=round(step_data["Current(A)"].mean()/max_capacity,1)
        if not step_data.empty:
            plt3.plot(step_data["Relative Time(s)"],step_data["Voltage(V)"], label=str(step_label)+"C")
    plt3.legend(bbox_to_anchor=(0.5,-0.07),loc='upper center', ncol=4, fontsize=legend_fontsize)

    plt4.set_xlabel("State of Charge(%)", fontsize=axis_fontsize)
    plt4.set_ylabel("Charge Voltage(V)", fontsize=axis_fontsize)
    plt4.set_title("Charge Voltage vs State of Charge", fontsize=title_fontsize)
    plt4.minorticks_on()
    #plt4.set_xlim([0,100])
    for i in step:
        step_data=data[(data["Steps"]==i) & (data["State"]=="CCCV Chg")]
        max_capacity=step_data["Capacity(Ah)"].max()
        step_label=round(step_data["Current(A)"].max()/max_capacity,1)
        if not step_data.empty:
            max_capacity=step_data["Capacity(Ah)"].max()
            step_data["SoC"]=100*step_data["Capacity(Ah)"]/max_capacity
            plt4.plot(step_data["SoC"],step_data["Voltage(V)"], label=str(step_label)+"C")
        #For separated CC CV
        step_data=data[(data["Steps"].isin([i,i+1])) & ((data["State"]=="CC Chg")|(data["State"]=="CV Chg"))]
        if not step_data.empty:
            cc_max = step_data[step_data["State"]=="CC Chg"]["Capacity(Ah)"].max()
            cv_max = step_data[step_data["State"]=="CV Chg"]["Capacity(Ah)"].max()
            max_capacity = cc_max + cv_max
            step_label=round(step_data["Current(A)"].max()/max_capacity,1)
            step_data["SoC"]=np.where(step_data["State"]=="CC Chg",100*step_data["Capacity(Ah)"]/max_capacity,100*(cc_max+step_data["Capacity(Ah)"])/max_capacity)
            plt4.plot(step_data["SoC"],step_data["Voltage(V)"], label=str(step_label)+"C")
    plt4.legend(bbox_to_anchor=(0.5,-0.07),loc='upper center', ncol=4, fontsize=legend_fontsize)
    
    plt5.set_xlabel("Charge Capacity(Ah)", fontsize=axis_fontsize)
    plt5.set_ylabel("Charge Voltage(V)", fontsize=axis_fontsize)
    plt5.set_title("Charge Voltage vs Charge Capacity", fontsize=title_fontsize)
    plt5.minorticks_on()
    #plt5.set_xlim([0,1.2*capacity])
    for i in step:
        step_data=data[(data["Steps"]==i) & (data["State"]=="CCCV Chg")]
        max_capacity=step_data["Capacity(Ah)"].max()
        step_label=round(step_data["Current(A)"].max()/max_capacity,1)
        if not step_data.empty:
            plt5.plot(step_data["Capacity(Ah)"],step_data["Voltage(V)"], label=str(step_label)+"C")
        #For separated CC CV
        step_data=data[(data["Steps"].isin([i,i+1])) & ((data["State"]=="CC Chg")|(data["State"]=="CV Chg"))]
        if not step_data.empty:
            cc_max = step_data[step_data["State"]=="CC Chg"]["Capacity(Ah)"].max()
            cv_max = step_data[step_data["State"]=="CV Chg"]["Capacity(Ah)"].max()
            max_capacity = cc_max + cv_max
            step_label=round(step_data["Current(A)"].max()/max_capacity,1)
            step_data["CCCV_Capacity"]=np.where(step_data["State"]=="CC Chg",step_data["Capacity(Ah)"],cc_max+step_data["Capacity(Ah)"])
            plt5.plot(step_data["CCCV_Capacity"],step_data["Voltage(V)"], label=str(step_label)+"C")
    plt5.legend(bbox_to_anchor=(0.5,-0.07),loc='upper center', ncol=4, fontsize=legend_fontsize)
    
    plt6.set_xlabel("Charge Time(s)", fontsize=axis_fontsize)
    plt6.set_ylabel("Charge Voltage(V)", fontsize=axis_fontsize)
    plt6.set_title("Charge Voltage vs Time", fontsize=title_fontsize)
    plt6.minorticks_on()
    #plt6.set_xlim([0,])
    for i in step:
        step_data=data[(data["Steps"]==i) & (data["State"]=="CCCV Chg")]
        max_capacity=step_data["Capacity(Ah)"].max()
        step_label=round(step_data["Current(A)"].max()/max_capacity,1)
        if not step_data.empty:
            plt6.plot(step_data["Relative Time(s)"],step_data["Voltage(V)"], label=str(step_label)+"C")
        #For separated CC CV
        step_data=data[(data["Steps"].isin([i,i+1])) & ((data["State"]=="CC Chg")|(data["State"]=="CV Chg"))]
        if not step_data.empty:
            cc_time = step_data[step_data["State"]=="CC Chg"]["Relative Time(s)"].max()
            cc_max = step_data[step_data["State"]=="CC Chg"]["Capacity(Ah)"].max()
            cv_max = step_data[step_data["State"]=="CV Chg"]["Capacity(Ah)"].max()
            max_capacity = cc_max + cv_max
            step_label=round(step_data["Current(A)"].max()/max_capacity,1)
            step_data["CCCV_Time"]=np.where(step_data["State"]=="CC Chg",step_data["Relative Time(s)"],cc_time+step_data["Relative Time(s)"])
            plt6.plot(step_data["CCCV_Time"],step_data["Voltage(V)"], label=str(step_label)+"C")
    plt6.legend(bbox_to_anchor=(0.5,-0.07),loc='upper center', ncol=4, fontsize=legend_fontsize)
    
    fig.savefig('Output/'+str(label)+'CBand.png')
    
def plot_cband_voltage(data,step=[1],label=""):
    
    if step==[1]:
        step = data['Steps'].unique()
    
    fig, plt1=plt.subplots(1,1,figsize=(18, 12))
    
    #fig.suptitle("Voltage")
    #fig.tight_layout(pad=3)
    
    plt1.set_xlabel("State of Charge(%)", fontsize=axis_fontsize)
    plt1.set_ylabel("Voltage(V)", fontsize=axis_fontsize)
    plt1.set_title("Voltage vs State of Charge", fontsize=title_fontsize)
    #plt1.set_xlim([0,100])
    plt1.minorticks_on()
    for i in step:
        #steps=data[(data["Steps"]==i)]["Steps"].unique()
        step_data=data[(data["Steps"]==i) & (data["State"]=="CC DChg")]
        max_capacity=step_data["Capacity(Ah)"].max()
        step_data.loc[:,"SoC"]=100*(1-step_data.loc[:,"Capacity(Ah)"]/max_capacity)
        step_label=round(step_data["Current(A)"].mean()/max_capacity,1)
        if not step_data.empty:
            plt1.plot(step_data["SoC"],step_data["Voltage(V)"], label=str(step_label)+"C" )
    

    #plt4.set_xlim([0,100])
    for i in step:
        step_data=data[(data["Steps"]==i) & (data["State"]=="CCCV Chg")]
        max_capacity=step_data["Capacity(Ah)"].max()
        step_label=round(step_data["Current(A)"].max()/max_capacity,1)
        if not step_data.empty:
            max_capacity=step_data["Capacity(Ah)"].max()
            step_data["SoC"]=100*step_data["Capacity(Ah)"]/max_capacity
            plt1.plot(step_data["SoC"],step_data["Voltage(V)"], label=str(step_label)+"C")
        #For separated CC CV
        step_data=data[(data["Steps"].isin([i,i+1])) & ((data["State"]=="CC Chg")|(data["State"]=="CV Chg"))]
        if not step_data.empty:
            cc_max = step_data[step_data["State"]=="CC Chg"]["Capacity(Ah)"].max()
            cv_max = step_data[step_data["State"]=="CV Chg"]["Capacity(Ah)"].max()
            max_capacity = cc_max + cv_max
            step_label=round(step_data["Current(A)"].max()/max_capacity,1)
            step_data["SoC"]=np.where(step_data["State"]=="CC Chg",100*step_data["Capacity(Ah)"]/max_capacity,100*(cc_max+step_data["Capacity(Ah)"])/max_capacity)
            plt1.plot(step_data["SoC"],step_data["Voltage(V)"], label=str(step_label)+"C")

    plt1.legend(bbox_to_anchor=(0.5,-0.07),loc='upper center', ncol=10, fontsize=legend_fontsize)
    
    fig.savefig('Output/'+str(label)+'CBand.png')

def compare_cell_stats():
    path='/Cell Summaries'
    path = os.getcwd()+path
    files = glob.glob(path + "/*.xlsx")
    i=0
    fig,plt1=plt.subplots(1,1,figsize=(18, 10))
    for file in files:
        sheet=pd.read_excel(file)
        label=file[file.rfind('/')+1:-5]
        sheet.plot(ax=plt1,color=color_palette[i],x='Cycle',y='charge_capacity(Ah)',kind='scatter',label=label,xlabel='Cycle',ylabel='Capacity(Ah)')
        i=i+1
    plt1.legend(fontsize=legend_fontsize,loc=(1.01,0.01))#facecolor='k', labelcolor='w'
    plt1.xaxis.label.set_size(axis_fontsize)
    plt1.yaxis.label.set_size(axis_fontsize)
    plt.grid()#axis = 'y'
    fig.suptitle("Cell Capacity - Charge",x=0.1,y=0.9,fontweight='bold',fontsize=fig_title_size,verticalalignment='bottom',ha='left')
    
    i=0
    fig,plt1=plt.subplots(1,1,figsize=(18, 10))
    for file in files:
        sheet=pd.read_excel(file)
        label=file[file.rfind('/')+1:-5]
        sheet.plot(ax=plt1,color=color_palette[i],x='Cycle',y='discharge_capacity(Ah)',kind='scatter',label=label,xlabel='Cycle',ylabel='Capacity(Ah)')#marker='^',
        i=i+1
    plt1.legend(fontsize=legend_fontsize,loc=(1.01,0.01))
    plt1.xaxis.label.set_size(axis_fontsize)
    plt1.yaxis.label.set_size(axis_fontsize)
    fig.suptitle("Cell Capacity - Discharge",x=0.2,y=0.9,fontweight='bold',fontsize=fig_title_size,verticalalignment='bottom')
    
    
    i=0
    fig,plt1=plt.subplots(1,1,figsize=(18, 10))
    for file in files:
        sheet=pd.read_excel(file)
        label=file[file.rfind('/')+1:-5]
        sheet.plot(ax=plt1,color=color_palette[i],x='Cycle',y='charge_efficiency',kind='scatter',label=label,xlabel='Cycle',ylabel='Efficiency')
        i=i+1
    plt1.legend(fontsize=legend_fontsize,loc=(1.01,0.01))
    plt1.xaxis.label.set_size(axis_fontsize)
    plt1.yaxis.label.set_size(axis_fontsize)
    fig.suptitle("Coulombic Efficiency",x=0.2,y=0.9,fontweight='bold',fontsize=fig_title_size,verticalalignment='bottom')
    
    i=0
    fig,plt1=plt.subplots(1,1,figsize=(18, 10))
    for file in files:
        sheet=pd.read_excel(file)
        label=file[file.rfind('/')+1:-5]
        sheet.plot(ax=plt1,color=color_palette[i],x='Cycle',y='charge_energy(Wh)',kind='scatter',label=label,xlabel='Cycle',ylabel='Energy(Wh)')
        i=i+1
    plt1.legend(fontsize=legend_fontsize,loc=(1.01,0.01))
    plt1.xaxis.label.set_size(axis_fontsize)
    plt1.yaxis.label.set_size(axis_fontsize)
    fig.suptitle("Cell Energy - Charge",x=0.2,y=0.9,fontweight='bold',fontsize=fig_title_size,verticalalignment='bottom')
    
    i=0
    fig,plt1=plt.subplots(1,1,figsize=(18, 10))
    for file in files:
        sheet=pd.read_excel(file)
        label=file[file.rfind('/')+1:-5]
        sheet.plot(ax=plt1,color=color_palette[i],x='Cycle',y='discharge_energy(Wh)',kind='scatter',label=label,xlabel='Cycle',ylabel='Energy(Wh)')
        i=i+1
    plt1.legend(fontsize=legend_fontsize,loc=(1.01,0.01))
    plt1.xaxis.label.set_size(axis_fontsize)
    plt1.yaxis.label.set_size(axis_fontsize)
    fig.suptitle("Cell Energy - Discharge",x=0.2,y=0.9,fontweight='bold',fontsize=fig_title_size,verticalalignment='bottom')
    
    i=0
    fig,plt1=plt.subplots(1,1,figsize=(18, 10))
    for file in files:
        sheet=pd.read_excel(file)
        label=file[file.rfind('/')+1:-5]
        sheet.plot(ax=plt1,color=color_palette[i],x='Cycle',y='energy_efficiency',kind='scatter',label=label,xlabel='Cycle',ylabel='Energy Efficiency')
        i=i+1
    plt1.legend(fontsize=legend_fontsize,loc=(1.01,0.01))
    plt1.xaxis.label.set_size(axis_fontsize)
    plt1.yaxis.label.set_size(axis_fontsize)
    fig.suptitle("Energy Efficiency",x=0.2,y=0.9,fontweight='bold',fontsize=fig_title_size,verticalalignment='bottom')
    
    i=0
    fig,plt1=plt.subplots(1,1,figsize=(18, 10))
    for file in files:
        sheet=pd.read_excel(file)
        label=file[file.rfind('/')+1:-5]
        sheet.plot(ax=plt1,color=color_palette[i],x='Cycle',y='recovery_voltage(V)',kind='scatter',label=label,xlabel='Cycle',ylabel='OCV')
        i=i+1
    plt1.legend(fontsize=legend_fontsize,loc=(1.01,0.01))
    plt1.xaxis.label.set_size(axis_fontsize)
    plt1.yaxis.label.set_size(axis_fontsize)
    fig.suptitle("End of Cycle OCV",x=0.2,y=0.9,fontweight='bold',fontsize=fig_title_size,verticalalignment='bottom')
    
def compare_capacity_degradation():
    path='/Cell Summaries'
    path = os.getcwd()+path
    files = glob.glob(path + "/*.xlsx")
    i=0
    fig = go.Figure()
    for file in files:
        sheet=pd.read_excel(file)
        label=file[file.rfind('/')+1:-5]
        sheet['degradation']=100*(sheet['discharge_capacity(Ah)']/sheet['discharge_capacity(Ah)'].cummax()-1)
        fig.add_trace(go.Scatter(x=sheet['Cycle'],y=sheet['degradation'],marker={'color':plotly_color_palette[i]},name=label))
        i=i+1
    fig.update_layout(
    title="Cell Capacity Degradation",
    xaxis_title="Cycle",
    yaxis_title="Degradation(%)",
    legend_title="Cells",
    width=1200,
    height=600,
    font=dict(
        #family="Courier New, monospace",
        #size=18,
        #color="RebeccaPurple"
    )
)
    fig.show()
    
def compare_energy_degradation():
    path='/Cell Summaries'
    path = os.getcwd()+path
    files = glob.glob(path + "/*.xlsx")
    i=0
    fig = go.Figure()
    for file in files:
        sheet=pd.read_excel(file)
        label=file[file.rfind('/')+1:-5]
        sheet['degradation']=100*(sheet['discharge_energy(Wh)']/sheet['discharge_energy(Wh)'].cummax()-1)
        fig.add_trace(go.Scatter(x=sheet['Cycle'],y=sheet['degradation'],marker={'color':plotly_color_palette[i]},name=label))
        i=i+1
    fig.update_layout(
    title="Cell Energy Degradation",
    xaxis_title="Cycle",
    yaxis_title="Degradation(%)",
    legend_title="Cells",
    width=1200,
    height=600,
    font=dict(
        #family="Courier New, monospace",
        #size=18,
        #color="RebeccaPurple"
    )
)
    fig.show()
    
