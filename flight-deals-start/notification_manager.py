from flight_search import FlightSearch
import smtplib

# Auth email
USERNAME = 'klamchukmoney@gmail.com'
PASSWORD = 'muxtar15'
SEND_TO = 'vladklimchukit@gmail.com'
MAIL_PROVIDER_SMTP_ADDRESS = "smtp.gmail.com"

flight = FlightSearch()


class NotificationManager:

    def send_emails(self, emails, message, google_flight_link):
        with smtplib.SMTP(MAIL_PROVIDER_SMTP_ADDRESS) as connection:
            connection.starttls()
            connection.login(USERNAME, PASSWORD)
            for email in emails:
                connection.sendmail(
                    from_addr=USERNAME,
                    to_addrs=email,
                    msg=f"Subject:New Low Price Flight!\n\n{message}\n{google_flight_link}".encode('utf-8')
                )

