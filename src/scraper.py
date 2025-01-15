import requests
from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import urljoin

def fetch_page_content(url):
    """
    Fetch the HTML content of a given URL.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"[WARNING] Failed to fetch {url}: {e}")
        return None

def extract_links(base_url, html_content):
    """
    Extract valid links from HTML content, treating main and subdomains as the same domain.
    """
    from tldextract import extract

    def get_root_domain(url):
        # Extract the root domain (e.g., "cfd.direct")
        extracted = extract(url)
        return f"{extracted.domain}.{extracted.suffix}"

    base_root_domain = get_root_domain(base_url)
    soup = BeautifulSoup(html_content, 'html.parser')
    links = set()

    for a_tag in soup.find_all('a', href=True):
        full_url = urljoin(base_url, a_tag['href'])
        link_root_domain = get_root_domain(full_url)

        # Only add links with the same root domain
        if link_root_domain == base_root_domain:
            # Normalize the URL (remove query strings and fragments)
            normalized_url = full_url.split("#")[0].split("?")[0]
            links.add(normalized_url)

    return links

def scrape_page(url, html_content):
    """
    Scrape headers and their associated paragraphs from a given page's HTML content.
    Handles headers with links (<a>) inside them.
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    qa_pairs = []

    # Find all header tags (h1, h2, h3, etc.)
    headers = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])

    for header in headers:
        # Extract the header text, including handling links inside headers
        link = header.find('a')
        if link:
            question = link.get_text(strip=True)  # Extract text from <a>
        else:
            question = header.get_text(strip=True)  # Extract text from the header

        # Collect all paragraphs until the next header
        answer = []
        next_sibling = header.find_next_sibling()
        while next_sibling:
            if next_sibling.name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
                break  # Stop when another header is encountered
            if next_sibling.name == 'p':  # Append paragraph content
                answer.append(next_sibling.get_text(strip=True))
            next_sibling = next_sibling.find_next_sibling()

        # Join paragraphs into a single answer
        answer_text = "\n".join(answer)

        # Only add pairs with non-empty question and answer
        if question and answer_text:
            qa_pairs.append({'url': url, 'question': question, 'answer': answer_text})

    return qa_pairs

def crawl_and_scrape(start_url, max_pages, max_depth=3):
    """
    Crawl and scrape content starting from a given URL with depth restriction.
    Each Q&A pair includes the source URL.
    """
    visited = set()
    to_visit = [(start_url, 0)]  # Queue of (URL, depth)
    data = []
    total_pages = max_pages
    current_count = 0

    while to_visit and len(visited) < total_pages:
        current_url, depth = to_visit.pop(0)  # FIFO for breadth-first crawling
        if current_url in visited or depth > max_depth:
            continue

        print(f"[SCRAPING] ({current_count + 1}/{total_pages}) Depth: {depth}, URL: {current_url}")

        # Fetch the page content
        html_content = fetch_page_content(current_url)
        if not html_content:
            print(f"[WARNING] Failed to fetch content for: {current_url}")
            continue

        # Scrape headers and paragraphs
        page_data = scrape_page(current_url, html_content)
        if page_data:
            data.extend(page_data)  # Append all Q&A pairs
            print(f"[SUCCESS] Scraped {len(page_data)} Q&A pairs from: {current_url}")
        else:
            print(f"[WARNING] No Q&A data found on: {current_url}")

        visited.add(current_url)

        # Extract new links
        new_links = extract_links(start_url, html_content)
        for link in new_links - visited:
            to_visit.append((link, depth + 1))

        # Update progress
        current_count += 1
        print(f"[INFO] Found {len(new_links)} new links. Progress: {current_count}/{total_pages}")

    return pd.DataFrame(data)

def main():
    import argparse
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Web scraping tool for crawling and extracting content.")
    parser.add_argument("start_url", type=str, help="The starting URL for crawling.")
    parser.add_argument("output_path", type=str, help="Path to save the output CSV file.")
    parser.add_argument("--max_pages", type=int, default=100, help="Maximum number of pages to scrape (default: 100).")
    parser.add_argument("--max_depth", type=int, default=3, help="Maximum depth for crawling (default: 3).")
    args = parser.parse_args()

    # Start crawling
    print(f"[INFO] Starting crawl from: {args.start_url}")
    scraped_data = crawl_and_scrape(args.start_url, args.max_pages, args.max_depth)
    scraped_data.to_csv(args.output_path, index=False)
    print(f"[INFO] Scraping completed. Data saved to {args.output_path}.")

if __name__ == "__main__":
    main()
