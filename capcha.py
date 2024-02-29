import re
import asyncio
import os
from playwright.async_api import async_playwright
from dotenv import load_dotenv
from Model.ElectronicReport import Electronic_report

load_dotenv()


async def check_element(element, body):
    inner_html = await body.inner_html()
    return body.locator(f".{element}") if element in inner_html else None


def extract_business_code(business_code_text):
    code_match = re.search(r"MÃ SỐ DN: (\d+)", business_code_text)
    return code_match.group(1) if code_match else None


async def process_page_data(page):
    CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
    DOWNLOAD_DIR = os.path.join(CURRENT_DIR, "downloads")
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)

    await page.wait_for_selector("#ctl00_C_CtlList tr")
    await page.wait_for_timeout(5000)
    body_rows = await page.locator("#ctl00_C_CtlList tr").all()
    for body in body_rows:
        enterprise_name = await check_element("enterprise_name", body)
        enterprise_code = await check_element("enterprise_code", body)

        if enterprise_name and enterprise_code:
            enterprise_name_text = await enterprise_name.inner_text()
            business_code = extract_business_code(await enterprise_code.inner_text())

            check_business_code = await Electronic_report.objects.filter(
                business_code=business_code
            ).exists()
            if not check_business_code:
                await Electronic_report.objects.create(
                    business_name=enterprise_name_text,
                    business_code=business_code,
                )
            print(f"Business code: {business_code} {check_business_code}")


async def bytedance():
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=False, args=["--single-process", "--incognito"]
        )
        ctx = await browser.new_context()

        for pagination in range(1, 6):
            page = await ctx.new_page()
            print(os.getenv("url_bcdn"))
            print(f"page {pagination}")
            await page.goto(os.getenv("url_bcdn"))
            await page.wait_for_load_state("networkidle")  # Wait for network to be idle
            await page.wait_for_timeout(5000)

            if pagination >= 2:
                result = await page.evaluate(
                    f"__doPostBack('ctl00$C$CtlList','Page${pagination}');"
                )
                print(result)
                await page.wait_for_timeout(5000)

            await process_page_data(page)
            await page.close()

        await browser.close()


if __name__ == "__main__":
    asyncio.run(bytedance())
