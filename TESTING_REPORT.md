# Testing Report

## Project
Automated Web Scraping & Data Extraction Pipeline

## Testing Approach
Automated unit tests were implemented using Python's unittest framework and mocked HTTP responses. This allows extraction logic to be tested without depending on a live website.

## Test Cases

| Test | Purpose | Expected Result |
|---|---|---|
| Article extraction | Verify title, URL, publication date, description, and source fields | Pass |
| Duplicate removal | Ensure repeated article URLs are deduplicated | Pass |
| Optional fields | Verify missing publication dates and descriptions use empty strings | Pass |

## Test Execution

Command:

```bash
python -m unittest discover -s tests -v
```

Result: 3 tests passed.

## Integration Verification
A live execution of the pipeline successfully extracted 21 unique technology news articles during the initial run. The CSV, JSON, and summary report files were generated.

## Conclusion
The initial unit tests and live execution confirmed that the core extraction and deduplication workflow functions as expected. Network failures and changes in the source feed may affect future runs.