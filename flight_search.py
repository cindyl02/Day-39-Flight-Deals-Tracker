import requests
from flight_data import FlightData
import os

TEQUILA_ENDPOINT = "https://api.tequila.kiwi.com"
TEQUILA_API_KEY = os.environ.get("TEQUILA_API_KEY")
HEADERS = {
    "apikey": TEQUILA_API_KEY
}


class FlightSearch:

    def get_iata_codes(self, city_names):
        location_endpoint = f"{TEQUILA_ENDPOINT}/locations/query"
        codes = []
        for city in city_names:
            query = {
                "term": city,
                "locationTypes": "city",
                "locale": "en-US",
                "limit": 1,
                "activeOnly": "true"
            }
            response = requests.get(url=location_endpoint, params=query, headers=HEADERS)
            response.raise_for_status()
            codes.append(response.json()["locations"][0]["code"])
        return codes

    def search_flight(self, departure_airport_code, arrival_airport_code, date_from, date_to):
        query = {
            "fly_from": departure_airport_code,
            "fly_to": arrival_airport_code,
            "date_from": date_from,
            "date_to": date_to,
            "nights_in_dst_from": 7,
            "nights_in_dst_to": 28,
            "one_for_city": 1,
            "curr": "CAD",
            "max_stopovers": 0,
            "limit": 1
        }
        response = requests.get(url=f"{TEQUILA_ENDPOINT}/v2/search", params=query, headers=HEADERS)
        response.raise_for_status()
        try:
            data = response.json()["data"][0]
            print(data)
        except IndexError:
            query["max_stopovers"] = 2
            response = requests.get(url=f"{TEQUILA_ENDPOINT}/v2/search", params=query, headers=HEADERS)
            response.raise_for_status()
            data = response.json()["data"][0]
            print(data)
            flight_data = FlightData(price=data["price"], origin_city=data["route"][0]["cityFrom"],
                                     origin_airport=data["route"][0]["flyFrom"],
                                     destination_city=data["route"][1]["cityTo"],
                                     destination_airport=data["route"][1]["flyTo"],
                                     out_date=data["route"][0]["local_departure"].split("T")[0],
                                     return_date=data["route"][-1]["local_departure"].split("T")[0],
                                     stop_overs=1,
                                     via_city=data["route"][0]["cityTo"], nights_in_dest=data["nightsInDest"])
            print(f"{flight_data.destination_city}: ${flight_data.price}")
            return flight_data
        else:
            flight_data = FlightData(price=data["price"], origin_city=data["route"][0]["cityFrom"],
                                     origin_airport=data["route"][0]["flyFrom"],
                                     destination_city=data["route"][0]["cityTo"],
                                     destination_airport=data["route"][0]["flyTo"],
                                     out_date=data["route"][0]["local_departure"].split("T")[0],
                                     return_date=data["route"][1]["local_departure"].split("T")[0],
                                     nights_in_dest=data["nightsInDest"])

            print(f"{flight_data.destination_city}: ${flight_data.price}")
            return flight_data
