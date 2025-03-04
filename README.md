# B2B SaaS Scraper and Data Cleaner

This project was originally meant to scrape **all US & Canada B2B SaaS companies** from Harmonic.ai, but because Harmonic.ai was not readily available (no API key or account access), we devised an **alternative** approach using **Google’s Custom Search** (CSE) and standard web scraping with Python. 

## Project Overview

- **Goal**: Gather a large list of B2B SaaS companies (US and Canada), with:
  1. Company Name  
  2. Company LinkedIn URL  
  3. Company Domain  

- **Challenge**: Harmonic.ai access was not available.  
- **Solution**:  
  1. Used Google Custom Search Engine (CSE) to query many keywords relating to “B2B SaaS in the US and Canada.”  
  2. Fetched each result page (HTML or PDF) via Python’s `requests` and `BeautifulSoup`.  
  3. Stored raw data in CSV.  
  4. Cleaned and filtered it with **pandas** (removing duplicates, trimming PDF links if not needed, extracting LinkedIn URLs, etc.).

- **Outcome**: A semi-automated list of leads that includes the data fields required. Additional cleanup or manual review may be necessary, but this approach satisfies the essential deliverable.

## Disclaimer

- **No API Keys in this Repo**: We do **not** include any actual API keys. You will need to supply your own Google Custom Search API key (if you follow the same method) or whichever approach you choose.  
- **Respect TOS**: Large-scale scraping can violate the Terms of Service of certain sites, including Google. The scripts here are for demonstration or small-scale usage. For production, consider official data providers or check the relevant TOS.  

## Installation & Setup

### 1. Clone or Download
Download the scripts (`search_saas.py`, `parse_saas.py`, `cleaned_saas_data.py`, etc.) to your local machine.

### 2. Create & Activate a Conda Environment
```bash
conda create -n b2b_saas_scrape python=3.9 -y
conda activate b2b_saas_scrape

