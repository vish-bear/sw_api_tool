from requests import get
from urllib.parse import urlparse
import pandas as pd
import ast
    
#AGENT = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:66.0) Gecko/20100101 Firefox/66.0", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate", "DNT": "1", "Connection": "close", "Upgrade-Insecure-Requests": "1"}

COUNTRY_CODES = pd.read_csv('wikipedia-iso-country-codes.csv')


def swGet(website, headers = AGENT):
    ''' Extract the data from the Similar Web API '''
    domain = '{uri.netloc}'.format(uri=urlparse(website))
    domain = domain.replace("www.", "")
    ENDPOINT = 'https://data.similarweb.com/api/v1/data?domain=' + domain
    resp = get(ENDPOINT, headers = headers)
    return resp
    
    
def user_cap(api_key, headers = AGENT):
    ''' Show the user capabilities from Similar Web API '''
    ENDPOINT = 'https://api.similarweb.com/user-capabilities?api_key='+api_key
    resp = get(ENDPOINT, headers = AGENT)
    if resp.text[:7] == 'invalid':
        return 'Invalid API Key! Please check the key again.'
    else:
        res = pd.DataFrame(ast.literal_eval(resp.text).items(), columns = ['Type','User Capabilities'])
        res['Type'] = res['Type'].str.capitalize()
        return res
    
    
def get_country(code):
    ''' Get the Country Name from the numeric code '''
    result = COUNTRY_CODES.loc[COUNTRY_CODES['Numeric code'] == code, 'English short name lower case']
    if result.empty:
        return 'Error'
    else:
        return result.iloc[0]
    
    