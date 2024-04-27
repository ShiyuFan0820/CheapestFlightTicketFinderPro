import requests


class FlightSearch:
    #This class is responsible for talking to the Flight Search API.
    @classmethod
    def SetEndPoint(cls, endpoint, api_key):
        cls.m_endpoint = endpoint
        cls.m_api_key = api_key
    @classmethod
    def SearchCityCode(cls, city_name):
        """

        :param city_name: Name of the city.
        :return: The city code.
        """
        query_endpoint = f'{cls.m_endpoint}/locations/query'
        headers = {'apikey': cls.m_api_key}
        query = {
            'term': city_name,
            "location_types": "city"
        }
        query_response = requests.get(url=query_endpoint, headers=headers, params=query)
        query_data = query_response.json()
        city_code = query_data['locations'][0]['code']
        return city_code

    @classmethod
    def SearchFlight(cls, fly_from, fly_to, date_from, date_to, adults=1, children=0, infants=0, selected_cabins="M", curr="GBP", max_stopovers=0, one_for_city=0, ret_from_diff_city=False, ret_to_diff_city=False):
        """

        :param fly_from: City code of departure city.
        :param fly_to: City code of destination city.
        :param date_from: The start range of departure date, the format should be like dd/mm/yyyy.
        :param date_to: The end range of departure date, the format should be like dd/mm/yyyy.
        :param adults: Default value is 1.
        :param children: Default value is 0.
        :param infants: Default value is 0.
        :param selected_cabins: Default value is "M". M (economy), W (economy premium), C (business), or F (first class).
        :param curr: Default value is "GBP".
        :param max_stopovers: Default value is 0. Means direct flight.
        :param one_for_city: Default value is 0.
        :param ret_from_diff_city: Default value is False.
        :param ret_to_diff_city: Default value is False.
        :return: A list of dictionary which includes flight information.
        """
        search_endpoint = f"{cls.m_endpoint}/v2/search"
        headers = {
            "apikey": cls.m_api_key
        }
        info = {
            "fly_from": fly_from,
            "fly_to": fly_to,
            "date_from": date_from,
            "date_to": date_to,
            "adults": adults,
            "children": children,
            "infants": infants,
            "selected_cabins": selected_cabins,
            "curr": curr,
            "max_stopovers": max_stopovers,
            "one_for_city": one_for_city,
            "ret_from_diff_city": ret_from_diff_city,
            "ret_to_diff_city": ret_to_diff_city
        }
        response = requests.get(
            url=search_endpoint,
            headers=headers,
            params=info
        )
        try:
            data = response.json()["data"][0]
        except IndexError:
            info["max_stopovers"] = 1
            new_response = requests.get(
                url=search_endpoint,
                headers=headers,
                params=info
            )
            try:
                new_data = new_response.json()["data"][0]
            except IndexError:
                return None
            else:
                return new_response.json()["data"][0]
        return response.json()["data"]

