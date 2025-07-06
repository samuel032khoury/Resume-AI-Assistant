import asyncio
from playwright.async_api import async_playwright

def generate_pdf_from_html(html_content: str, output_path: str) -> None:
    async def main():
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            context = await browser.new_context(locale="en-US")
            page = await context.new_page()
            await page.set_content(html_content, wait_until='networkidle')
            await page.pdf(path=output_path, format='A4')
            await browser.close()

    asyncio.run(main())