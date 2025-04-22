import re
import logging
from login_manager import login
from config import HEADERS
from utils import write_result, write_failed

scraper = login()

def scrape_profile(url):
    global scraper
    for attempt in range(3):  # Retry limit
        try:
            html = scraper.get(url).text
            escort_id = re.search(r"CONFIG\.escortId\s*=\s*'(\d+)'", html).group(1)
            geci_token = re.search(r"CONFIG\.geciToken\s*=\s*'([^']+)'", html).group(1)

            base_headers = {
                **HEADERS,
                "X-Geci-Token": geci_token,
                "Origin": "https://www.eroticmonkey.ch"
            }

            def get_info(info_type):
                res = scraper.post(
                    "https://www.eroticmonkey.ch/controller/ajax/get_escort_contact_info.php",
                    headers=base_headers,
                    data={"id": escort_id, "type": info_type}
                )
                data = res.json()
                return data["DATA"]["result"] if data["STATUS"] == "success" else "N/A"

            email = get_info("email")
            phone = get_info("phone")

            logging.info(f"✅ Scraped: {url} | 📧 {email} | 📞 {phone}")
            write_result(url, phone, email)
            return True

        except Exception as e:
            logging.warning(f"❌ Attempt {attempt+1}/3 failed for {url}: {e}")
            if attempt == 2:
                write_failed(url)
                logging.error(f"🛑 Failed scraping {url} after 3 attempts")
                scraper = login()  # Switch account
