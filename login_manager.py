import cloudscraper
import threading
import logging
from config import LOGIN_URL, HEADERS

scraper_lock = threading.Lock()
scraper = None

def get_next_credentials():
    with threading.Lock():
        with open("login.txt", "r") as f:
            lines = [line.strip() for line in f if line.strip()]

        if not lines:
            raise Exception("No credentials left in login.txt")

        cred = lines[0]
        with open("login.txt", "w") as f:
            f.writelines(line + "\n" for line in lines[1:])

        with open("disable_account.txt", "a") as f:
            f.write(cred + "\n")

        return cred

def login():
    global scraper
    while True:
        try:
            username = get_next_credentials()
            payload = {"login": "1", "email": username, "password": username}
            with scraper_lock:
                scraper = cloudscraper.create_scraper()
                res = scraper.post(LOGIN_URL, data=payload, headers=HEADERS)
                return scraper
                # if "logout" in res.text.lower():
                #     logging.info(f"✅ Logged in as {username}")
                #     return scraper
                # else:
                #     logging.warning(f"⚠️ Login failed for {username}")
        except Exception as e:
            logging.error(f"🚫 Error logging in: {e}")
