import requests
import smtplib
import os
from email.mime.text import MIMEText
print("API_KEY:", API_KEY)
# --- GET DATA ---
API_KEY = os.environ.get("GOLD_API_KEY")

headers = {"x-access-token": API_KEY}

gold = requests.get("https://www.goldapi.io/api/XAU/INR", headers=headers, timeout=10).json()
silver = requests.get("https://www.goldapi.io/api/XAG/INR", headers=headers, timeout=10).json()

gold_price = gold.get("price", 0)
silver_price = silver.get("price", 0)

# --- CALCULATIONS ---
ratio = gold_price / silver_price if silver_price else 0
silver_percent = (silver_price / gold_price) * 100 if gold_price else 0

# --- EMAIL CONTENT ---
if gold_price == 0 or silver_price == 0:
    message = "⚠️ Error fetching gold/silver prices. Please check API."
else:
    message = f"""
Gold: ₹{gold_price:,.2f}
Silver: ₹{silver_price:,.2f}

Gold/Silver Ratio: {ratio:.2f}

Gold is ~{ratio:.0f}x costlier than silver
Silver is ~{silver_percent:.2f}% the price of gold
"""

subject = "Daily Gold & Silver Update"

# --- EMAIL ---
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
