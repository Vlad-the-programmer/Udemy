import smtplib

FROM = "vladklimchukit@gmail.com"
TO = "klamchukmoney@gmail.com"
PASSWORD = "muxtar18"

import requests
from datetime import datetime
import time

MY_LAT = 51.507351 # Your latitude
MY_LONG = -0.127758 # Your longitude


def iss_is_overhead():
        response = requests.get(url="http://api.open-notify.org/iss-now.json")
        response.raise_for_status()
        data = response.json()
        iss_latitude = float(data["iss_position"]["latitude"])
        iss_longitude = float(data["iss_position"]["longitude"])

        if MY_LAT-5 <= iss_longitude <= MY_LAT+5 and MY_LONG-5 <= iss_longitude <= MY_LONG+5:
            return True


def is_night():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }
    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

    time_now = datetime.now().hour

    if time_now >= sunset or time_now <= sunrise:
        return True


while True:
    time.sleep(60)
    if iss_is_overhead() and is_night():
                with smtplib.SMTP("smtp.gmail.com") as connection:
                    connection.starttls()
                    connection.login(user=FROM, password=PASSWORD)
                    connection.sendmail(FROM,
                                        TO,
                      msg="Subject:ALert\n\nLook up! The ISS is above you in the sky!")





