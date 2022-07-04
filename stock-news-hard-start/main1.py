
import smtplib
import html

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_API_KEY = "G7A55D2WJ7K3FP12"
NEWS_API_KEY = "0650cce1fd7d4f95a39f82d38661f625"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

import requests


## STEP 1: Use https://newsapi.org/docs/endpoints/everything
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").
#HINT 1: Get the closing price for yesterday and the day before yesterday. Find the positive difference between the two prices. e.g. 40 - 20 = -20, but the positive difference is 20.

#HINT 2: Work out the value of 5% of yerstday's closing stock price.
stock_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": STOCK_API_KEY,

}

response = requests.get(STOCK_ENDPOINT, params=stock_params)
data = response.json()['Time Series (Daily)']

data_list = [value for (key, value) in data.items()]

yesterday_data = data_list[0]
yesterday_closing_price = yesterday_data["4. close"]
day_before_yesterday_data = data_list[1]
day_before_yesterday_closing_price = day_before_yesterday_data["4. close"]

difference = float(yesterday_closing_price) - float(day_before_yesterday_closing_price)

up_down = None

if difference > 0:
        up_down = "🔺"
else:
        up_down = "🔻"

diff_percent = round(( difference / float(yesterday_closing_price)) * 100)

## STEP 2: Use https://newsapi.org/docs/endpoints/everything
# Instead of printing ("Get News"), actually fetch the first 3 articles for the COMPANY_NAME. 
#HINT 1: Think about using the Python Slice Operator
news_params = {
    "qInTitle": COMPANY_NAME,
    'apikey': NEWS_API_KEY,
}
response_news = requests.get(NEWS_ENDPOINT, params=news_params)
news_data = response_news.json()

articles = news_data['articles']
three_articles = articles[:3]



## STEP 3: Use twilio.com/docs/sms/quickstart/python
# Send a separate message with each article's title and description to your phone number. 
#HINT 1: Consider using a List Comprehension.
formatted_articles = [
 f"{STOCK}: {up_down}{diff_percent}%\nHeadline: {article['title']}. \nBrief: {article['description']}" for article in three_articles]


for article in formatted_articles:
    """
     with smtplib.SMTP("smtp.gmail.com") as connection:
        SEND_TO = 'klamchukmoney@gmail.com'
        FROM = 'vladklimchukit@gmail.com'
        PASSWORD = 'muxtar17'
        connection.starttls()

        connection.login(FROM, PASSWORD)

        connection.sendmail(from_addr=FROM,
                            to_addrs=SEND_TO,
                            msg=article
    )
    """

    print(article)




