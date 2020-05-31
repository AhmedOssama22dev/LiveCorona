import json
import threading
import time

import requests

api_key = "tetdNjTHiC9n"
project_key = "tjTtEYxKzDBM"


class ParseData:
    def __init__(self, api_key, project_key):
        self.api_key = api_key
        self.project_key = project_key
        self.params = {"api_key": self.api_key}
        self.data = self.get_data()

    def get_data(self):
        r = requests.get(f'https://www.parsehub.com/api/v2/projects/{self.project_key}/last_ready_run/data',
                         params=self.params)
        data = json.loads(r.text)
        return data

    def get_total_cases(self):
        data = self.data['total_data']
        for content in data:
            if (content['name'] == "Coronavirus Cases:"):
                return content['value']

    def get_total_deaths(self):
        data = self.data['total_data']
        for content in data:
            if (content['name'] == "Deaths:"):
                return content['value']

    def get_country_data(self, country):
        data = self.data['country']
        for content in data:
            if (content['name'].lower() == country.lower()):
                return content
    def update_data(self):
        response = requests.post(f'https://www.parsehub.com/api/v2/projects/{self.project_key}/run',params=self.params)
        def poll():
            time.sleep(0.1)
            old_data=self.data
            while True:
                new_data = self.get_data()

                if new_data!=old_data:
                    print("Data updated succesfully")
                    break
                else:
                    time.sleep(5)
data = ParseData(api_key, project_key)
data.update_data()
print(f"Total world cases: {data.get_total_cases()}")
print(f"Total world deaths : {data.get_total_deaths()}")
country=""
print("Enter stop instead of a country to abort")
while(country!="stop"):
    country = input("Enter a country")
    if(country!="stop"):
     try:
         print(f"Total cases in {country}: {data.get_country_data(country)['total_cases']}")
     except:
         print("Enter a valid country")
