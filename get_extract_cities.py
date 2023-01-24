"""
Парсер страницы Википедии со списком городов России.
Сохраняет в файл cities.txt
"""


from bs4 import BeautifulSoup
import requests

# Скачиваем страницу Википедии со списком городов России
URL = "https://ru.wikipedia.org/wiki/%D0%A1%D0%BF%D0%B8%D1%81%D0%BE%D0%BA_%D0%B3%D0%BE%D1%80%D0%BE%D0%B4%D0%BE%D0%B2_%D0%A0%D0%BE%D1%81%D1%81%D0%B8%D0%B8"
r = requests.get(URL)
html = r.content

# Вытаскиваем города России из html.
soup = BeautifulSoup(html, features="html.parser")
table = soup.find("table", attrs={"class": "standard sortable"})

# Удаляем из названий городов "призн." и сохраняем в файл cities.txt
with open("cities.txt", "w") as f:
    for row in table.find_all("tr")[2:]:
        city = row.find_all("td")[2].get_text().strip()
        if "призн." in city:
            new_city = city[0:-7]
            f.write(f"{new_city}\n")
        else:
            f.write(f"{city}\n")
