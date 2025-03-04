import time
import csv
import requests
from bs4 import BeautifulSoup

def parse_urls_for_saas(csv_input="candidate_urls.csv", csv_output="b2b_saas_companies.csv"):
    """
    Reads candidate URLs from CSV, attempts to parse each for references to B2B SaaS data:
      - Company Names
      - Domains
      - LinkedIn URLs
    This is a naive approach. Real sites often require custom logic & selectors.
    """
    with open(csv_input, "r", encoding="utf-8") as infile, \
         open(csv_output, "w", newline="", encoding="utf-8") as outfile:

        reader = csv.DictReader(infile)
        fieldnames = ["SourceURL", "ExtractedText", "PossibleDomain", "LinkedInURL"]
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()

        for row in reader:
            url = row["url"]
            print(f"[INFO] Parsing: {url}")
            try:
                resp = requests.get(url, timeout=10)
                if resp.status_code == 200:
                    soup = BeautifulSoup(resp.text, "html.parser")

                    # This is a super simplistic approach:
                    # 1) Extract all text
                    page_text = soup.get_text(separator="\n")

                    # 2) Look for patterns or direct links
                    all_links = soup.find_all("a", href=True)
                    possible_domain = ""
                    linkedin_url = ""
                    for link in all_links:
                        href = link["href"]
                        if "linkedin.com" in href:
                            linkedin_url = href
                        elif href.startswith("http"):
                            # Could be the company's website
                            # Heuristic: if "company" or "saas" in link text, we guess it's relevant
                            link_text = (link.get_text() or "").lower()
                            if "company" in link_text or "saas" in link_text:
                                possible_domain = href

                    writer.writerow({
                        "SourceURL": url,
                        "ExtractedText": page_text[:500],  # store partial text for debug
                        "PossibleDomain": possible_domain,
                        "LinkedInURL": linkedin_url,
                    })
                else:
                    print(f"[WARN] Status {resp.status_code} for {url}")
            except Exception as e:
                print(f"[ERROR] {url} - {e}")

            time.sleep(0.5)  # slight delay to be polite

if __name__ == "__main__":
    parse_urls_for_saas()

