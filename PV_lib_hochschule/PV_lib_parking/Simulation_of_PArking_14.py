#!/usr/bin/env python
# coding: utf-8

# In[1]:


get_ipython().system('pip install pvlib')


# In[2]:


import pvlib
from pvlib.modelchain import ModelChain
from pvlib.location import Location
from pvlib.pvsystem import PVSystem
from pvlib.temperature import TEMPERATURE_MODEL_PARAMETERS
import pandas as pd
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
import plotly.graph_objects as go
import plotly.io as pio


# In[3]:


global_14=pd.read_csv('parking_14_global.csv',skiprows=8,nrows=8784,
                      index_col=0)


# In[4]:


components_14=pd.read_csv('parking_45_components.csv',skiprows=8,nrows=8784,
                          index_col=0)


# In[5]:


poa_14=pd.DataFrame(columns=['poa_global','poa_direct','poa_diffuse','temp_air','wind_speed'],
                     index=global_14.index)


# In[6]:


poa_14['poa_global']=global_14['G(i)']
poa_14['poa_direct']=components_14['Gb(i)']
poa_14['poa_diffuse']=components_14['Gd(i)']+components_14['Gr(i)']
poa_14['temp_air']=components_14['T2m']
poa_14['wind_speed']=components_14['WS10m']


# In[7]:


poa_14.index=pd.to_datetime(poa_14.index,format='%Y%m%d:%H%M')


# In[8]:


poa_14


# In[9]:


location=Location(latitude=51.4984,
                  longitude=10.7931,
                  tz='Europe/Berlin',
                  altitude=210,
                  name='parking_14')


# In[10]:


cec=pvlib.pvsystem.retrieve_sam('CECmod')
cec_inverters=pvlib.pvsystem.retrieve_sam('CECInverter')


# In[ ]:





# In[11]:


module=cec['Hanwha_Q_CELLS_Q_PEAK_L_G4_2_370']
inverter=cec_inverters['SMA_America__SC125U__480V_']
temperature_parameters=TEMPERATURE_MODEL_PARAMETERS['sapm']['open_rack_glass_glass']


# In[12]:


cec_inverters['SMA_America__SC125U__480V_']


# In[13]:


cec['Hanwha_Q_CELLS_Q_PEAK_L_G4_2_370']


# In[ ]:





# In[14]:


system=PVSystem(surface_tilt=45,surface_azimuth=184,module_parameters=module,inverter_parameters=inverter,temperature_model_parameters=temperature_parameters,
                modules_per_string=7,strings_per_inverter=50)


# In[15]:


modelchain=ModelChain(system,location,aoi_model="physical",spectral_model="no_loss")


# In[16]:


modelchain.run_model_from_poa(poa_14)
modelchain.results.ac.resample('M').sum().plot(kind='bar',figsize=(16,9))


# In[17]:


global_14_30=pd.read_csv('parking_14_30_global.csv',skiprows=8,
                         nrows=8784,index_col=0)


# In[18]:


global_14_30


# In[19]:


components_14_30=pd.read_csv('parking_14_30_components.csv',skiprows=8,
                             nrows=8784,index_col=0)


# In[20]:


components_14_30


# In[21]:


poa_14_30=pd.DataFrame(columns=['poa_global','poa_direct','poa_diffuse','temp_air','wind_speed'],
                     index=global_14_30.index)


# In[ ]:





# In[22]:


poa_14_30['poa_global']=global_14_30['G(i)']
poa_14_30['poa_direct']=components_14_30['Gb(i)']
poa_14_30['poa_diffuse']=components_14_30['Gd(i)']+components_14_30['Gr(i)']
poa_14_30['temp_air']=components_14_30['T2m']
poa_14_30['wind_speed']=components_14_30['WS10m']


# In[23]:


poa_14_30


# In[24]:


poa_14_30.index=pd.to_datetime(poa_14_30.index,format='%Y%m%d:%H%M')


# In[25]:


poa_14_30


# In[26]:


system1=PVSystem(surface_tilt=30,surface_azimuth=184,module_parameters=module,inverter_parameters=inverter,temperature_model_parameters=temperature_parameters,
                modules_per_string=7,strings_per_inverter=50)


# In[27]:


modelchain1=ModelChain(system1,location,aoi_model="physical",spectral_model="no_loss")


# In[28]:


modelchain1.run_model_from_poa(poa_14)
modelchain1.results.ac.resample('M').sum().plot(kind='bar',figsize=(16,9))


# In[29]:


a=modelchain.results.ac.resample('M').sum()
b=modelchain1.results.ac.resample('M').sum()


# In[30]:


energy=pd.DataFrame({'tilt_45':a,
                     'tilt_30':b})


# In[31]:


energy.plot(kind='bar')


# In[32]:


energy_14_30=modelchain1.results.ac.resample('M').sum()


# In[33]:


a=pd.DataFrame({'en_14_30':energy_14_30})


# In[34]:


a.to_csv('energy_parking_14_30.csv')


# In[35]:


energy_14_45=modelchain.results.ac.resample('M').sum()


# In[36]:


b=pd.DataFrame({'en_14_45':energy_14_45})


# In[37]:


b.to_csv('energy_parking_14_45.csv')


# In[38]:


a['Months']=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']


# In[39]:


a


# In[40]:


a['en_14_30'].sum()


# In[41]:


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


# In[42]:


trace1=go.Bar(
        x=a['Months'],
        y=a['en_14_30'],
        text=a['en_14_30'],
        #textposition='auto',
        name='Energy distribution across the year',
        marker_color=hsn_bluebl)


# In[43]:


data = [trace1]
fig = go.Figure(data = data)
fig.update_traces(texttemplate='%{text:.4s}',textposition='inside', opacity=1,
                  textfont=dict(family=A,size=18,color='white'))
fig.update_layout(uniformtext_minsize=20)
#fig.update_layout(xaxis_tickangle=45)
fig.update_layout(title='Energy yield of parking roof top',
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
pio.write_image(fig, 'energy_yield_of_parking_roof_top_14.png',scale=6, width=1080, height=650)

