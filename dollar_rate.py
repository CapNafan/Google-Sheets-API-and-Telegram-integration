import requests
import xmltodict


def get_dollar_rate():
    url = f'http://www.cbr.ru/scripts/XML_daily.asp'
    response = requests.get(url)
    data = xmltodict.parse(response.content)    # xmltodict makes a python dict() from XML
    usd_rate = data['ValCurs']['Valute'][10]['Value']
    usd_rate = usd_rate.replace(',', '.')
    return float(usd_rate)


