import requests
import xmltodict
import datetime
import json
import telegram_send


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
    today_date = (datetime.date.today() + datetime.timedelta(days=1))
    year = (str(today_date).strip().split("-"))[0]
    month = (str(today_date).strip().split("-"))[1]
    day = (str(today_date).strip().split("-"))[2]
    date_req = f"{day}/{month}/{year}" # преобразует дату в формат 20/10/2022 # noqa
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
        telegram_send.send(messages=[
            f"ЦБ РФ обновил официальные курсы валют.\n"
            f"Курс на {date}\n"
            f"{dollar_name} - {dollar_value}\n"
            f"{euro_name} - {euro_value}\n"
        ])
# команды в консоли для настройки telegram-send:
# telegram-send --configure | для отправки сообщений в бота
# telegram-send --configure-group | для отправки сообщений в группу
# telegram-send --configure-channel | для отправки сообщений в канал
