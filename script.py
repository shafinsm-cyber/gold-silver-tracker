import requests
import smtplib
import os
from email.mime.text import MIMEText

# --- GET DATA ---
API_KEY = os.environ.get("GOLD_API_KEY")

headers = {"x-access-token": API_KEY}

gold = requests.get("https://www.goldapi.io/api/XAU/INR", headers=headers).json()
silver = requests.get("https://www.goldapi.io/api/XAG/INR", headers=headers).json()

gold_price = gold.get("price", 0)
silver_price = silver.get("price", 0)

ratio = gold_price / silver_price if silver_price else 0
silver_percent = (silver_price / gold_price) * 100 if gold_price else 0

# --- EMAIL ---
subject = "Daily Gold & Silver Update"
message = f"""
Gold: ₹{gold_price}
Silver: ₹{silver_price}

Gold/Silver Ratio: {ratio:.2f}

Gold is ~{ratio:.0f}x costlier than silver
Silver is ~{silver_percent:.2f}% the price of gold
"""

sender = "shafinsm@gmail.com"
receiver = "asifisa57@gmail.com"
password = os.environ.get("EMAIL_PASS")

msg = MIMEText(message)
msg["Subject"] = subject
msg["From"] = sender
msg["To"] = receiver

with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
    server.login(sender, password)
    server.send_message(msg)
