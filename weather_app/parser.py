from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
from datetime import datetime

from .models import Weather


BASE_URL = "https://pogoda.meta.ua/"
WEATHER_URL = urljoin(BASE_URL, "ua/Kyivska/Kyivskiy/Kyiv/5/")

month_mapping = {
    "січня": "01",
    "лютого": "02",
    "березня": "03",
    "квітня": "04",
    "травня": "05",
    "червня": "06",
    "липня": "07",
    "серпня": "08",
    "вересня": "09",
    "жовтня": "10",
    "листопада": "11",
    "грудня": "12",
}


def convert_date_string(date_str):
    day, month = date_str.split()
    month_number = month_mapping.get(month)
    return f"{day}.{month_number}.2023"


def parse_weather():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"
    }
    response = requests.get(WEATHER_URL, headers=headers).content
    soup = BeautifulSoup(response, "html.parser")
    weather_days = soup.find_all("div", class_="five-days__day")
    for day in weather_days:
        date_str = day.find("span", class_="date").text.strip()
        converted_date_str = convert_date_string(date_str)
        date = datetime.strptime(
            converted_date_str, "%d.%m.%Y"
        ).date()  # Конвертація в тип date
        temperature_spans = day.find("span", class_="high")
        temperature_max = int(temperature_spans.text.strip().replace("°", ""))
        elem = day.find("div", class_="five-days__icon")
        description = elem.get("data-tippy-content")
        try:
            # Спробувати знайти об'єкт Weather за датою
            weather = Weather.objects.get(date=date)
            # Оновити значення температури та опису
            weather.temperature = temperature_max
            weather.weather_description = description
            weather.save()
        except Weather.DoesNotExist:
            # Якщо об'єкт Weather за датою не існує, створити новий
            weather = Weather.objects.create(
                date=date, temperature=temperature_max, weather_description=description
            )
            weather.save()
