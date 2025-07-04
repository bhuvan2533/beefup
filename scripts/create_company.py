import requests
import time
from dotenv import load_dotenv
import os

load_dotenv(override=True)

BACKEND_URL = os.environ.get("BACKEND_URL")
COMPANY_NAME = os.environ.get("COMPANY_NAME")

for _ in range(30):
    try:
        check_resp = requests.get(BACKEND_URL + f"/{COMPANY_NAME}")
        if check_resp.status_code == 404:
            print("Company does not exist, creating...")
            create_resp = requests.post(BACKEND_URL, json={"name": COMPANY_NAME})
            if create_resp.status_code == 200:
                print("Company created:", create_resp.json())
                break
            else:
                print("Failed, status:", create_resp.json())
        elif check_resp.status_code == 200:
            print("Company already exists:", check_resp.json())
            break
        else:
            print("Failed, status:", check_resp.json())
    except Exception as e:
        print("Waiting for backend...", e)
    time.sleep(5)
else:
    print("Failed to create company after retries.")