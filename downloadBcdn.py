import re
import os
from playwright.sync_api import sync_playwright
from dotenv import load_dotenv
from recognizer.agents.playwright import SyncChallenger
from GoogleDriver import upload_basic
from Model.ElectronicReport import Electronic_report

load_dotenv()


def check_element(element, body):
    return body.locator(f".{element}") if element in body.inner_html() else None


def extract_business_code(business_code_text):
    code_match = re.search(r"MÃ SỐ DN: (\d+)", business_code_text)
    return code_match.group(1) if code_match else None


def process_page_data(arr_bussine_code, ctx):
    CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
    DOWNLOAD_DIR = os.path.join(CURRENT_DIR, "downloads")
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)

    for business_obj in arr_bussine_code:
        enterprise_code = business_obj.business_code

        enterprise_code_text = extract_business_code(enterprise_code.inner_text())
        print(f"Business code: {enterprise_code_text}")

        page_find = ctx.new_page()
        page_find.goto(os.getenv("url_find_bcdn"))
        page_find.locator("#ctl00_C_ANNOUNCEMENT_TYPE_IDFilterFld").select_option("NEW")
        page_find.wait_for_timeout(5000)
        while True:
            try:
                challenger = SyncChallenger(page_find)
                challenger.solve_recaptcha()
                break
            except:
                print("Your computer or network may be sending automated queries")
                page_find.reload()
                page_find.wait_for_timeout(15000)

        page_find.locator("#ctl00_C_ENT_GDT_CODEFld").click()
        page_find.locator("#ctl00_C_ENT_GDT_CODEFld").fill(f"{enterprise_code_text}")
        page_find.get_by_role("button", name="Tìm kiếm", exact=True).click()

        with page_find.expect_download() as download_info:
            page_find.locator("#ctl00_C_CtlList_ctl02_LnkGetPDFActive").click()

        file_name = f"{enterprise_code_text}.pdf"
        print(f"wait download file {file_name}")
        download = download_info.value
        download_path = os.path.join(DOWNLOAD_DIR, file_name)
        download.save_as(download_path)
        page_find.wait_for_timeout(5000)
        with open(download_path, "rb") as file:
            file_content = file.read()
        os.remove(download_path)

        folder_id = os.getenv("folder_id")
        print(download_path, folder_id)
        upload_basic(folder_id, file_content, file_name, "application/pdf")

        print(f"Successfully installed {file_name}")
        page_find.wait_for_timeout(5000)
        page_find.close()


async def download_bcdn():
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True, args=["--single-process", "--incognito"]
        )
        ctx = browser.new_context()
        Electronic = await Electronic_report.objects.all()
        process_page_data(Electronic, ctx)

        browser.close()


import asyncio

if __name__ == "__main__":
    asyncio.run(download_bcdn())
