import asyncio
import playwright.async_api as pw

async def _generate_pdf_from_html(html_content: str, output_path: str) -> None:
    async with pw.async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.set_content(html_content, wait_until='networkidle')
        await page.pdf(path=output_path, format='A4')
        await browser.close()
def generate_pdf_from_html(html_content: str, output_path: str) -> None:
    asyncio.run(_generate_pdf_from_html(html_content, output_path))
