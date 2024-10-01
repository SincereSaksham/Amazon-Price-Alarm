import os
from bs4 import BeautifulSoup
import requests
import smtplib
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get environment variables
EMAIL = os.getenv("EMAIL_ADDRESS").strip()
PASSWORD = os.getenv("EMAIL_PASSWORD").strip()
SMTP_ADD = "smtp.gmail.com"  # Hardcoded for testing

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 OPR/112.0.0.0",
    "Accept-Language": "en-US,en;q=0.9",
}

response = requests.get(
    "https://www.amazon.in/Pixel-Stromy-Black-128GB-Storage/dp/B0DCC2RXF9/ref=sr_1_1?crid=2QGBWR4G7850O&dib=eyJ2IjoiMSJ9.faFF7-w-0U1b75Qk7lOlKTQREdWer-p6z2JluqIF10s-iaGDYsPNSEcy3XT9-8DCNoFQB1FNOkS-JdQtP1nu-8TbRhHm35WPkTzh0_luXxLLrvCekeJDQJyqH5HPHhkEZ2c5HdoBYK4rUQvSwHuRoiJS0mcJybLbhX2OTvIv8LmLB1dqFYZVrQX2ixhKYZZI3CXtp0mBi7KBh5oleY1Id6Mc_CryLv9Ym-PJnJ3oT5w.td9H4ARE-8rHPLGJI9-SIcgIlRXQP70jNlcf-MAj7Mk&dib_tag=se&keywords=google+pixel&qid=1724524277&sprefix=%2Caps%2C223&sr=8-1",
    headers=HEADERS)

response_html = response.text
soup = BeautifulSoup(response_html, "html.parser")

price: str = ""

price_data = soup.select(selector=".aok-offscreen")[0].getText().strip().split(" ")[0].split("₹")[1]
price_list = price_data.split(",")
for pric in price_list:
    price = price + pric

final_price = float(price)



target = 38000.0

# Send email if price is below target
if final_price < target:
    message = "The price is below target, buy quick"
    try:
        connection = smtplib.SMTP(SMTP_ADD, port=587)
        connection.starttls()
        connection.login(user=EMAIL, password=PASSWORD)
        connection.sendmail(EMAIL, "recepient mail", message)
        connection.quit()
        print("Email sent successfully!")
    except smtplib.SMTPAuthenticationError as e:
        print(f"SMTP Authentication Error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
