"""
Web scraper for sierra.ai website
Crawls the site and extracts text content for RAG ingestion
"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time
import json
from pathlib import Path
from typing import Set, List, Dict


class SierraScraper:
    def __init__(self, base_url: str = "https://sierra.ai", max_pages: int = 50):
        self.base_url = base_url
        self.max_pages = max_pages
        self.visited_urls: Set[str] = set()
        self.scraped_content: List[Dict[str, str]] = []
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })

    def is_valid_url(self, url: str) -> bool:
        # Check if URL belongs to sierra.ai domain
        parsed = urlparse(url)
        return parsed.netloc == 'sierra.ai' or parsed.netloc == 'www.sierra.ai'

    def clean_text(self, soup: BeautifulSoup) -> str:
        # Remove script and style elements
        for script in soup(["script", "style", "nav", "footer", "header"]):
            script.decompose()

        text = soup.get_text(separator='\n')

        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = '\n'.join(chunk for chunk in chunks if chunk)

        return text

    def scrape_page(self, url: str) -> tuple[str, List[str]]:
        try:
            print(f"  Scraping: {url}")
            response = self.session.get(url, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'lxml')

            # Extract title
            title = soup.find('title')
            title_text = title.get_text() if title else url

            # Extract main content
            content = self.clean_text(soup)

            # Store content
            if content and len(content) > 100:  # Only store if meaningful content
                self.scraped_content.append({
                    'url': url,
                    'title': title_text,
                    'content': content
                })

            # Extract links
            links = []
            for link in soup.find_all('a', href=True):
                absolute_url = urljoin(url, link['href'])
                clean_url = absolute_url.split('#')[0].split('?')[0]
                if self.is_valid_url(clean_url):
                    links.append(clean_url)

            return content, links

        except Exception as e:
            print(f"Error scraping {url}: {e}")
            return "", []

    def crawl(self):
        print(f"Starting crawl of {self.base_url}")
        print(f"Max pages: {self.max_pages}\n")

        to_visit = [self.base_url]

        while to_visit and len(self.visited_urls) < self.max_pages:
            url = to_visit.pop(0)

            if url in self.visited_urls:
                continue

            self.visited_urls.add(url)
            content, links = self.scrape_page(url)

            # Add new links to queue
            for link in links:
                if link not in self.visited_urls and link not in to_visit:
                    to_visit.append(link)

            # Be respectful - rate limit
            time.sleep(1)

        print(f"\nCrawled {len(self.visited_urls)} pages")
        print(f"Extracted {len(self.scraped_content)} documents with content\n")

    def save_to_file(self, filepath: str = "data/scraped_content.json"):
        Path(filepath).parent.mkdir(parents=True, exist_ok=True)

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.scraped_content, f, indent=2, ensure_ascii=False)

        print(f"Saved scraped content to {filepath}")

    def load_from_file(self, filepath: str = "data/scraped_content.json") -> List[Dict[str, str]]:
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                self.scraped_content = json.load(f)
            print(f"Loaded {len(self.scraped_content)} documents from {filepath}")
            return self.scraped_content
        except FileNotFoundError:
            print(f"No cached content found at {filepath}")
            return []


def main():
    scraper = SierraScraper(max_pages=30)
    scraper.crawl()
    scraper.save_to_file()

    print(f"\n Summary:")
    print(f"Total pages visited: {len(scraper.visited_urls)}")
    print(f"Documents with content: {len(scraper.scraped_content)}")
    


if __name__ == "__main__":
    main()
