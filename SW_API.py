from requests import get
from urllib.parse import urlparse
import pandas as pd
import ast
from functools import lru_cache
    
AGENT = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.61 Safari/537.36", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9", "Accept-Language": "en-IN,en-GB;q=0.9,en-US;q=0.8,en;q=0.7", "Accept-Encoding": "gzip, deflate, br", "DNT": "1", "Upgrade-Insecure-Requests": "1", "if-none-match" : 'W/"511-Ah29p4csjh43WYLW/X57SUuszl0"', "sec-ch-ua" : '" Not A;Brand";v="99", "Chromium";v="102", "Google Chrome";v="102"', "upgrade-insecure-requests" : "1", "sec-fetch-user" : "?1", "sec-fetch-mode":"navigate","sec-fetch-dest":"document",'Connection': 'keep-alive'}

COUNTRY_CODES = pd.read_csv('wikipedia-iso-country-codes.csv')

@lru_cache(maxsize=None)
def swGet(website, headers = AGENT):
    ''' Extract the data from the Similar Web API '''
    domain = '{uri.netloc}'.format(uri=urlparse(website))
    domain = domain.replace("www.", "")
    ENDPOINT = 'https://data.similarweb.com/api/v1/data?domain=' + domain
    resp = get(ENDPOINT, headers = headers)
    return resp
    
@lru_cache(maxsize=None)    
def user_cap(api_key, headers = AGENT):
    ''' Show the user capabilities from Similar Web API '''
    ENDPOINT = 'https://api.similarweb.com/user-capabilities?api_key='+api_key
    resp = get(ENDPOINT, headers = headers)
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
    
    