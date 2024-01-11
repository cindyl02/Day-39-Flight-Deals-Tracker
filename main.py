# This file will need to use the DataManager,FlightSearch, FlightData, NotificationManager classes to achieve the program requirements.
from data_manager import DataManager
import datetime as dt
from flight_search import FlightSearch
from notification_manager import NotificationManager

flight_search = FlightSearch()
data_manager = DataManager()
notification_manager = NotificationManager()
sheet_data = data_manager.get_destination_data()
DEPARTURE_IATA_CODE = "YVR"

if sheet_data[0]["iataCode"] == "":
    city_names = [row["city"] for row in sheet_data]
    codes = flight_search.get_iata_codes(city_names)
    print(codes)
    data_manager.update_destination_codes(codes)
    sheet_data = data_manager.get_destination_data()

today = dt.datetime.now()
date_from = today + dt.timedelta(days=1)
date_from = date_from.strftime("%d/%m/%Y")
date_to = today + dt.timedelta(days=6 * 30)
date_to = date_to.strftime("%d/%m/%Y")

for destination in sheet_data:
    flight = flight_search.search_flight(DEPARTURE_IATA_CODE, destination["iataCode"], date_from, date_to)
    if flight is None:
        flight = flight_search.search_flight(DEPARTURE_IATA_CODE, destination["iataCode"], date_from, date_to, 1)
    if flight is None:
        continue
    if "lowestPrice" in destination and flight.price < destination["lowestPrice"]:
        message = f"Subject:Low price alert!\n\nOnly ${flight.price} to fly from {flight.origin_city}-{flight.origin_airport} to {flight.destination_city}-{flight.destination_airport} from {flight.out_date} to {flight.return_date}.\n"
        if flight.via_city != "":
            message += f"Flight has {flight.stop_overs} stop over, via {flight.via_city}. Nights in destination is {flight.nights_in_dest} nights."
        notification_manager.send_email(message)
        data_manager.update_row(destination["id"], price=flight.price, out_date=flight.out_date, return_date=flight.return_date, stop_overs=flight.stop_overs, via_city=flight.via_city)
