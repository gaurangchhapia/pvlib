#!/usr/bin/env python
# coding: utf-8

# In[6]:


get_ipython().system('pip install chart_studio')
get_ipython().system('pip install cufflinks')
get_ipython().system('pip install -U kaleido')
get_ipython().system('pip install pvlib')


# In[7]:


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


# In[8]:


studi_global=pd.read_csv('studienkolleg_global.csv',skiprows=8,nrows=8784,
                     index_col=0)


# In[9]:


studi_components=pd.read_csv('studienkolleg_components.csv',skiprows=8,nrows=8784,
                     index_col=0)


# In[10]:


poa_studi=pd.DataFrame(columns=['poa_global','poa_direct','poa_diffuse','temp_air','wind_speed'],
                       index=studi_global.index)


# In[11]:


poa_studi['poa_global']=studi_global['G(i)']
poa_studi['poa_direct']=studi_components['Gb(i)']
poa_studi['poa_diffuse']=studi_components['Gd(i)']+studi_components['Gr(i)']
poa_studi['temp_air']=studi_components['T2m']
poa_studi['wind_speed']=studi_components['WS10m']


# In[12]:


poa_studi.index=pd.to_datetime(poa_studi.index,format='%Y%m%d:%H%M')


# In[13]:


location=Location(latitude=51.4984,
                  longitude=10.7931,
                  tz='Europe/Berlin',
                  altitude=202,
                  name='Studienkolleg')


# In[14]:


cec=pvlib.pvsystem.retrieve_sam('CECmod')
cec_inverters=pvlib.pvsystem.retrieve_sam('CECInverter')


# In[15]:


module=cec['Hanwha_Q_CELLS_Q_PEAK_L_G4_2_370']
inverter=cec_inverters['SMA_America__ST36__277V_']
temperature_parameters=TEMPERATURE_MODEL_PARAMETERS['sapm']['open_rack_glass_glass']


# In[16]:


cec['Hanwha_Q_CELLS_Q_PEAK_L_G4_2_370']


# In[17]:


cec_inverters['ABB__TRIO_27_6_TL_OUTD_S1A_US_480_A__480V_']


# In[18]:


cec_inverters['SMA_America__ST36__208V_']


# In[19]:


cec_inverters['Advanced_Energy_Industries__AE_3TL_16_10_08__480V_']


# In[20]:


cec_inverters['ABB__TRIO_20_0_TL_OUTD_S1A_US_480_A__480V_']


# In[21]:


cec_inverters['Advanced_Energy_Industries__AE_35TX_208__208V_']


# In[22]:


system=PVSystem(surface_tilt=30,surface_azimuth=191,
                module_parameters=module,
                inverter_parameters=inverter,
                temperature_model_parameters=temperature_parameters,
                modules_per_string=13,strings_per_inverter=8)


# In[ ]:





# In[23]:


modelchain=ModelChain(system,location,aoi_model="physical",spectral_model="no_loss")
modelchain


# In[24]:


clear


# In[25]:


clear


# In[26]:


modelchain.run_model_from_poa(poa_studi)
modelchain.results.ac.resample('M').sum().plot(kind='bar',figsize=(16,9))


# In[ ]:





# In[21]:


a=modelchain.results.ac.resample('M').sum()


# In[22]:


en=pd.DataFrame({'inverter1':a
                 })


# In[23]:


clear


# In[24]:


clear


# In[25]:


en['inverter1'].sum()


# In[26]:


en.plot(kind='bar')


# In[27]:


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


# In[28]:


en['Months']=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']


# In[29]:


en['inverter1'].sum()


# In[30]:


trace1=go.Bar(
        x=en['Months'],
        y=en['inverter1'],
        text=en['inverter1'],
        #textposition='auto',
        name='Energy distribution across the year',
        marker_color=hsn_bluebl)


# In[31]:


data = [trace1]
fig = go.Figure(data = data)
fig.update_traces(texttemplate='%{text:.4s}',textposition='inside', opacity=1,
                  textfont=dict(family=A,size=18,color='white'))
fig.update_layout(uniformtext_minsize=20)
#fig.update_layout(xaxis_tickangle=45)
fig.update_layout(title='Energy yield of Studienkolleg',
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
pio.write_image(fig, 'energy_yield_of_Studienkolleg.png',scale=6, width=1080, height=650)


# In[ ]:





# In[ ]:




