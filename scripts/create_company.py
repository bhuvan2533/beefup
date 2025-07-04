import requests
import time
from dotenv import load_dotenv
import os

load_dotenv(override=True)

BACKEND_URL = os.environ.get("BACKEND_URL")
COMPANY_NAME = os.environ.get("COMPANY_NAME")

for _ in range(30):
    try:
        resp = requests.post(BACKEND_URL, json={"name": COMPANY_NAME})
        if resp.status_code == 200:
            print("Company created:", resp.json())
            break
        else:
            print("Failed, status:", resp.status_code, resp.text)
    except Exception as e:
        print("Waiting for backend...", e)
    time.sleep(2)
else:
    print("Failed to create company after retries.")