import pandas as pd
import streamlit as st
import SW_API
import matplotlib.pyplot as plt


### Sidebar work below ###
    
st.sidebar.header('Model Inputs')

user_perm = st.sidebar.selectbox('Do you have a Similar Web API Key ?',\
                                 ('No. I would like to use the free version please.',\
                                  'Yes. I would be happy to provide the key below.'))

if user_perm[:3] == 'Yes':
    apiKey = st.sidebar.text_input('API KEY - ', '')
    if apiKey != '':
        perm_res = SW_API.user_cap(apiKey)
        if isinstance(perm_res, str):
            st.sidebar.error(perm_res)
        else:
            st.sidebar.dataframe(perm_res)
            

st.sidebar.subheader('Comparetive Analysis : ')

comp_csv = st.sidebar.text_area('Please enter websites of companies you want a comparetive analysis \
for - (comma seperated complete URLs please)',"https://www.google.com/,https://reddit.com/,\
https://www.zillow.com/,https://freetrade.io/,https://www.amazon.com/")

comp_input = comp_csv.strip().split(',')
comp_web = [SW_API.swGet(c) for c in comp_input]
comp_stat = ['Good' if r.status_code == 200 else 'Error Code : %s'%r.status_code for r in comp_web]
comp_web_final = [r.json() for r in comp_web if r.status_code == 200]
comp_df = pd.DataFrame(zip(comp_input,comp_stat),columns=['URL','Status'])

expander = st.sidebar.expander("See all inputs and corresponding status")
with expander:
    st.sidebar.dataframe(comp_df)

    

"""
# Data Sourcing Tool - Similar Web API
Welcome to the Similar Web API Sourcing tool. This page is intended to extract information from the Similar Web API to pull down company websites that could make interesting investment targets. The way to surface promising companies as potential investment targets would be to do a comparative analysis based on similar companies. Given the [SW API](https://docs.api.similarweb.com/) is designed to extract information specific to a domain, this tool is designed to pull information from individual domain names. You have the option to use the free data from the SW API or enter your API key to show the current capabilities. Future versions of this tool would scale depending on the license and user capabilities.

Please enter the api key information and a collection of company domain names on your left. The company websites have to be comma separated and would be used to compare the growth in estimated monthly visits for the last 6 months. We will also do a comparative analysis on the web engagements. As a use case we can dump multiple private and public company information in the text area on the left and based on the monthly visit growth we can surface investment opportunities. 

The tool below is designed to study a company and its performance through its website analytics. You can enter the domain name below and it will show the title, description and category for the company. Next it will show the traffic shares for the top 5 countries. This will be followed by the website ranking for the company - Global Rank, Country Rank and Category Rank. We also represent the source of the traffic through a pie chart.

For comparative analysis we will show the engagement metrics for the company along with the ones listed on the left pane. This will be followed by a graph showing the growth in monthly visits for the past six months for the domains listed. This should make the tool well rounded as a data sourcing tool. 

If you have any questions about the tool, reach out to me at <vishal.tripathi@berkeley.edu> or through [LinkedIn](https://www.linkedin.com/in/vtripathi30/). Alternatively see the source code on github through the dropdown on the right. 
Below is the data sourcing tool:

"""

domain = st.text_input('Please enter the domain name of the company you want to review','https://www.m1.com/')

resp = SW_API.swGet(domain)



if resp.status_code != 200:
    resp.raise_for_status()
    st.error('Error Code : %s'%resp.status_code)

if resp.status_code == 200:
    result = resp.json()
    st.markdown(
        f"""
        * Site Name : {result.get('SiteName','None')}
        * Title : {result.get('Title','None')}
        * Description : {result.get('Description','None')}
        * Category : {result.get('Category','None')}
    """
    )
    
    conDf = pd.DataFrame(result.get('TopCountryShares',[]))
    if not conDf.empty:
        conDf['Country'] = conDf.apply(lambda row: SW_API.get_country(row['Country']), axis = 1)
        conDf['Traffic Shares'] = conDf.apply(lambda row: str(row['Value']*100)[:5]+"%", axis = 1)
        country_df = conDf[['Country','Traffic Shares']]
        st.dataframe(country_df)
    
    st.markdown(
        f"""
        * Global Rank : {result.get('GlobalRank',{}).get('Rank','None')}
        * Top Country Rank : {result.get('CountryRank',{}).get('Rank','None')}
        * Category Rank : {result.get('CategoryRank',{}).get('Rank','None')}
    """
    )
    
    traf = result.get('TrafficSources',None)
    if traf:
        fig1, ax1 = plt.subplots()
        ax1.pie(traf.values(), autopct='%1.1f%%', radius = 3,
                shadow=True, startangle=90, pctdistance = 1.2)
        ax1.legend(traf.keys(), bbox_to_anchor=(0.9, 0.9))
        ax1.axis('equal')
        st.pyplot(fig1)
        
    comp_web_final.append(result)
        
    
st.subheader('Comparetive Analysis - ')

if comp_web_final:
    
    month = comp_web_final[-1].get('Engagments',{}).get('Month','None')
    year = comp_web_final[-1].get('Engagments',{}).get('Year','None')
    
    st.text('Below you can see the comparetive analysis for the engagement on the website\
    for the companies. This data is as of Year %s and Month %s'%(month, year))
    
    comp_engmt = [r['Engagments'] for r in comp_web_final if 'Engagments' in r.keys()]
    comp_names = [r['SiteName'] for r in comp_web_final if 'SiteName' in r.keys()]
    engmt_df = pd.DataFrame(comp_engmt, index = comp_names)
    engmt_df['Total Visits'] = engmt_df['Visits'].astype(float).astype(int)
    engmt_df['Pages per Visit'] = engmt_df['PagePerVisit'].astype(float).astype(int)
    engmt_df['Avg Visit Duration (seconds)'] = engmt_df['TimeOnSite'].astype(float).astype(int)
    engmt_df['Bounce Rate'] = engmt_df.apply(lambda row: str(float(row['BounceRate'])*100)[:5]+"%", axis = 1)
    engmt_df = engmt_df[['Total Visits','Pages per Visit','Avg Visit Duration (seconds)','Bounce Rate']]
    st.dataframe(engmt_df)
    
    
        
        
        
        
        
        
        
        
        
        
        
        
        
        
    
    