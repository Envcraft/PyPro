"""Web Scraper — implement your solution here."""

# TODO: Implement the web scraper.
#
# LEGAL: Only scrape public sites that permit scraping.
# Always add a delay between requests.
#
# This project requires httpx. Install it with:
#   uv add httpx
#
# Suggested structure:
#   def fetch_page(url: str, delay: float = 1.0) -> str | None: ...
#   def parse_page(html: str) -> list[dict]: ...
#   def deduplicate(records: list[dict], key: str) -> list[dict]: ...
#   def save_csv(records: list[dict], filepath: Path) -> None: ...
#   def save_sqlite(records: list[dict], filepath: Path) -> None: ...
#   def scrape(urls: list[str], output: Path, delay: float = 1.0) -> None: ...
#   def main() -> None: ...


def main() -> None:
    raise NotImplementedError("Implement the main() function.")


if __name__ == "__main__":
    main()
