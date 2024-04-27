# This file will need to use the DataManager,FlightSearch, FlightData, NotificationManager classes to achieve the program requirements.
from data_manager import DataManager
from flight_search import FlightSearch
from datetime import datetime, timedelta


# Set API endpoints and keys, replace them with your own endpoints and keys.
sheety_prices_endpoint = "https://api.sheety.co/596407487435113fa1b524e86a87b95d/flightDealPro/prices"
sheety_users_endpoint = "https://api.sheety.co/596407487435113fa1b524e86a87b95d/flightDealPro/users"
tequila_endpoint = "https://api.tequila.kiwi.com"
tequila_api_key = "yMehLUMCrfKBZ5wANlk1tYZVh70fBFXG"

DataManager.SetEndPoint(sheety_prices_endpoint, sheety_users_endpoint)
FlightSearch.SetEndPoint(tequila_endpoint, tequila_api_key)


# Ask users to sign up their account.
print("Welcome to Fanfan's Flight Club🥳.\nWe can find the best flight deals and email you.")
first_name = input("What's your first name?\n")
last_name = input("What's your last name?\n")
no_confirm = True
while no_confirm:
    email = input("What's your email?\n")
    confirm_email = input("Please confirm your email again.\n")
    if email == confirm_email:
        # DataManager.SignInUser(first_name, last_name, email)
        no_confirm = False
    print("The two inputs are different, please insert again.")
print("You has signed up successfully🥰!")

# Collect the user flight data.
from_city = input("Which city do you fly from?\n").capitalize()
input_cities = input("Which city do you want to fly to? (If you have more than one destinations, separated them by comma. Example: Paris, Bali)\n")
to_cities = [city.strip().capitalize() for city in input_cities]
row_number = 2
formatted_cities = []
for city in to_cities:
    formatted_cities.append(
        {
            "to_city": city,
            "id": row_number
        }
    )
    row_number += 1

# Search for the flight prices from one city to all the destinations in the Google Sheet and collect the result.
from_city_code = FlightSearch.SearchCityCode(from_city)
date_range = input("Please insert your departure date. Example: 26/04/2014 (means a specific day)  or 26/04/2014, 25/06/2024 (means a range)\n")
split_date = date_range.split(",")
date_from = split_date[0].strip()
if len(split_date) > 1:
    date_to = split_date[1].strip()
else:
    date_to = split_date[0].strip()

update_data = []
for city_info in formatted_cities:
    to_city = city_info["city"]
    to_city_code = FlightSearch.SearchCityCode(to_city)
    flights_data = FlightSearch.SearchFlight(from_city_code, to_city_code, date_from, date_to)
    if flights_data:
        for flight in flights_data:
            from_city = flight["cityFrom"]
            iata_code = flight["cityCodeFrom"]
            from_airport = flight["flyFrom"]
            to_airport = flight["flyTo"]
            dep_date = flight["local_departure"].split("T")[0]
            dep_time = flight["local_departure"].split("T")[1].split(".")[0] # Only extract the time.
            arr_date = flight["local_arrival"].split("T")[0]
            arr_time = flight["local_arrival"].split("T")[1].split(".")[0] # Only extract the time.
            price = flight["price"]
            order_link = flight["deep_link"]
            if flight["route"] > 1:
                via_city = flight["route"][0]["cityTo"]
                stopover = 1
            else:
                via_city = ""
                stopover = 0
            try:
                city_info["flight"]
            except KeyError:
                city_info["flight"] = []
            finally:
                city_info["flight"].append(
                    {
                        "from_city": from_city,
                        "iata_code": iata_code,
                        "from_airport": from_airport,
                        "to_airport": to_airport,
                        "departure_date": dep_date,
                        "departure_time": dep_time,
                        "arrival_date": arr_date,
                        "arrival_time": arr_time,
                        "price": price,
                        "order_link": order_link,
                        "via_city": via_city
                    }
                )
        # After finding all flights, then find the cheapest flight.
        cheapest_flight = min(city_info["flight"], key=lambda x: x["price"])
        update_data.append(
            {
                "city": city_info["city"],
                "id": city_info["id"],
                "cheapest_flight": cheapest_flight
            }
        )
        # Update the cheapest flight information to Google sheet
        DataManager.UpdateCheaptestFlight(update_data)
        print(f"Cheapest flight deal from {from_city} to {to_city} found! It's departured on {dep_date} at {dep_time} and arrived on {arr_date} at {arr_time} with {stopover} stopover. Please check this link for details: {order_link}.")
    else:
        print(f"No flight found from {from_city} to {to_city}.")

