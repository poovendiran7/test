"""
Playwright Script: Extract metadata from facebook.com
"""

import asyncio
import json
from playwright.async_api import async_playwright


async def safe_get_attribute(page, selector, attr, timeout=2000):
    """Safely get an attribute from a meta tag if it exists."""
    locator = page.locator(selector)
    try:
        count = await locator.count()
        if count > 0:
            return await locator.first.get_attribute(attr, timeout=timeout)
    except Exception:
        return None
    return None


async def run():
    async with async_playwright() as p:
        # Launch browser (headless mode = no UI)
        browser = await p.chromium.launch(headless=False, slow_mo=50)
        page = await browser.new_page()

        # Go to Facebook
        await page.goto("https://www.facebook.com", timeout=60000)

        # Extract metadata
        metadata = {
            "title": await page.title(),
            "description": await safe_get_attribute(page, "meta[name='description']", "content"),
            "og:title": await safe_get_attribute(page, "meta[property='og:title']", "content"),
            "og:description": await safe_get_attribute(page, "meta[property='og:description']", "content"),
            "og:image": await safe_get_attribute(page, "meta[property='og:image']", "content"),
        }

        # Print metadata
        print("📌 Extracted Metadata:")
        for key, value in metadata.items():
            print(f"{key}: {value}")

        # Save metadata into JSON file
        with open("metadata.json", "w", encoding="utf-8") as f:
            json.dump(metadata, f, indent=4, ensure_ascii=False)

        print("\n✅ Metadata saved to metadata.json")

        # Close browser
        await browser.close()


if __name__ == "__main__":
    asyncio.run(run())
