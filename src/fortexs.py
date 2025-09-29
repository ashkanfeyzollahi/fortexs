"""
A web scraper for fetching products from `www.fortex.ir`
"""

import json
import re
import time

import requests
import tqdm
from parsel import Selector
from requests.adapters import HTTPAdapter, Retry


retry_strategy = Retry(total=5)
adapter = HTTPAdapter(max_retries=retry_strategy)
http = requests.Session()
http.mount("https://", adapter)
http.mount("http://", adapter)


def fortex_scrape_many(pages: range) -> list[dict[str, bool | int | None | str]]:
    """Scrape `www.fortex.ir` products from a range of pages

    Args:
        pages (range): A range of integers indicating which pages to scrape products from

    Returns:
        list[dict[str, bool | int | str]]: A list of products
    """

    products: list[dict[str, bool | int | None | str]] = []

    for page in tqdm.tqdm(pages, desc="Scraping products from `www.fortex.ir`"):
        try:
            products.extend(fortex_scrape_one(page))
        except:
            print(f"Couldn't scrap the products from the page {page}")
        time.sleep(0.1)

    return products


def fortex_scrape_one(page: int) -> list[dict[str, bool | int | None | str]]:
    """Scrape `www.fortex.ir` products from one page

    Args:
        page (int): Which page to scrape products from

    Returns:
        list[dict[str, bool | int | str]]: A list of products
    """

    products: list[dict[str, bool | int | None | str]] = []

    url = f"https://www.fortex.ir/search?search=%20&description=true&page={page}"
    response = http.get(url, timeout=10)

    selector = Selector(text=response.text)

    for sub_selector in selector.css("div.product-thumb"):
        products.append({
            "name": sub_selector.css("h3 a::attr(data-original-title)").get(),
            "image_url": sub_selector.css("a img::attr(src)").get(),
            "available": not bool(sub_selector.css("div.caption p")),
            "url": sub_selector.css("h3 a::attr(href)").get(),
            "page": page,
            "page_url": url,
        })

    return products


def fortex_get_last_page_url() -> str | None:
    """Get last page url

    Returns:
        str | None: An url to the last page or None
    """

    url = f"https://www.fortex.ir/search?search=%20&description=true&page=1"
    response = requests.get(url, timeout=10)

    selector = Selector(text=response.text)

    return selector.css("ul.pagination > li:nth-child(11) > a:nth-child(1)::attr(href)").get()


def fortex_get_page_count() -> int:
    """Get count of pages

    Raises:
        Exception: If couldn't get last page url or didn't match any numbers using regex
            from the last page url

    Returns:
        int: Count of pages
    """

    last_page_url = fortex_get_last_page_url()

    if last_page_url is None:
        raise Exception()

    match = re.search(r"page=(\d+)", last_page_url)

    if match is None:
        raise Exception()

    return int(match.group(1))


if __name__ == "__main__":
    with open("fortexs.json", "w") as f:
        json.dump(fortex_scrape_many(range(1, fortex_get_page_count() + 1)), f)
    print("Done!")
