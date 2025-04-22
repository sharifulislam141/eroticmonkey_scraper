import csv
import os

def load_remaining_urls():
    with open("profile.txt", "r", encoding="utf-8") as f:
        urls = [line.strip() for line in f if line.strip()]

    existing = set()
    if os.path.exists("results.csv"):
        with open("results.csv", "r", encoding="utf-8") as f:
            for row in csv.reader(f):
                if row and row[0] != "url":
                    existing.add(row[0])

    return [url for url in urls if url not in existing]

def init_csv():
    if not os.path.exists("results.csv") or os.stat("results.csv").st_size == 0:
        with open("results.csv", "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["url", "phone", "email"])

def write_result(url, phone, email):
    with open("results.csv", "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([url, phone, email])

def write_failed(url):
    with open("failed.txt", "a", encoding="utf-8") as f:
        f.write(url + "\n")
