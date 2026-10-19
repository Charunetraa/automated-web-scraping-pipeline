# Automated Web Scraping & Data Extraction Pipeline

## Overview
A Python-based ETL pipeline that extracts technology news from a public BBC RSS feed, transforms the data into structured records, and generates datasets and analytical reports.

## Features
- Extracts technology news using Requests.
- Parses XML content using BeautifulSoup and lxml.
- Uses custom HTTP headers and request timeouts.
- Implements automatic retries for temporary HTTP failures.
- Removes duplicate article URLs.
- Exports structured CSV and JSON datasets.
- Generates automated summary statistics.
- Handles request and pipeline errors.
- Organizes outputs into dedicated data and reports folders.

## Technology Stack
- Python
- Requests
- BeautifulSoup4
- lxml
- Pandas

## Project Structure
```text
automated-web-scraping-pipeline/
├── scraper.py
├── requirements.txt
├── README.md
├── .gitignore
├── data/
│   ├── scraped_data.csv
│   └── scraped_data.json
└── reports/
    └── summary_report.txt
```

## Installation

Clone the repository and enter the project directory.

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

## Run the Pipeline

```bash
python scraper.py
```

The script retrieves available technology news articles and generates:
- `data/scraped_data.csv`
- `data/scraped_data.json`
- `reports/summary_report.txt`

## Dataset Fields
- `title`: Article title
- `url`: Article URL
- `published_at`: Publication date when available
- `description`: Article description
- `source`: News source
- `scraped_at`: UTC extraction timestamp

## Sample Execution
The initial successful run extracted 21 unique article records, with zero missing descriptions.

The output count may vary depending on the live feed.

## Responsible Scraping
This project uses a public RSS feed, a descriptive User-Agent, request timeouts, retry handling, and a small delay between parsed records. Always respect the source's terms and access policies.

## Limitations
The pipeline depends on network availability and the source's feed structure. A successful request does not guarantee that the same number of articles will be returned on every run.

## Future Improvements
- Automated scheduled execution
- Unit tests
- Structured logging
- Data quality validation
- Historical dataset comparisons

## License
For educational use. Check the source website's terms before redistributing extracted content.