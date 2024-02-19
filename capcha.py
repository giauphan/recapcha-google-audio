import re
import os
from playwright.sync_api import sync_playwright
from dotenv import load_dotenv
from recognizer.agents.playwright import SyncChallenger

load_dotenv()

def check_element(element, body):
    return body.locator(f".{element}") if element in body.inner_html() else None

def extract_business_code(business_code_text):
    code_match = re.search(r'MÃ SỐ DN: (\d+)', business_code_text)
    return code_match.group(1) if code_match else None

def save_unique_file(download_obj, target_directory, suggested_filename):
    base_name, extension = os.path.splitext(suggested_filename)
    counter = 1

    while True:
        new_filename = f"{base_name} ({counter}){extension}"
        file_path = os.path.join(target_directory, new_filename)

        if not os.path.exists(file_path):
            download_obj.save_as(file_path)
            break

        counter += 1

def process_page_data(page):
    body_rows = page.locator("#ctl00_C_CtlList tr").all()
    for body in body_rows:
        enterprise_name = check_element('enterprise_name', body)
        enterprise_code = check_element('enterprise_code', body)
        
        if enterprise_name and enterprise_code:
            enterprise_name_text = enterprise_name.inner_text()
            enterprise_code_text = extract_business_code(enterprise_code.inner_text())
            print(f'Business code: {enterprise_code_text}')

            page1 = page.context.new_page()
            page1.goto(os.getenv('url_find_bcdn'))
            page1.locator("#ctl00_C_ANNOUNCEMENT_TYPE_IDFilterFld").select_option("NEW")
            page1.wait_for_timeout(5000)

            while True:
                try:
                    challenger = SyncChallenger(page1)
                    challenger.solve_recaptcha()
                    break
                except:
                    page1.reload()
                    page1.wait_for_timeout(15000)
                    print('Your computer or network may be sending automated queries')

            page1.locator("#ctl00_C_ENT_GDT_CODEFld").click()
            page1.locator("#ctl00_C_ENT_GDT_CODEFld").fill(f"{enterprise_code_text}")
            page1.get_by_role("button", name="Tìm kiếm", exact=True).click()

            with page1.expect_download() as download_info:
                page1.locator("#ctl00_C_CtlList_ctl02_LnkGetPDFActive").click()

            download_object = download_info.value
            target_directory = os.getenv('target_directory')
            file_name = f"{enterprise_code_text}.pdf"
            save_unique_file(download_object, target_directory, file_name)
            page1.wait_for_timeout(5000)
            page1.close()

def bytedance():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, args=['--disable-gpu', '--single-process'])
        ctx = browser.new_context(locale="en-US")

        for pagination in range(1, 5):
            page = ctx.new_page()
            print(os.getenv('url_bcdn'))
            page.goto(os.getenv('url_bcdn'))
            page.wait_for_timeout(5000)

            if pagination >= 2:
                page.wait_for_timeout(5000)
                result = page.evaluate(f"__doPostBack('ctl00$C$CtlList','Page${pagination}');")
                print(result)

            process_page_data(page)
            page.close()

        browser.close()

if __name__ == "__main__":
    bytedance()
