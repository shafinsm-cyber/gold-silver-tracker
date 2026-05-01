import requests
import smtplib
from email.mime.text import MIMEText

# --- GET DATA ---
API_KEY = "demo"

headers = {"x-access-token": API_KEY}

gold = requests.get("https://www.goldapi.io/api/XAU/INR", headers=headers).json()
silver = requests.get("https://www.goldapi.io/api/XAG/INR", headers=headers).json()

gold_price = gold.get("price", 0)
silver_price = silver.get("price", 0)

ratio = gold_price / silver_price if silver_price else 0

# --- EMAIL ---
subject = "Daily Gold & Silver Update"
body = f"""
Gold: ₹{gold_price}
Silver: ₹{silver_price}
Ratio: {ratio:.2f}
"""

sender = "your_email@gmail.com"
receiver = "your_email@gmail.com"
password = "your_app_password"

msg = MIMEText(body)
msg["Subject"] = subject
msg["From"] = sender
msg["To"] = receiver

with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
    server.login(sender, password)
    server.send_message(msg)
