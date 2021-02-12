from io import BytesIO
import requests
from PIL import Image
from spn_counter import spn_counter

search_api_server = "https://search-maps.yandex.ru/v1/"
api_key = "dda3ddba-c9ea-4ead-9010-f43fbc15c6e3"

text = input("Введите адрес: ")

search_params = {
    "apikey": api_key,
    "text": text,
    "lang": "ru_RU",
}

response = requests.get(search_api_server, params=search_params)
if not response:
    print("Место не найдено")
else:
    json_response = response.json()

    place = json_response["features"]
    if place:
        place = place[0]
        place_name = place["properties"]["name"]
        try:
            place_size = place["properties"]["boundedBy"]
        except KeyError:
            place_size = json_response["properties"]["SearchResponse"]["boundedBy"]

        spn = spn_counter(place_size)

        point = place["geometry"]["coordinates"]
        org_point = "{0},{1}".format(point[0], point[1])

        map_params = {
            "spn": ",".join(spn),
            "l": "map",
            "pt": "{0},pm2dgl".format(org_point),
        }

        map_api_server = "http://static-maps.yandex.ru/1.x/"
        response = requests.get(map_api_server, params=map_params)

        Image.open(BytesIO(response.content)).show()
    else:
        print("Место не найдено")
