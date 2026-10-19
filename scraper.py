import csv
import json
import time
from pathlib import Path
from collections import Counter
from datetime import datetime, timezone

import requests
import pandas as pd
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
REPORT_DIR = BASE_DIR / "reports"

DATA_DIR.mkdir(exist_ok=True)
REPORT_DIR.mkdir(exist_ok=True)

URL = "https://feeds.bbci.co.uk/news/technology/rss.xml"

HEADERS = {
    "User-Agent": "TechNewsResearchPipeline/1.0 (educational project)"
}


def create_session():
    retry = Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET"],
    )
    session = requests.Session()
    session.headers.update(HEADERS)
    session.mount("https://", HTTPAdapter(max_retries=retry))
    return session


def extract_news(session):
    response = session.get(URL, timeout=20)
    response.raise_for_status()

    soup = BeautifulSoup(response.content, "xml")
    records = []

    for item in soup.find_all("item"):
        title = item.find("title")
        link = item.find("link")
        pub_date = item.find("pubDate")
        description = item.find("description")

        if not title or not link:
            continue

        records.append({
            "title": title.get_text(" ", strip=True),
            "url": link.get_text(strip=True),
            "published_at": (
                pub_date.get_text(strip=True) if pub_date else ""
            ),
            "description": (
                description.get_text(" ", strip=True)
                if description else ""
            ),
            "source": "BBC Technology",
            "scraped_at": datetime.now(timezone.utc).isoformat(),
        })

        time.sleep(0.2)

    # Remove duplicate article URLs
    unique = {}
    for record in records:
        unique[record["url"]] = record

    return list(unique.values())


def save_data(records):
    csv_path = DATA_DIR / "scraped_data.csv"
    json_path = DATA_DIR / "scraped_data.json"

    columns = [
        "title", "url", "published_at",
        "description", "source", "scraped_at"
    ]

    with csv_path.open("w", newline="", encoding="utf-8-sig") as file:
        writer = csv.DictWriter(file, fieldnames=columns)
        writer.writeheader()
        writer.writerows(records)

    with json_path.open("w", encoding="utf-8") as file:
        json.dump(records, file, indent=2, ensure_ascii=False)

    return csv_path


def generate_report(records, csv_path):
    report_path = REPORT_DIR / "summary_report.txt"

    titles = [record["title"] for record in records]
    word_counts = [len(title.split()) for title in titles]

    with report_path.open("w", encoding="utf-8") as file:
        file.write("TECHNOLOGY NEWS ETL REPORT\n")
        file.write("=" * 35 + "\n")
        file.write(f"Generated UTC: {datetime.now(timezone.utc)}\n")
        file.write(f"Source: {URL}\n")
        file.write(f"Total unique articles: {len(records)}\n")
        file.write(f"CSV output: {csv_path}\n")

        if records:
            file.write(
                f"Average title words: "
                f"{sum(word_counts) / len(word_counts):.2f}\n"
            )
            file.write(
                f"Articles with descriptions: "
                f"{sum(bool(r['description']) for r in records)}\n"
            )
            file.write(
                f"Source distribution: "
                f"{dict(Counter(r['source'] for r in records))}\n"
            )
        else:
            file.write("No articles were extracted.\n")

    # Extra analytical summary in the terminal
    if records:
        df = pd.DataFrame(records)
        print("\nDATASET SUMMARY")
        print(df[["title", "url", "published_at"]].head())
        print(f"\nTotal records: {len(df)}")
        print(f"Missing descriptions: {df['description'].eq('').sum()}")

    print(f"\nReport saved to: {report_path}")


def main():
    print("Starting technology news ETL pipeline...")
    session = create_session()

    try:
        records = extract_news(session)
        csv_path = save_data(records)
        generate_report(records, csv_path)
        print(f"\nPipeline completed. Extracted {len(records)} articles.")
    except requests.RequestException as error:
        print(f"Network/request error: {error}")
        raise SystemExit(1)
    except Exception as error:
        print(f"Pipeline error: {error}")
        raise SystemExit(1)
    finally:
        session.close()


if __name__ == "__main__":
    main()