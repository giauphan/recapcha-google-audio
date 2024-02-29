import os
import asyncio
from playwright.async_api import async_playwright
from dotenv import load_dotenv
from recognizer.agents.playwright import AsyncChallenger
from GoogleDriver import upload_basic
from Model.ElectronicReport import Electronic_report

load_dotenv()


async def process_page_data(arr_business_code, ctx):
    CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
    DOWNLOAD_DIR = os.path.join(CURRENT_DIR, "downloads")
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)

    for business_obj in arr_business_code:
        enterprise_code_text = business_obj.business_code
        print(f"Business code: {enterprise_code_text}")

        page_find = await ctx.new_page()
        await page_find.goto(os.getenv("url_find_bcdn"))
        print(os.getenv("url_find_bcdn"))
        await page_find.wait_for_selector("#ctl00_C_ANNOUNCEMENT_TYPE_IDFilterFld")
        await page_find.wait_for_timeout(5000)
        await page_find.locator("#ctl00_C_ANNOUNCEMENT_TYPE_IDFilterFld").select_option(
            "NEW"
        )
        await page_find.wait_for_timeout(5000)
        while True:
            try:
                challenger = AsyncChallenger(page_find)
                await challenger.solve_recaptcha()
                break
            except:
                print("Your computer or network may be sending automated queries")
                await page_find.reload()
                await page_find.wait_for_timeout(15000)

        await page_find.locator("#ctl00_C_ENT_GDT_CODEFld").click()
        await page_find.locator("#ctl00_C_ENT_GDT_CODEFld").fill(
            f"{enterprise_code_text}"
        )
        await page_find.get_by_role("button", name="Tìm kiếm", exact=True).click()

        async with page_find.expect_download() as download_info:
            await page_find.locator("#ctl00_C_CtlList_ctl02_LnkGetPDFActive").click()

        file_name = f"{enterprise_code_text}.pdf"
        print(f"wait download file {file_name}")
        download = download_info.value
        download_path = os.path.join(DOWNLOAD_DIR, file_name)
        await download.save_as(download_path)
        await page_find.wait_for_timeout(5000)
        with open(download_path, "rb") as file:
            file_content = file.read()
        os.remove(download_path)

        folder_id = os.getenv("folder_id")
        print(download_path, folder_id)
        upload_basic(folder_id, file_content, file_name, "application/pdf")

        print(f"Successfully installed {file_name}")
        await page_find.wait_for_timeout(5000)
        await page_find.close()


async def download_bcdn():
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True, args=["--single-process", "--incognito"]
        )
        ctx = await browser.new_context()
        Electronic = await Electronic_report.objects.all()
        await process_page_data(Electronic, ctx)

        await browser.close()


if __name__ == "__main__":
    asyncio.run(download_bcdn())
