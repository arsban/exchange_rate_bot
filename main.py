import requests
import xmltodict
import datetime
import json


def exchage_get(date_req):  # принимает даты, и выдает результат по этой дате
    url = f"http://www.cbr.ru/scripts/XML_daily.asp?date_req={date_req}"
    payload = {}
    headers = {
        'Cookie': '__ddg1_=kudnGZIrhMMywbyS4hvW'
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    dict_data = xmltodict.parse(response.content)
    json_data = json.dumps(dict_data)
    return json_data


def get_format_date():
    today_date = datetime.date.today()
    year = (str(today_date).strip().split("-"))[0]
    month = (str(today_date).strip().split("-"))[1]
    day = (str(today_date).strip().split("-"))[2]
    date_req = f"{int(day)}/{int(month)}/{int(year)}" # преобразует дату в формат 20/10/2022 # noqa
    return date_req


if __name__ == "__main__":
    with open('data.json', 'w') as f:
        print(exchage_get(get_format_date()), file=f, end="")

    with open('data.json') as file:
        templates = json.load(file)
        date = templates["ValCurs"]["@Date"]  # дата по которой ориентирован курс # noqa
        dollar_name = templates["ValCurs"]["Valute"][10]["Name"]  # название валюты # noqa
        dollar_value = templates["ValCurs"]["Valute"][10]["Value"]  # курс валюты  # noqa
        euro_name = templates["ValCurs"]["Valute"][11]["Name"]  # название валюты # noqa
        euro_value = templates["ValCurs"]["Valute"][11]["Value"]  # курс валюты  # noqa
        print(
            f"ЦБ РФ обновил официальные курсы валют.\n"
            f"Курс на {date}\n"
            f"{dollar_name} - {dollar_value}\n"
            f"{euro_name} - {euro_value}\n",
            end=""
        )
