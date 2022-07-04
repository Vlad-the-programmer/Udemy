
import smtplib
import pandas
from datetime import datetime
import random

MY_EMAIL = "vladklimchukit@gmail.com"
PASSWORD = "muxtar17"

today = datetime.now()

today_tuple = (today.month, today.day)

data = pandas.read_csv("birthdays.csv")
print(data)
birthday_dict = {(data_row["month"], data_row["day"]): data_row for (index, data_row) in data.iterrows()}
if today_tuple in birthday_dict:
    birthday_person = birthday_dict[today_tuple]
    file_path = f"letter_templates/letter_{random.randint(1,3)}.txt"
    with open(file_path) as letter_file:
        contents = letter_file.read()
        contents = contents.replace("[NAME]", birthday_person["name"])
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(MY_EMAIL, PASSWORD)
        connection.sendmail(from_addr=MY_EMAIL,
                            to_addrs=birthday_person["email"],
                            msg=f"Subject:Happy Birthday\n\n{contents}")


















# letters = ["letter_1.txt", "letter_2.txt", "letter_3.txt"]
# birthdays = [["Lesya", 1979, 8, 21], ["Markian", 2008, 4, 14], ["Vlad", 2004, 4, 1], ["Daniel", 2004, 4, 1]]
# with open("birthdays.csv") as data:
#     for birthday_data in birthdays:
#         data.writelines(birthday_data)
#         today = datetime.now()
#
#         for birthday in birthdays:
#             if today.day and today.month in birthday:
#                 letter = random.choice(letters)
#                 with open(letter) as letter_to_send:
#                     name_place = letter.find("[Name]")
#                     letter_to_send.write(birthday[0])



