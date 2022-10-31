import random
from time import sleep

import requests
from bs4 import BeautifulSoup
import json
import csv

# url = "https://health-diet.ru/table_calorie/"
#
headers = {
    "Accept": "*/*",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 "
                  "Safari/537.36 "
}
#
# req = requests.get(url, headers=headers)
# src = req.text
# # print(src)
#
# with open("index.html", "w") as f:
#     f.write(src)
#
# with open("index.html") as f:
#     src = f.read()
#
# soup = BeautifulSoup(src, "lxml")
# all_products_href = soup.findAll(class_="mzr-tc-group-item-href")
#
# all_categories_dict = {}
#
# for item in all_products_href:
#     item_text = item.text
#     item_href = "https://health-diet.ru" + item.get("href")
#
#     all_categories_dict[item_text] = item_href
#
# with open("all_category_dict.json", "w") as f:
#     json.dump(all_categories_dict, f, indent=4, ensure_ascii=False)

with open("all_category_dict.json") as f:
    all_categories = json.load(f)

iteration_count =int(len(all_categories)) - 1
count = 0
print(f"Всего итераций: {iteration_count}")

for category_name, category_href in all_categories.items():
    rep = [",", " ", "-", "'"]
    for items in rep:
        if items in category_name:
            category_name = category_name.replace(items, "_")

    req = requests.get(url=category_href, headers=headers)
    src = req.text

    with open (f"data/{category_name}.html", "w") as f:
        f.write(src)

    with open(f"data/{category_name}.html") as f:
        src = f.read()

    soup = BeautifulSoup(src, "lxml")
    table_head = soup.find(class_="mzr-tc-group-table").find("tr").find_all("th")
    product = table_head[0].text
    calories = table_head[1].text
    proteins = table_head[2].text
    fats = table_head[3].text
    carbohydrate = table_head[4].text

    with open(f"data/{category_name}.csv", "w", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(
            (
                product,
                calories,
                proteins,
                fats,
                carbohydrate
            )
        )

    product_data = soup.find(class_="mzr-tc-group-table").find("tbody").find_all("tr")
    product_info = []
    for item in product_data:
        product_tds = item.find_all("td")

        title = product_tds[0].find("a").text
        calories = product_tds[1].text
        proteins = product_tds[2].text
        fats = product_tds[3].text
        carbohydrate = product_tds[4].text

        product_info.append(
            {
                "Title": title,
                "Calories": calories,
                "Proteins": proteins,
                "Fats": fats,
                "Carbohydrates": carbohydrate
            }

        )

        with open(f"data/{category_name}.csv", "a", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(
                (
                    title,
                    calories,
                    proteins,
                    fats,
                    carbohydrate
                )
            )

    with open(f"data/{category_name}.json", "w") as f:
        json.dump(product_info, f, indent=4, ensure_ascii=False)

    count += 1
    print(f"# Итерация {count}. {category_name} записан...")
    iteration_count = iteration_count - 1

    if iteration_count == 0:
        print("Работа завершена!")
        break

    print(f"Осталось итераций: {iteration_count}")
    sleep(random.randrange(2, 5))



