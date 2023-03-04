import requests
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

API_ID = os.getenv("API_ID")
API_KEY = os.getenv("API_KEY")
SHEETY_API = os.getenv("SHEETY_API")

exercise_endpoint = "https://trackapi.nutritionix.com/v2/natural/exercise"
# api that sheety gave me when I signed up and added my project
sheety_endpoint = "https://api.sheety.co/1a2fdbd443424c5f4dcfb760d6c4323d/myWorkouts/workouts"

exercise_text = input("What exercises did you do? ")

user_params = {
    "query": exercise_text,
    "gender": "female",
    "weight_kg": 170,
    "height_cm": 170.18,
    "age": 40
}

# headers to get id and api key
headers = {
    "x-app-id": API_ID,
    "x-app-key": API_KEY
}

# posting my exercise based on my input
response = requests.post(url=exercise_endpoint, json=user_params, headers=headers)
result = response.json()

# sheety header establishing the authorization aka api key from sheety
sheety_header = {
    "Authorization": f"Bearer {SHEETY_API}"
}

# putting the date and time into the format we want
today_date = datetime.now().strftime("%m/%d/%Y")
today_time = datetime.now().strftime("%H:%M:%S")

# pulling the data from the post request above in json format and formatting it with the info we need...title()
# makes sure every first letter in each word is uppercase...for loop is saying if exercises are inputted then use
# params...keys are the columns and values are what the keys are in the original json file
for exercise in result["exercises"]:
    sheet_params = {
        "workout": {
            "date": today_date,
            "time": today_time,
            "exercise": exercise["user_input"].title(),
            "duration": exercise["duration_min"],
            "calories": exercise["nf_calories"]
            }
        }
    sheet_response = requests.post(url=sheety_endpoint, json=sheet_params, headers=sheety_header)
    print(sheet_response.text)