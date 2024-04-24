from scrapy import Selector
import requests
from urllib.parse import parse_qs
import json


#######################################################################################
####################################### utils #######################################
def find_between_strings(s, first, last):
    try:
        return (s.split(first))[1].split(last)[0]
    except ValueError:
        return ""

####################################### Security Part #################################
#### GET params from html
headers = {
    'Host': 'ooredoo.dz',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Dest': 'document',
    'Referer': 'https://l.facebook.com/',
    # 'Accept-Encoding': 'gzip, deflate, br',
}

params = {
    'fbclid': 'IwAR1oxm4yeW7H6wG-cR5J-ZHVzo91dPcZMKnA0UEOFRLoPjgVD9WeAZZ1xj8_aem_ASOlTgsXhXgu_4QFSR7qpgI_Bt3eCsVLPT5wmTRXzNWkhAPmNtuRcm0IHf0QZog3ZV9XO_vafMJ6SS8kxZOg0_NF',
}

response = requests.get(
    'https://ooredoo.dz/fr/web/guest/particuliers/assistance/trouvez-nous',
    params=params,
    headers=headers,
    verify=False,
)
html_sel = Selector(text=response.text)
script_element = html_sel.css('script:contains(getBasicTokenAsync)::text').get()
params_string = find_between_strings(script_element, 'let databody =', ';').strip("' ")
decoded_dict = parse_qs(params_string)
params_dict = {key: value[0] for key, value in decoded_dict.items()}
params_dict

### Get access tokens from in the middle API
headers = {
    'Host': 'ooredoo.dz',
    'Content-Type': 'application/x-www-form-urlencoded',
    # 'Content-Length': '135',
}
response = requests.post('https://ooredoo.dz/o/oauth2/token', headers=headers, data=params_dict)
access_tokens = json.loads(response.text)
access_tokens

####################################### End of Security Part #################################
####################################### Data extraction part #################################

authorization = f'{access_tokens["token_type"]} {access_tokens["access_token"]}'
headers = {
    'Host': 'ooredoo.dz',
    'Accept-Language': 'fr-FR',
    'Authorization': authorization
    }
params = {
    'filter': "villaya eq '15'", # stores are provided based on the wilaya code
    'pageSize': '1000',
}
response = requests.get('https://ooredoo.dz/o/c/stores/', params=params, headers=headers)
response.text

# final data
data = json.loads(response.text)
# first location
print(data['items'][0])

