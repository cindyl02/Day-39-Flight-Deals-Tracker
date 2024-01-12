import requests
from pprint import pprint
import os

SHEETY_ENDPOINT = os.environ.get("SHEETY_ENDPOINT")
TOKEN = os.environ.get("TOKEN")
BEARER_HEADERS = {
    "Authorization": TOKEN
}


class DataManager:
    def __init__(self):
        self.destination_data = {}

    def get_destination_data(self):
        response = requests.get(url=SHEETY_ENDPOINT, headers=BEARER_HEADERS)
        response.raise_for_status()
        self.destination_data = response.json()["sheet1"]
        return self.destination_data

    def update_destination_codes(self, codes):
        for index, city in enumerate(self.destination_data):
            new_data = {
                "sheet1": {
                    "iataCode": codes[index]
                }
            }
            response = requests.put(url=f"{SHEETY_ENDPOINT}/{city["id"]}", json=new_data, headers=BEARER_HEADERS)
            response.raise_for_status()
            pprint(response.text)

    def update_row(self, row_id, **kwargs):
        new_data = {
            "sheet1": {
                "lowestPrice": kwargs["price"],
                "outDate": kwargs["out_date"],
                "returnDate": kwargs["return_date"],
                "stopOvers": kwargs["stop_overs"],
                "viaCity": kwargs["via_city"]
            }
        }
        response = requests.put(url=f"{SHEETY_ENDPOINT}/{row_id}", json=new_data, headers=BEARER_HEADERS)
        response.raise_for_status()
        pprint(response.text)
