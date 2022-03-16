# > Import Libraries
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# > ------RUN STEAMLIT AND VIZ CODE HERE------- #
st.set_page_config(page_title="Funding and Expenditure Breakdown by Agency - Pie Chart")

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