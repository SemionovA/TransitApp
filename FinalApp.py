# -*- coding: utf-8 -*-
"""
Created on Sun Mar 13 17:41:35 2022

@author: Arthur
"""

import pandas as pd
import numpy as np
import streamlit as st
import folium
from streamlit_folium import folium_static #using folium on streamlit
import altair as alt
from vega_datasets import data
import matplotlib.pyplot as plt
from PIL import Image
import pydeck as pdk



st.set_page_config(page_title = 'CET 522 App', page_icon="random", layout="wide") #, layout="wide"

st.title("Impacts of COVID-19 on U.S. Transit Finance")

page_names = ['Home', 'Data', 'Summary', 'Map', 'Time Series', 'Pie Chart']

page = st.radio('Navigation', page_names, index = 0)



if page == 'Home':
    st.header('Welcome! Here is how to go through our app')
    st.subheader('Select above which interactive page you would like to visit. Then select each function that you want per feature')   
    st.text('COVID-19 had many impacts on different industries and communities in the United States, during the pandemic travel decreased a great amount\n\
and especially transit since it is a shared use space. This study will focus on transit to better understand the effects COVID-19\n\
had on travel patterns and to investigate this, the finances will be evaluated. By evaluating the transit finances and how the\n\
finances can affect travel patterns before and “after” the pandemic, the hope is to understand how finances directly impact\n\
ridership due to COVID-19. Additionally, possible solutions can evolve from the study after the impact of finances and COVID-19\n \
is better understood regarding the transit agencies. By using the NTD Data, we will be able to visualize how the finances were impacted.')

    image = Image.open('transit.png')
    st.image(image, caption='Transit')
    
elif page == 'Data':
    st.header('Summary of Data and Management Plan')
    st.text('The main data source that was used was the NTD, National Transit Database, the information in this database will be used regarding\n\
 finances and ridership. Below is a list of the data tables that were used for analysis:\n\
    - Time Series of Monthly Ridership\n\
    - Time Series of Operating and Capital Funding Sources(Local, State, Federal, Total, Other)\n\
    - Time Series of Operating and Capital Expenditures\n\
The year 2020 will be claimed as the start of the pandemic, all other years before 2020 are pre-pandemic. Another note is that since 2021 was\n\
still during the pandemic, it is still considered a COVID year. Additionally, since there is no data for 2021 or 2022 yet, analysis of just pre-COVID\n\
and during COVID will be made with some predictions and analysis for post-COVID. With this data, analysis of how finances affected ridership before COVID\n\
and during COVID will be understood.')
    image = Image.open('ntd.png')
    st.image(image, caption='National Transit Database')

    
elif page == 'Summary':
    st.header('Brief Summary of Project and Results')  
    st.text('By inspecting the map, the different visualizations offered in the Time Series and Pie Chart tab, we are able to better understand how funds\n\
are sourced and spent as well as how ridership is affected by expenses. We found that there was a rapid decrease in ridership in the year 2020.\n\
A similar pattern for all agencies is also the increase of operating expenses until 2019, and its decrease after 2019. On the other hand,\n\
the capital expenses for the three agencies vary throughout the years, with LACMTA having an overall increasing trend and KCM having a rapid decrease\n\
after 2019. Even though the ridership is steady or decreasing for all examples the federal, state, and local funding are increasing or steady even after\n\
the COVID-19 outbreak, with the exception of the local funding for KCM that decreases significantly after 2015.\n\n\n *All results can be found in the report\
 with the according visuals.*')
 
    image = Image.open('finaltable.png')
    st.image(image, caption='Avg. expenditures and funding across studied agencies, per rider (2019-2020)')

elif page == 'Map': 
    st.header('Map of Agencies by Funding, Expense, or Ridership')
    st.subheader('Instructions on how to Navigate:')
    st.text('First choose which year you would like to look at and choose the type of data')
    capex = pd.read_csv('capex.csv')
    capex_pax = pd.read_csv('capex_pax.csv')

    # Make an empty map
    m = folium.Map(location=[40, -95], tiles="OpenStreetMap", zoom_start=4)

    #year choice input
    year_choice = ['2005','2006','2007','2008','2009','2010','2011','2012','2013','2014','2015','2016','2017',
                   '2018','2019','2020']

    #data choice input
    data_choice = ['Ridership','CAPEX','OPEX','Fare revenue','Federal funding','State funding','Local funding','Operational funding']

    #sidebar
    with st.sidebar:
        year_select = st.selectbox('Select year', year_choice, key=1)
        data_select = st.selectbox('Select data', data_choice, key=2)
        
        #can't normalize ridership; disable below checkbox if ridership is selected
        if data_select == 'Ridership':
            p = True
        else:
            p = False
        
        pax_select = st.checkbox('Normalize by ridership?', value=False, disabled = p)

    #Conditional inputs
    if data_select == 'Ridership':
            table_input = pd.read_csv('pax.csv')

    elif data_select == 'CAPEX':
        if pax_select == False:
            table_input = pd.read_csv('capex.csv')
        else:
            table_input = pd.read_csv('capex_pax.csv')
            
    elif data_select == 'OPEX':
        if pax_select == False:
            table_input = pd.read_csv('opex.csv')
        else:
            table_input = pd.read_csv('opex_pax.csv')
            
    elif data_select == 'Fare revenue':
        if pax_select == False:
            table_input = pd.read_csv('fares.csv')
        else:
            table_input = pd.read_csv('fares_pax.csv')

    elif data_select == 'Federal funding':
        if pax_select == False:
            table_input = pd.read_csv('fedfund.csv')
        else:
            table_input = pd.read_csv('fedfund_pax.csv')

    elif data_select == 'Federal funding':
        if pax_select == False:
            table_input = pd.read_csv('fedfund.csv')
        else:
            table_input = pd.read_csv('fedfund_pax.csv')
            
    elif data_select == 'State funding':
        if pax_select == False:
            table_input = pd.read_csv('statefund.csv')
        else:
            table_input = pd.read_csv('statefund_pax.csv')

    elif data_select == 'Local funding':
        if pax_select == False:
            table_input = pd.read_csv('localfund.csv')
        else:
            table_input = pd.read_csv('localfund_pax.csv')
            
    elif data_select == 'Operational funding':
        if pax_select == False:
            table_input = pd.read_csv('opfund.csv')
        else:
            table_input = pd.read_csv('opfund_pax.csv')      


    # add marker one by one on the map
    for i in range(0,len(table_input)):
        
        #Pax is selected
        if pax_select == True: 
            label = '<strong>{name}</strong>: ${data}'.format(
                name=table_input.iloc[i]['Agency Name'], data=round(table_input.iloc[i][year_select],2).astype(str)) #popup label
            size_factor = 5000 #adjust for bubble size
        
        #Ridership is selected
        elif data_select == 'Ridership':
            t = table_input[year_select].astype(int).apply(lambda x : "{:,}".format(x)) #thousand seperators, output string
            label = '<strong>{name}</strong>: {data}'.format(
                name=table_input.iloc[i]['Agency Name'], data=t.iloc[i]) #popup label
            size_factor = 0.0005 #adjust for bubble size
       
        else: 
            t = table_input[year_select].astype(int).apply(lambda x : "{:,}".format(x)) #thousand seperators, output string
            label = '<strong>{name}</strong>: ${data}'.format(
                name=table_input.iloc[i]['Agency Name'], data=t.iloc[i]) #popup label
            size_factor = 0.0005 #adjust for bubble size
        
        folium.Circle(
            location=[table_input.iloc[i]['lat'], table_input.iloc[i]['lon']],
            popup=label,
            radius=table_input.iloc[i][year_select]*size_factor,
            color='crimson',
            fill=True,
        ).add_to(m)

    # Show the map 
    folium_static(m,width=1280,height=720)
    
elif page == 'Time Series':
    st.header('Time Series of Funding, Expense, or Ridership by Agency')
    st.subheader('Instructions on how to Navigate:')
    st.text('First choose the type of data and then pick the agencies to graph')
    capex = pd.read_csv('capex.csv')
    capex_pax = pd.read_csv('capex_pax.csv')
    
   #agency choice input
    agency_choice = ['MTA New York City Transit (NYCT)',
                   'New Jersey Transit Corporation',
                   'Massachusetts Bay Transportation Authority (MBTA)',
                   'Los Angeles County Metropolitan Transportation Authority (LACMTA)',
                   'Chicago Transit Authority (CTA)',
                   'Washington Metropolitan Area Transit Authority (WMATA)',
                   'Central Puget Sound Regional Transit Authority (ST)',
                   'King County Department of Metro Transit (KCM)',
                   'Metro-North Commuter Railroad Company, dba: MTA Metro-North Railroad (MTA-MNCR)',
                   'City and County of San Francisco (SFMTA)',
                   'Dallas Area Rapid Transit (DART)',
                   'Denver Regional Transportation District (RTD)',
                   'Northeast Illinois Regional Commuter Railroad Corporation',
                   'Metropolitan Transit Authority of Harris County, Texas' ,
                   'San Francisco Bay Area Rapid Transit District (BART)',
                   'Southeastern Pennsylvania Transportation Authority (SEPTA)',
                   'Tri-County Metropolitan Transportation District of Oregon',
                   'County of Miami-Dade (MDT)',
                   'Maryland Transit Administration (MTA)',
                   'Metropolitan Atlanta Rapid Transit Authority (MARTA)',
                   'Peninsula Corridor Joint Powers Board (PCJPB)',
                   'San Diego Metropolitan Transit System (MTS)',
                   'Utah Transit Authority (UTA)',
                   'Valley Metro Rail, Inc. (VMR)',
                   'Santa Clara Valley Transportation Authority (VTA)',
                   'The Greater Cleveland Regional Transit Authority (GCRTA)',
                   'VIA Metropolitan Transit (VIA)',
                   'Capital Metropolitan Transportation Authority (CMTA)',
                   'Staten Island Rapid Transit Operating Authority (SIRTOA)',
                   'Port Authority of Allegheny County',
                   'Greater Dayton Regional Transit Authority (GDRTA)',
                   'Pace - Suburban Bus Division',
                   'Northern Indiana Commuter Transportation District (NICTD)',
                   'Central Ohio Transit Authority (COTA)',
                   'Connecticut Department of Transportation - CTTRANSIT - Hartford Division',
                   'Central Florida Regional Transportation Authority (LYNX)',
                   'City of Charlotte North Carolina (CATS)',
                   'Washington State Ferries (WSF)',
                   'Golden Gate Bridge, Highway and Transportation District (GGBHTD)',
                   'Fort Worth Transportation Authority (FWTA)',
                   'Bi-State Development Agency of the Missouri-Illinois Metropolitan District (BSD)',
                   'New Orleans Regional Transit Authority (NORTA)',
                   'Broward County Board of County Commissioners (BCT)',
                   'Indianapolis and Marion County Public Transportation (IndyGo)',
                   'Rhode Island Public Transit Authority (RIPTA)']

   #data choice input
    data_choice = ['Ridership','CAPEX','OPEX','Fare revenue','Federal funding','State funding','Local funding','Operational funding']


   #sidebar
    with st.sidebar:
       #agency_select = st.selectbox('Select agency', agency_choice, key=1)
       data_select = st.selectbox('Select data', data_choice, key=2)
       
       #can't normalize ridership; disable below checkbox if ridership is selected
       if data_select == 'Ridership':
           p = True
       else:
           p = False
       
       pax_select = st.checkbox('Normalize by ridership?', value=False, disabled = p)
       
   #Conditional inputs
    if data_select == 'Ridership':
           table_input = pd.read_csv('pax.csv')

    elif data_select == 'CAPEX':
       if pax_select == False:
           table_input = pd.read_csv('capex.csv')
       else:
           table_input = pd.read_csv('capex_pax.csv')
           
    elif data_select == 'OPEX':
       if pax_select == False:
           table_input = pd.read_csv('opex.csv')
       else:
           table_input = pd.read_csv('opex_pax.csv')
           
    elif data_select == 'Fare revenue':
       if pax_select == False:
           table_input = pd.read_csv('fares.csv')
       else:
           table_input = pd.read_csv('fares_pax.csv')

    elif data_select == 'Federal funding':
       if pax_select == False:
           table_input = pd.read_csv('fedfund.csv')
       else:
           table_input = pd.read_csv('fedfund_pax.csv')

    elif data_select == 'Federal funding':
       if pax_select == False:
           table_input = pd.read_csv('fedfund.csv')
       else:
           table_input = pd.read_csv('fedfund_pax.csv')
           
    elif data_select == 'State funding':
       if pax_select == False:
           table_input = pd.read_csv('statefund.csv')
       else:
           table_input = pd.read_csv('statefund_pax.csv')

    elif data_select == 'Local funding':
       if pax_select == False:
           table_input = pd.read_csv('localfund.csv')
       else:
           table_input = pd.read_csv('localfund_pax.csv')
           
    elif data_select == 'Operational funding':
       if pax_select == False:
           table_input = pd.read_csv('opfund.csv')
       else:
           table_input = pd.read_csv('opfund_pax.csv')      

    option_list = []
    with st.sidebar:
       for ii in agency_choice:
           option_list.append(st.checkbox(ii))

    choice = [i for i, x in enumerate(option_list) if x]

    agency_select = list(map(agency_choice.__getitem__, choice))

    if pax_select == False:
       table_input = table_input.drop(['State'], axis=1)

    if len(agency_select):
       table_input = table_input.drop([table_input.columns[0],'City_x','place_id','City_y','state_id','lat','lon'],axis=1)
       temp_df = table_input[table_input['Agency Name'].isin(agency_select)].iloc[:, 1:].transpose().reset_index()
       temp_df.columns = ['Date'] + agency_select
       
       fontsize_label = 14
       fortsize_title = 16
       fontsize_ticks = 10
       
       fig, ax = plt.subplots()

       temp_df.plot(x='Date', y=agency_select, ax=ax)
       #ax.set_xticks(temp_df['Date'].astype(int).tolist())
       ax.set_xticks(range(len(temp_df)));
       ax.set_xticklabels(temp_df.Date.tolist(), rotation=45);
       
       ax.set_title(f'{data_select} Timeseries', fontsize = fortsize_title)
       ax.set_xlabel('Date', fontsize=fontsize_label)
       ax.set_ylabel(data_select, fontsize=fontsize_label)
       ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.20))
       ax.grid(True)
       
       
       st.pyplot(fig)
       
else:  
    st.header('Pie Chart for Funding, Expense, or Ridership by Agency')
    st.subheader('Instructions: First choose the type of data, then pick the agencies to graph and for what year')
    
    
    # > Data input
    data_choice = ['Funding', 'Expenditure']
    agency_choice = ['MTA New York City Transit (NYCT)',
                    'New Jersey Transit Corporation',
                    'Massachusetts Bay Transportation Authority (MBTA)',
                    'Los Angeles County Metropolitan Transportation Authority (LACMTA)',
                    'Chicago Transit Authority (CTA)',
                    'Washington Metropolitan Area Transit Authority (WMATA)',
                    'Central Puget Sound Regional Transit Authority (ST)',
                    'King County Department of Metro Transit (KCM)',
                    'Metro-North Commuter Railroad Company, dba: MTA Metro-North Railroad (MTA-MNCR)',
                    'City and County of San Francisco (SFMTA)',
                    'Dallas Area Rapid Transit (DART)',
                    'Denver Regional Transportation District (RTD)',
                    'Northeast Illinois Regional Commuter Railroad Corporation',
                    'Metropolitan Transit Authority of Harris County, Texas' ,
                    'San Francisco Bay Area Rapid Transit District (BART)',
                    'Southeastern Pennsylvania Transportation Authority (SEPTA)',
                    'Tri-County Metropolitan Transportation District of Oregon',
                    'County of Miami-Dade (MDT)',
                    'Maryland Transit Administration (MTA)',
                    'Metropolitan Atlanta Rapid Transit Authority (MARTA)',
                    'Peninsula Corridor Joint Powers Board (PCJPB)',
                    'San Diego Metropolitan Transit System (MTS)',
                    'Utah Transit Authority (UTA)',
                    'Valley Metro Rail, Inc. (VMR)',
                    'Santa Clara Valley Transportation Authority (VTA)',
                    'The Greater Cleveland Regional Transit Authority (GCRTA)',
                    'VIA Metropolitan Transit (VIA)',
                    'Capital Metropolitan Transportation Authority (CMTA)',
                    'Staten Island Rapid Transit Operating Authority (SIRTOA)',
                    'Port Authority of Allegheny County',
                    'Greater Dayton Regional Transit Authority (GDRTA)',
                    'Pace - Suburban Bus Division',
                    'Northern Indiana Commuter Transportation District (NICTD)',
                    'Central Ohio Transit Authority (COTA)',
                    'Connecticut Department of Transportation - CTTRANSIT - Hartford Division',
                    'Central Florida Regional Transportation Authority (LYNX)',
                    'City of Charlotte North Carolina (CATS)',
                    'Washington State Ferries (WSF)',
                    'Golden Gate Bridge, Highway and Transportation District (GGBHTD)',
                    'Fort Worth Transportation Authority (FWTA)',
                    'Bi-State Development Agency of the Missouri-Illinois Metropolitan District (BSD)',
                    'New Orleans Regional Transit Authority (NORTA)',
                    'Broward County Board of County Commissioners (BCT)',
                    'Indianapolis and Marion County Public Transportation (IndyGo)',
                    'Rhode Island Public Transit Authority (RIPTA)']
    year_choice = ['2005','2006','2007','2008','2009','2010','2011','2012','2013','2014','2015','2016','2017','2018','2019','2020']
        #Not normalizing by ridership b/c not comparing to other agencies, not meaningful

    # > Create sidebar
    with st.sidebar:
        data_select = st.selectbox('Funding or Expenditure', data_choice, key=1)
        agency_select = st.selectbox('Select Agency', agency_choice, key=2)
        year_select = st.selectbox('Select Year', year_choice, key=3)

    # > Conditional inputs
        # >> Create tables with funding data
    if data_select == 'Funding':
        fed = pd.read_csv('fedfund.csv', index_col = 'Agency Name')
        state = pd.read_csv('statefund.csv', index_col = 'Agency Name')
        local = pd.read_csv('localfund.csv', index_col = 'Agency Name')
        op = pd.read_csv('opfund.csv', index_col = 'Agency Name')
        fares = pd.read_csv('fares.csv', index_col = 'Agency Name')
        # >> Create tables with expenditure data
    elif data_select == 'Expenditure':
        capex = pd.read_csv('capex.csv', index_col = 'Agency Name')
        opex = pd.read_csv('opex.csv', index_col = 'Agency Name')

    # > Data Generation
        # >> Extract funding values for given year, agency
    if data_select == 'Funding':
        fed_select0 = fed.at[agency_select, year_select]
        state_select0 = state.at[agency_select, year_select]
        local_select0 = local.at[agency_select, year_select]
        op_select0 = op.at[agency_select, year_select]
        fares_select0 = fares.at[agency_select, year_select]
        dollar_amounts0 = [fed_select0, state_select0, local_select0, op_select0, fares_select0]
        categories = [f'Federal Funding - ${fed_select0}', f'State Funding - ${state_select0}', f'Local Funding - ${local_select0}', f'Other Operational Funding - ${op_select0}', f'Fare Revenue - ${fares_select0}']
        # >> Extract expenditure values for given year, agency
    elif data_select == 'Expenditure':
        capex_select0 = capex.at[agency_select, year_select]
        opex_select0 = opex.at[agency_select, year_select]
        dollar_amounts0 = [capex_select0, opex_select0]
        categories = [f'Capital Expenditure - ${capex_select0}', f'Operating Expenditure - ${opex_select0}']

    # Pie Chart Generation
    fig, ax = plt.subplots()
    ax.pie(dollar_amounts0, labels=categories, autopct='%1.1f%%',
            shadow=True, startangle=90)
    ax.axis('equal')
    ax.set_title(f'{agency_select} {year_select} {data_select} Breakdown', fontsize = 14)

    st.pyplot(fig)
