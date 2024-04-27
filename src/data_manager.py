import requests


class DataManager:
    @classmethod
    def SetEndPoint(cls, prices_endpoint, users_endpoint):
        cls.m_prices_endpoint = prices_endpoint
        cls.m_users_endpoint = users_endpoint
    # This class is responsible for talking to the Google Sheet.
    ## Define a method to get the city names from the Google Sheet.
    @classmethod
    def GetCityInfo(cls):
        """

        :return: City information on the Google Sheet.
        """
        response = requests.get(cls.m_prices_endpoint)
        city_info = response.json()['prices']
        return city_info

    @classmethod
    def UpdateCityCode(cls, row_id, city_code):
        """

        :param row_id: City's row id.
        :param city_code: City's code
        :return: None
        """
        new_data = {
            "price": {
                "iataCode": city_code
            }
        }
        response = requests.put(
            url=f"{cls.m_prices_endpoint}/{row_id}",
            json=new_data
        )
        print("IATA Code has been updated successfully.")
        return

    @classmethod
    def UpdateCheaptestFlight(cls, update_data):
        """

        :param update_data: A list of dictionary, each dictionary inludes the updated information of the cities.
        :return: None
        """
        for row in update_data:
            new_data = {
                "price": {
                    "fromCity": row["cheapest_flight"]["from_city"],
                    "iataCode": row["cheapest_flight"]["iata_code"],
                    "lowestPrice": row["cheapest_flight"]["price"],
                    "fromAirport": row["cheapest_flight"]["from_airport"],
                    "toAirport": row["cheapest_flight"]["to_airport"],
                    "departureDate": row["cheapest_flight"]["departure_date"],
                    "departureTime": row["cheapest_flight"]["departure_time"],
                    "arrivalDate": row["cheapest_flight"]["arrival_date"],
                    "arrivalTime": row["cheapest_flight"]["arrival_time"],
                    "orderLink": row["cheapest_flight"]["order_link"],
                    "viaCity": row["cheapest_flight"]["via_city"]
                }
            }
            response = requests.put(
                url=f"{cls.m_prices_endpoint}/{row['id']}",
                json=new_data
            )
            print(f"{row["city"]}'s flight information has been updated successfully.")
        return

    @classmethod
    def SignInUser(cls, first_name, last_name, email):
        """

        :param first_name: User's first name.
        :param last_name: User's last name.
        :param email: Uer's email.
        :return: None
        """
        user_data = {
            "user": {
                "firstName": first_name,
                "lastName": last_name,
                "email": email
            }
        }
        response = requests.post(url=cls.m_users_endpoint, json=user_data)
        print("User data uploaded!")
        return

