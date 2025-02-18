import requests
class Environment:
    def __init__(self,):
        self.temperature = self.get_temperature()

    def get_temperature(self):
        url = "https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&appid={API_key}"
        response =  requests.get(url)

        if response.status_code == 200:

