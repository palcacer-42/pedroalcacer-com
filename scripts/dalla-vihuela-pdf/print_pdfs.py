import asyncio
import os
from pathlib import Path
from playwright.async_api import async_playwright

OUT = Path(__file__).parent / "output"
BASE_DIR = '/Users/palcacer/Sites/pedroalcacer-com/static/programs/originals'

async def print_pdfs():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        for html_file in OUT.glob("*.html"):
            pdf_path = os.path.join(BASE_DIR, html_file.name.replace(".html", ".pdf"))
            await page.goto(f"file://{html_file.absolute()}")
            await page.wait_for_timeout(500)
            await page.pdf(
                path=pdf_path,
                format="A4",
                landscape=True,
                print_background=True,
                display_header_footer=False,
                margin={"top": "0", "right": "0", "bottom": "0", "left": "0"}
            )
            print(f"Printed PDF from {html_file.name} to {pdf_path}")
            
        await browser.close()

if __name__ == "__main__":
    asyncio.run(print_pdfs())
