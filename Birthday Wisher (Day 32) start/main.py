import random
import smtplib
import datetime as dt

MY_EMAIL = "vladklimchukit@gmail.com"
PASSWORD = "muxtar17"
TO = "klamchukmoney@gmail.com"

now = dt.datetime.now()
weakday = now.weekday()

if weakday == 1:
    with open("quotes.txt") as quote_file:
        all_quotes = quote_file.readlines()
        quote = random.choice(all_quotes)
    print(quote)

    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(MY_EMAIL, PASSWORD)
        connection.sendmail(from_addr=MY_EMAIL,
                            to_addrs=TO,
                            msg=f"Subject:Monday Motivation\n\n{quote}")