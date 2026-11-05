
import requests
import xml.etree.ElementTree as ET
from datetime import datetime


def get_exchange_rate(currency, date):
    if currency == "RUB":
        return 1.0

    formatted_date = datetime.strptime(
        date, "%Y-%m-%d"
    ).strftime("%d/%m/%Y")

    url = "https://www.cbr.ru/scripts/XML_daily.asp"

    response = requests.get(
        url,
        params={"date_req": formatted_date},
        timeout=10
    )
    response.raise_for_status()

    root = ET.fromstring(response.content)

    for valute in root.findall("Valute"):
        char_code = valute.findtext("CharCode")

        if char_code == currency:
            nominal = int(valute.findtext("Nominal"))
            value = float(
                valute.findtext("Value").replace(",", ".")
            )

            return value / nominal

    raise ValueError(
        f"Валюта {currency} не найдена в данных ЦБ РФ"
    )
