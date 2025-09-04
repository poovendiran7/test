# filename: aussie_vs_sa_news_playwright.py
"""
Playwright script (sync API)
- Searches for "Australia vs South Africa cricket latest news" on Bing
- Prints top N search results (title, url, snippet)
- Optionally opens the first result and tries to extract article text
"""
import argparse
import time
from typing import List, Dict, Tuple, Optional

from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError

DEFAULT_QUERY = "Latest cricket news Australia vs South Africa"
DEFAULT_MAX_RESULTS = 5


def extract_article_text_from_page(page) -> str:
    """Try a set of common article selectors and return the first useful text block found."""
    selectors = [
        "article",
        "div[itemprop='articleBody']",
        "div[class*='article']",
        "div[class*='Article']",
        "main",
        "div[class*='content']",
        "div[class*='article-body']",
        "section[class*='article']",
        "div#content",
    ]
    for sel in selectors:
        try:
            elem = page.query_selector(sel)
            if elem:
                txt = elem.inner_text().strip()
                if len(txt) > 200:
                    return txt
        except Exception:
            continue

    # Fallback: gather <p> text on the page (first 40 paragraphs)
    try:
        paragraphs = page.query_selector_all("body p")
        texts = [p.inner_text().strip() for p in paragraphs if p.inner_text().strip()]
        if texts:
            joined = "\n\n".join(texts[:40])
            if len(joined) > 50:
                return joined
    except Exception:
        pass

    return ""


def search_and_get_results(
    query: str,
    max_results: int = DEFAULT_MAX_RESULTS,
    open_first: bool = False,
    browser_name: str = "chromium",
    headless: bool = False,
    slow_mo: int = 0,
) -> Tuple[List[Dict], Optional[str]]:
    """
    Perform a search on Bing and return a list of results.
    If open_first is True, navigate to the first result and attempt to extract article text.
    Returns (results_list, first_article_text_or_None)
    """
    results: List[Dict] = []
    article_text: Optional[str] = None

    with sync_playwright() as p:
        browser = getattr(p, browser_name).launch(headless=headless, slow_mo=slow_mo)
        # Create a context with a typical viewport and a human-like user agent
        context = browser.new_context(
            viewport={"width": 1280, "height": 800},
        )

        # Slight attempt to reduce detection: hide webdriver flag in the page context
        try:
            context.add_init_script(
                "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
            )
        except Exception:
            pass

        page = context.new_page()

        try:
            page.goto("https://www.google.com", timeout=30000)
        except PlaywrightTimeoutError:
            print("Timed out loading Bing. Check your network and try again.")
            browser.close()
            return results, article_text

        # Fill search box and submit
        try:
            search_box = page.query_selector("input[name='q']")
            if not search_box:
                # fallback: go directly to search URL
                page.goto(f"https://www.bing.com/search?q={query.replace(' ', '+')}", timeout=30000)
            else:
                search_box.fill(query)
                search_box.press("Enter")
        except Exception:
            page.goto(f"https://www.bing.com/search?q={query.replace(' ', '+')}", timeout=30000)

        # Wait for results container
        try:
            page.wait_for_selector("li.b_algo", timeout=15000)
        except PlaywrightTimeoutError:
            print("No results selector found on the page; search may have been blocked or layout changed.")
            # Continue to attempt to parse whatever is present

        # Collect result blocks
        try:
            items = page.query_selector_all("li.b_algo")
            for item in items[:max_results]:
                title = ""
                url = ""
                snippet = ""
                try:
                    h2 = item.query_selector("h2")
                    if h2:
                        title = h2.inner_text().strip()
                        a = h2.query_selector("a")
                        if a:
                            url = a.get_attribute("href")
                except Exception:
                    pass
                try:
                    p = item.query_selector("p")
                    if p:
                        snippet = p.inner_text().strip()
                except Exception:
                    pass

                if not title and not url:
                    # Try alternate selectors if Bing layout changed
                    try:
                        a = item.query_selector("a")
                        if a:
                            title = a.inner_text().strip()
                            url = a.get_attribute("href")
                    except Exception:
                        pass

                if title or url:
                    results.append({"title": title, "url": url, "snippet": snippet})
        except Exception as e:
            print("Error extracting search results:", str(e))

        # Print results to console
        if results:
            print(f"\nTop {len(results)} search results for: {query}\n")
            for i, r in enumerate(results, start=1):
                print(f"{i}. {r.get('title') or '(no title)'}")
                print(f"   {r.get('url')}")
                if r.get("snippet"):
                    print(f"   snippet: {r.get('snippet')}")
                print("")
        else:
            print("No search results found.")

        # Optionally open the first result and try to scrape article text
        if open_first and results and results[0].get("url"):
            first_url = results[0]["url"]
            print(f"Opening first result: {first_url}")
            try:
                page.goto(first_url, timeout=30000)
                # small wait for page to settle
                time.sleep(1.0)
            except PlaywrightTimeoutError:
                print("Timeout while opening first result. Continuing to try to extract text.")

            # Try to close cookie banners with common labels (best-effort)
            cookie_labels = ["Accept", "Accept all", "Agree", "I accept", "OK"]
            for label in cookie_labels:
                try:
                    btn = page.query_selector(f"button:has-text('{label}')")
                    if btn:
                        try:
                            btn.click(timeout=2000)
                            time.sleep(0.3)
                            break
                        except Exception:
                            pass
                except Exception:
                    pass

            # Extract article text
            article_text = extract_article_text_from_page(page)
            if article_text:
                print("\nExtracted article text (first ~2000 chars):\n")
                print(article_text[:2000].strip())
                print("\n---\n")
            else:
                print("Could not extract substantive article text from the first result (site layout may vary).")
                       
        # Cleanup
        try:
            context.close()
        except Exception:
            pass
        browser.close()

    return results, article_text


def main():
    parser = argparse.ArgumentParser(description="Search latest news for Australia vs South Africa (Playwright)")
    parser.add_argument("--query", "-q", type=str, default=DEFAULT_QUERY, help="Search query")
    parser.add_argument("--max", "-m", type=int, default=DEFAULT_MAX_RESULTS, help="Max number of search results to print")
    parser.add_argument("--open-first", action="store_true", help="Open the first result and attempt to extract article text")
    parser.add_argument("--browser", choices=["chromium", "firefox", "webkit"], default="chromium", help="Browser engine")
    parser.add_argument("--headless", action="store_true", help="Run in headless mode (no visible browser)")
    parser.add_argument("--slow-mo", type=int, default=0, help="Slows down Playwright operations (ms) to observe actions")

    args = parser.parse_args()
    search_and_get_results(
        query=args.query,
        max_results=args.max,
        open_first=args.open_first,
        browser_name=args.browser,
        headless=args.headless,
        slow_mo=args.slow_mo,
    )


if __name__ == "__main__":
    main()
