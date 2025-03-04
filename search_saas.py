import requests
import time
import csv
import urllib.parse

# ---------------------------------------------------------------------
# CONFIGURATION
# ---------------------------------------------------------------------
API_KEY = "AIzaSyAyEjO9UyPXwVvlDrCcDQvQXrXNC0q4GAc"  # Replace with your real API key
CSE_ID = "d0e4bfea251534791"                   # The cx from your custom search engine link

# A large set of keywords to find B2B SaaS directories/lists in US & Canada
QUERY_KEYWORDS = [
    "List of B2B SaaS companies in United States",
    "List of B2B SaaS companies in Canada",
    "Top SaaS companies in North America",
    "Best enterprise SaaS providers in US",
    "Fast-growing B2B SaaS startups Canada",
    "US B2B SaaS directory 2025",
    "Software-as-a-service in Canada B2B directory",
    "Leading B2B SaaS solutions in the USA",
    "SaaS marketplace for US-based software companies",
    "Canadian B2B SaaS industry overview",
    "SaaS product listings North America",
    "B2B SaaS tech companies in USA and Canada",
    "Top 100 B2B SaaS North America",
    "B2B SaaS providers offering cloud software in US Canada",
    "New and emerging B2B SaaS in the United States",
    "Largest B2B SaaS markets US Canada",
    # Add or modify more queries as desired
]

# The Custom Search JSON API can return a maximum of 100 results per query
# in increments of 10. We'll fetch in pages of 10. This example will fetch up to 80 results
# (8 pages * 10 results) per keyword. Adjust as needed, minding your API quotas.
MAX_RESULTS_PER_QUERY = 80

# ---------------------------------------------------------------------
def google_custom_search(query, start_index):
    """
    Make a request to the Google Custom Search JSON API for a given query and start index (1-based).
    Returns JSON if successful, or None on error.
    """
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "key": API_KEY,
        "cx": CSE_ID,
        "q": query,
        "start": start_index
    }
    resp = requests.get(url, params=params)
    if resp.status_code == 200:
        return resp.json()
    else:
        print(f"[ERROR] Status {resp.status_code} - {resp.text}")
        return None

def main():
    all_urls = set()

    # Loop over each query keyword
    for query in QUERY_KEYWORDS:
        print(f"\n[INFO] Searching for: {query}")
        # We'll fetch results in increments of 10 (start=1, 11, 21, ...)
        for start_index in range(1, MAX_RESULTS_PER_QUERY + 1, 10):
            data = google_custom_search(query, start_index)
            if not data or "items" not in data:
                # Possibly no more results, or an error
                break

            for item in data["items"]:
                link = item.get("link")
                if link:
                    all_urls.add(link)

            # Sleep 1 second between requests to help avoid rate-limiting
            time.sleep(1)

    print(f"\n[INFO] Total unique URLs found across queries: {len(all_urls)}")

    # Write to CSV
    out_filename = "candidate_urls.csv"
    with open(out_filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["url"])
        for url in all_urls:
            writer.writerow([url])

    print(f"[INFO] Done! Wrote URLs to {out_filename}")

if __name__ == "__main__":
    main()

