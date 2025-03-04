import pandas as pd

def main():
    # 1. Load your CSV (IMPORTANT: change this if your file name differs!)
    try:
        df = pd.read_csv("b2b_saas_companies.csv", encoding="utf-8")
    except FileNotFoundError:
        print("[ERROR] 'b2b_saas_companies.csv' not found in current directory.")
        return

    print("Initial data shape:", df.shape)
    print(df.head())

    # 2. Clean & Filter

    # 2a) Remove rows where SourceURL ends with .pdf (case-insensitive check)
    if 'SourceURL' in df.columns:
        df['SourceURL'] = df['SourceURL'].astype(str)  # ensure it's a string
        pdf_mask = df['SourceURL'].str.lower().str.endswith('.pdf')
        df = df[~pdf_mask]

    # 2b) Drop rows that have neither a PossibleDomain nor LinkedInURL
    # (Only do this if your columns are named 'PossibleDomain' and 'LinkedInURL')
    for col in ['PossibleDomain', 'LinkedInURL']:
        if col not in df.columns:
            df[col] = ''  # Create the column if missing, so dropna won't fail
    df = df.dropna(subset=['PossibleDomain', 'LinkedInURL'], how='all')

    # 2c) Trim whitespace & trailing slashes in domain/linkedin columns
    df['PossibleDomain'] = df['PossibleDomain'].fillna("").str.strip().str.rstrip('/')
    df['LinkedInURL'] = df['LinkedInURL'].fillna("").str.strip().str.rstrip('/')

    # 2d) Truncate ExtractedText to 500 chars (if 'ExtractedText' exists)
    if 'ExtractedText' in df.columns:
        df['ExtractedText'] = df['ExtractedText'].astype(str).apply(lambda x: x[:500])

    # 2e) Deduplicate by LinkedInURL (or Domain) — keep first occurrence
    df = df.drop_duplicates(subset=['LinkedInURL'], keep='first')

    # 2f) (Optional) Filter rows to ensure mention of "b2b" or "saas" if you like:
    # Only if ExtractedText column exists
    if 'ExtractedText' in df.columns:
        keywords = ["b2b", "saas", "software-as-a-service"]
        def has_keywords(text):
            text_lower = text.lower()
            return any(k in text_lower for k in keywords)
        df = df[df['ExtractedText'].apply(has_keywords)]

    print("Cleaned data shape:", df.shape)

    # 3. Save the cleaned data
    df.to_csv("cleaned_saas_data.csv", index=False, encoding="utf-8")
    print("Cleaned data saved to 'cleaned_saas_data.csv'")

if __name__ == "__main__":
    main()
