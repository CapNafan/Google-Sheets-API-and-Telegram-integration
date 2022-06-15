import requests
import xmltodict
import datetime


def get_dollar_rate():
    current_date = datetime.date.today().strftime("%d/%m/%Y")  # format date to
    url = f'http://www.cbr.ru/scripts/XML_daily.asp?date_req={current_date}'
    response = requests.get(url)
    data = xmltodict.parse(response.content)    # xmltodict makes a python dict() from XML
    return data['ValCurs']['Valute'][10]['Value']

