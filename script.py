import requests
from companies import big_list
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor


KEYWORDS = ["entry level", "new grad", "junior", "software engineer"]

COMPANIES = big_list()

def check_company(company):
    """Fetch and search a company's Ashby job board for entry-level SWE roles."""
    url = f"https://jobs.ashbyhq.com/{company}"
    try:
        r = requests.get(url, timeout=6)
        if r.status_code != 200:
            return None

        text = r.text.lower()
        matches = [kw for kw in KEYWORDS if kw in text]
        if matches:
            soup = BeautifulSoup(r.text, "html.parser")
            titles = [t.get_text(strip=True) for t in soup.find_all("a") if "software" in t.get_text().lower()]
            return {
                "company": company,
                "url": url,
                "keywords": matches,
                "titles": titles[:5]  # show first few job titles
            }
    except Exception:
        pass
    return None

def main():
    print("Searching Ashby job boards for entry-level SWE jobs...\n")

    results = []
    with ThreadPoolExecutor(max_workers=15) as executor:
        for res in executor.map(check_company, COMPANIES):
            if res:
                results.append(res)

    if not results:
        print("No matches found. Try adding more companies or keywords.")
        return

    for job in results:
        print(f"✅ {job['company'].title()} — {job['url']}")
        print(f"   Keywords matched: {', '.join(job['keywords'])}")
        for t in job['titles']:
            print(f"   • {t}")
        print()

    print(f"Found {len(results)} companies with entry-level SWE roles!")

if __name__ == "__main__":
    main()
