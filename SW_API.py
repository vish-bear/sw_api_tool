from requests import get
from urllib.parse import urlparse
import pandas as pd
import ast
    
AGENT = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.61 Safari/537.36", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9", "Accept-Language": "en-IN,en-GB;q=0.9,en-US;q=0.8,en;q=0.7", "Accept-Encoding": "gzip, deflate, br", "DNT": "1", "Connection": "close", "Upgrade-Insecure-Requests": "1", "cookie":"_ga=GA1.2.2031308678.1654325430; sgID=f3082b3a-5387-21db-c886-faff8dcf17ad; _gcl_au=1.1.1243191851.1654329514; intercom-id-e74067abd037cecbecb0662854f02aee12139f95=8867d059-aff4-4bf1-a526-7e9e24a86d75; locale=en-us; _vis_opt_s=1%7C; _vis_opt_test_cookie=1; _vwo_uuid=JDF297619C604A60BF1A44A56C50CC479; _vwo_ds=3%241654329526%3A98.72554294%3A%3A; wingify_donot_track_actions=0; .SGTOKEN.SIMILARWEB.COM=b4yBsbivJLWaK_LARLqOVIS7bj92ipc-2upLcCdSKjYsSvZwKCznqq4H76DnTMPYhgGqJ2U2uIT0srgAr6ngLiWpUQ3zC5bDvT9wONG4jVg1vem3i0gBrG_mA4-ZUVRycPX6nGWqLEkiDv-T9XUSmrzDhkZ_FQhvuow5Doy7gsanYFh4DcesYeJxyXTBATaYOze_Jx1KPNQA7xbH3ZMjFHARXWqLP34WxjLfW3MQSlW3KZUkukran2t1x9CbO4mkmXwI9NLeBX-5tJiUbXK4hX4Dta9nomm9RBMTBkjFdD3o6mi42F49AwnsonA-1VRGks8rOJdFZWHBiHyE5PAaO6YUh7jFjIUGjvDGbpR9YxkBodCwHPIPCtqqObn-73wv; registrationpersona_13015169=similarweb.com; _BEAMER_USER_ID_zBwGJEbQ32550=24cfb1f8-8f37-4b7d-af05-62790fc18f68; _BEAMER_FIRST_VISIT_zBwGJEbQ32550=2022-06-04T08:01:08.288Z; panoramaId_expiry=1654974688591; panoramaId=2994c17dd06840470a4ab8e6bd1f16d539385fa372a6d46d483df93cfa567c63; _vwo_uuid_v2=DF2C5CCCEC0DA0EC03115EE4768DD5B27|ca046fe25ed3f5a379a4297cfabaa0e8; pxcts=224871c4-e440-11ec-990d-457961777157; _pxvid=22486684-e440-11ec-990d-457961777157; _hjid=01fc8f72-7039-457d-8bdc-9e5eb1f6b4e5; _hjSessionUser_1406830=eyJpZCI6ImQ0YzdmNzM0LWE3MGItNWQ5Yy04YzFiLWJkYzNiNTgzZTZkYyIsImNyZWF0ZWQiOjE2NTQzMjk1MjcyMDIsImV4aXN0aW5nIjp0cnVlfQ==; __qca=P0-573288976-1654372464831; _vis_opt_exp_944_exclude=1; _vis_opt_exp_937_combi=1; _gid=GA1.2.291731389.1654677398; _uetsid=1d2d6650e70611ec986685eaf9d8c3b1; _uetvid=2973c820e3dc11ec86f5e36c9c9542e6; _wingify_pc_uuid=747e957252244f5a87782181fa377c0a; _pk_ref.1.fd33=%5B%22%22%2C%22%22%2C1654677399%2C%22https%3A%2F%2Fwww.google.com%2F%22%5D; _pk_id.1.fd33=108f903e5b90d4af.1654325431.9.1654677399.1654677398.; sc_is_visitor_unique=rx8617147.1654677399.B555094A9C9B4F89F0F917FD71E364F8.3.3.3.3.3.3.3.2.2; _clck=1mnb8o0|1|f25|0; _clsk=1f4jy5b|1654677399407|1|1|l.clarity.ms/collect; _vwo_sn=352833%3A1; mp_7ccb86f5c2939026a4b5de83b5971ed9_mixpanel=%7B%22distinct_id%22%3A%20%2213015169%22%2C%22%24device_id%22%3A%20%2218142c152a910fe-0d0273c5c108bc-367a6700-1fa400-18142c152aa5f5%22%2C%22url%22%3A%20%22https%3A%2F%2Fpro.similarweb.com%2F%23%2Fresearch%2Fmarketresearch%2Fwebmarketanalysis%2Foverview%2FBusiness_and_Consumer_Services%2F840%2F2021.04-2021.06%3FwebSource%3DTotal%26comparedDuration%3D%22%2C%22is_sw_user%22%3A%20false%2C%22language%22%3A%20%22en-us%22%2C%22section%22%3A%20%22industryAnalysis%22%2C%22sub_section%22%3A%20%22overview%22%2C%22sub_sub_section%22%3A%20%22categoryPerformance%22%2C%22page_id%22%3A%20%22industryAnalysis-overview-categoryPerformance%22%2C%22country%22%3A%20840%2C%22date_range%22%3A%20%222021.04-2021.06%22%2C%22web_source%22%3A%20%22TOTAL%22%2C%22app_mode%22%3A%20null%2C%22main_category%22%3A%20%22Business_and_Consumer_Services%22%2C%22subscription_id%22%3A%20%2246981116%22%2C%22base_product%22%3A%20%22FRO%20Trial%20-%20AI%22%2C%22user_id%22%3A%2013015169%2C%22account_id%22%3A%2010000020%2C%22email%22%3A%20%22vishal.lionking%40gmail.com%22%2C%22last_event_time%22%3A%201654682374480%2C%22%24initial_referrer%22%3A%20%22https%3A%2F%2Fpro.similarweb.com%2F%22%2C%22%24initial_referring_domain%22%3A%20%22pro.similarweb.com%22%2C%22%24user_id%22%3A%20%2213015169%22%2C%22sgId%22%3A%20%22f3082b3a-5387-21db-c886-faff8dcf17ad%22%2C%22site_type%22%3A%20%22Pro%22%2C%22ui_generation%22%3A%20%22%22%7D; intercom-session-e74067abd037cecbecb0662854f02aee12139f95=K0JxcFgyWE1rdkhid3hEK21VN1o4YWR5MFNMRHNZVHBtWmE2YWp1RXdpcHBsZ3Z5QU8rKzRkY1RObjN6S3hMVC0tSCtjRmxNT0s1eFkxazlMUlQ3V0ZXQT09--54b8b146e1f48db2ff3277e01b7c11b5765c331d; _BEAMER_FILTER_BY_URL_zBwGJEbQ32550=true; _px3=65fbf443b985dc33d97be4e657e0ee96c903e0752fc1a06fa6fbff95c1d4b5c4:J15rS3VmfDh2J6kOw1dCDTUAvTwi+OeZLubWOtavlRTEEhVgkZL0MAaKx0/9GYCOGQ/bY1bdS7X3ACLQIxFiyg==:1000:YtTAkIJOOMYIuClqXa5W7PWwQtrGVdUSdiKcULZBRRGl8jNFdaPWJCDH845B9BaFVx0PmJqiQ/4ollDPw6mHkL4VMnsWIqdtA9oV6WvTHtM90oZAaJ7ZJUmkObN9OvRS1sEnEVhIhBglQQPP7Cxu1wlZ7U3ndU9kDnTlnKg54jLD+ASqQtwQTRHnMDB/sOenU8xW4kLSFPNhUucy9JN6PA==","if-none-match":'W/"546-6G6GE1Hxfy5euE4EN9zutMD/fVs"'}

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
    
    