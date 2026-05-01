import requests
import smtplib
import os
from email.mime.text import MIMEText

# --- GET DATA ---
API_KEY = os.environ.get("GOLD_API_KEY")
print("API_KEY:", API_KEY)

headers = {"x-access-token": API_KEY}

gold = requests.get(
    "https://www.goldapi.io/api/XAU/INR",
    headers=headers,
    timeout=10
).json()

silver = requests.get(
    "https://www.goldapi.io/api/XAG/INR",
    headers=headers,
    timeout=10
).json()

# --- DEBUG ---
print("GOLD RESPONSE:", gold)
print("SILVER RESPONSE:", silver)

# --- SAFE PRICE EXTRACTION ---
def get_price(data):
    return (
        data.get("price_gram_24k") or
        data.get("price_gram_22k") or
        data.get("price") or
        0
    )

gold_price = get_price(gold)
silver_price = get_price(silver)

# --- CALCULATIONS (UPDATED) ---
# Silver → Gold ratio (your requested version)
ratio = silver_price / gold_price if gold_price else 0

silver_percent = (silver_price / gold_price) * 100 if gold_price else 0

# --- EMAIL CONTENT ---
if gold_price == 0 or silver_price == 0:
    message = "⚠️ Error fetching gold/silver prices. Check API response."
else:
    message = f"""
Gold: ₹{gold_price:,.2f}
Silver: ₹{silver_price:,.2f}

Silver/Gold Ratio: {ratio:.6f}

Silver is ~{silver_percent:.2f}% the price of gold
(OR) 1 unit of silver ≈ {ratio:.6f} units of gold
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
