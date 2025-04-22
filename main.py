import logging
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm
from scraper import scrape_profile
from utils import load_remaining_urls, init_csv
from config import THREADS

# Setup logging
logging.basicConfig(
    filename="logs/scraper.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

if __name__ == "__main__":
    init_csv()
    urls = load_remaining_urls()
    progress = tqdm(total=len(urls), desc="Scraping", ncols=80)

    def worker(url):
        scrape_profile(url)
        progress.update(1)

    with ThreadPoolExecutor(max_workers=THREADS) as executor:
        executor.map(worker, urls)

    progress.close()
    logging.info("✅ Scraping finished")
