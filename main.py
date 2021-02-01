import os, requests
from datetime import datetime, date, timedelta
from pytz import timezone

tz = timezone(os.getenv("MY_TIMEZONE"))
today = datetime.now(tz)
my_date = today.strftime("%d/%m/%Y")
my_time = today.strftime("%H:%M:%S")
birth_date = datetime.strptime(os.getenv("DOB"), '%Y-%m-%d').date()


weight_kg = os.getenv("WEIGHT")
height_cm = os.getenv("HEIGHT")
age = (date.today() - birth_date) // timedelta(days=365.2425)
gender = os.getenv("GENDER")

sheety_bearer_token = os.getenv("SHEETY_BEARER_TOKEN")
nutritionix_id = os.getenv("NUTRITIONIX_ID")
nutritionix_apiKey = os.getenv("NUTRITIONIX_API_KEY")

headers = {"x-app-id": nutritionix_id, "x-app-key": nutritionix_apiKey}
sheety_headers = {"Authorization": f"Bearer {sheety_bearer_token}"}

query_string = input("Tell me which exercises you did:")

nutritionix_endpoint = "https://trackapi.nutritionix.com/v2/natural/exercise"

exercise_data = {
    "query": query_string,
    "gender": gender,
    "weight_kg": weight_kg,
    "height_cm": height_cm,
    "age": age
}

response = requests.post(url=nutritionix_endpoint, json=exercise_data, headers=headers)
response.raise_for_status()

records = response.json()

data_to_sheety = [{"date": my_date, "time": my_time, "exercise": record["name"].title(),
                   "duration": record["duration_min"], "calories": record["nf_calories"]} for record in records["exercises"]]

sheety_endpoint = os.getenv("SHEETY_ENDPOINT")



for record in data_to_sheety:
    sheety_data = {"workout": record}

    response = requests.post(sheety_endpoint, json=sheety_data, headers=sheety_headers)
    response.raise_for_status()
