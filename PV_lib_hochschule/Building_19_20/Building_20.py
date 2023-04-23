#!/usr/bin/env python
# coding: utf-8

# In[1]:


get_ipython().system('pip install chart_studio')
get_ipython().system('pip install cufflinks')
get_ipython().system('pip install -U kaleido')
get_ipython().system('pip install pvlib')


# In[2]:


import pvlib
from pvlib.modelchain import ModelChain
from pvlib.location import Location
from pvlib.pvsystem import PVSystem
from pvlib.temperature import TEMPERATURE_MODEL_PARAMETERS
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.io as pio
get_ipython().run_line_magic('matplotlib', 'inline')


# In[3]:


buil_20_global=pd.read_csv('Building_20_global.csv',skiprows=8,nrows=8784,
                     index_col=0)


# In[4]:


buil_20_components=pd.read_csv('Building_20_components.csv',skiprows=8,nrows=8784,
                     index_col=0)


# In[5]:


poa_buil_20=pd.DataFrame(columns=['poa_global','poa_direct','poa_diffuse','temp_air','wind_speed'],
                       index=buil_19_global.index)


# In[ ]:


poa_buil_20['poa_global']=buil_20_global['G(i)']
poa_buil_20['poa_direct']=buil_20_components['Gb(i)']
poa_buil_20['poa_diffuse']=buil_20_components['Gd(i)']+buil_20_components['Gr(i)']
poa_buil_20['temp_air']=buil_20_components['T2m']
poa_buil_20['wind_speed']=buil_20_components['WS10m']


# In[ ]:


poa_buil_20.index=pd.to_datetime(poa_buil_20.index,format='%Y%m%d:%H%M')


# In[ ]:


location=Location(latitude=51.4984,
                  longitude=10.7931,
                  tz='Europe/Berlin',
                  altitude=202,
                  name='Building 19')


# In[ ]:


cec=pvlib.pvsystem.retrieve_sam('CECmod')
cec_inverters=pvlib.pvsystem.retrieve_sam('CECInverter')


# In[ ]:


module=cec['Hanwha_Q_CELLS_Q_PEAK_L_G4_2_370']
inverter=cec_inverters['Advanced_Energy_Industries__AE_35TX_208__208V_']
temperature_parameters=TEMPERATURE_MODEL_PARAMETERS['sapm']['open_rack_glass_glass']


# In[ ]:


cec['Hanwha_Q_CELLS_Q_PEAK_L_G4_2_370']


# In[ ]:


cec_inverters['Advanced_Energy_Industries__AE_35TX_208__208V_']


# In[ ]:


system=PVSystem(surface_tilt=30,surface_azimuth=193,
                module_parameters=module,
                inverter_parameters=inverter,
                temperature_model_parameters=temperature_parameters,
                modules_per_string=10,strings_per_inverter=9)


# In[ ]:


modelchain=ModelChain(system,location,aoi_model="physical",spectral_model="no_loss")
modelchain


# In[ ]:


modelchain.run_model_from_poa(poa_buil_20)
modelchain.results.ac.plot(figsize=(16,9))


# In[ ]:


a=modelchain.results.ac.resample('M').sum()


# In[ ]:


en=pd.DataFrame({'inverter1':a
                 })


# In[ ]:


en['inverter1'].sum()


# In[ ]:


T='Times New Roman'
A='Arial'
hsn_blue='rgb(0,89,158)'
hsn_bluem='rgb(15,147,250)'
hsn_blueb='rgb(45,158,247)'
hsn_blueg='rgb(53,107,150)'
hsn_bluebl='rgb(9,47,77)'
hsn_green='rgb(103,189,0)'
hsn_greenb='rgb(144,252,15)'
hsn_greeng='rgb(120,163,69)'
hsn_greenl='rgb(193,240,137)'
hsn_greenbl='rgb(43,74,7)'
hsn_grey = 'rgb(97,98,99)'
hsn_greym= 'rgb(210,210,212)'
hsn_greyl= 'rgb(227,228,230)'


# In[ ]:


en['Months']=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']


# In[ ]:


en['inverter1'].sum()


# In[ ]:


trace1=go.Bar(
        x=en['Months'],
        y=en['inverter1'],
        text=en['inverter1'],
        #textposition='auto',
        name='Energy distribution across the year',
        marker_color=hsn_bluebl)


# In[ ]:


data = [trace1]
fig = go.Figure(data = data)
fig.update_traces(texttemplate='%{text:.4s}',textposition='inside', opacity=1,
                  textfont=dict(family=A,size=18,color='white'))
fig.update_layout(uniformtext_minsize=20)
#fig.update_layout(xaxis_tickangle=45)
fig.update_layout(title='Energy yield of Building 20',
                  title_x=0.5,
                  yaxis_title='Energy in mega Watt hour',font=dict(size=18),
                 legend=dict(
    #itemwidth=30,
    orientation='h',
    yanchor="middle",
    y=-0.3,
    xanchor="center",
    x=0.5,
    title_font_family=A,
    font=dict(
    family=A,
    size=10,
    color=hsn_blue),
    bgcolor=hsn_greyl,
    bordercolor=hsn_blue,
    valign='bottom',
    tracegroupgap=10,
    borderwidth=1,),
    font_family=A,
    font_color=hsn_blue,
    title_font_family=A,
    title_font_color=hsn_blue,
    legend_tracegroupgap=500,
                    
)
fig.update_xaxes(title_font_family=A)
fig.update_layout(
xaxis=dict(
showline=True,showgrid=False,showticklabels=True,
linecolor=hsn_blue,
title_text="Month",
title_standoff = 10,
linewidth=3,ticks='outside',tickfont=dict(
family=A,size=15,color=hsn_blue))
,
yaxis=dict(
showline=True,showgrid=False,showticklabels=True,
linecolor=hsn_blue,
ticklabelposition="outside",
linewidth=2,ticks='outside',tickfont=dict(
family=A,size=15,color=hsn_blue)
),autosize=True,margin=dict(
autoexpand=True,l=50,r=50,b=100,t=100,pad=0),
showlegend=False,paper_bgcolor=hsn_greyl,
    plot_bgcolor=hsn_greym)
fig.show()
pio.write_image(fig, 'energy_yield_of_Building_20.png',scale=6, width=1080, height=650)


# In[ ]:




