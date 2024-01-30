import typing
from playwright.sync_api import sync_playwright, Page
from recaptcha_challenger import new_audio_solver
import re
from dotenv import load_dotenv
import os


load_dotenv()

def motion(page: Page) -> typing.Optional[str]:
    solver = new_audio_solver()
    if solver.utils.face_the_checkbox(page):
        solver.anti_recaptcha(page)
    return solver.response

def check_element(element, body_text, body):
    if element in body_text:
        enterprise_name_element = body.locator(f".{element}")
        return enterprise_name_element
    return None

def part_business_code(business_code_text):
    code_match = re.search(r'MÃ SỐ DN: (\d+)', business_code_text)
    if code_match:
        business_code = code_match.group(1)
        return business_code
    return None

def bytedance():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        ctx = browser.new_context(locale="en-US")
        page = ctx.new_page()
        page.goto(f"{os.getenv('url_bcdn')}")
        bodys =    page.locator("#ctl00_C_CtlList tr").all()
        for body in bodys:
            body_text = body.inner_html()
            # Checking if 'enterprise_name' class is present in the current table row
            check_class =  check_element('enterprise_name', body_text, body)
            bussiness_code =  check_element('enterprise_code', body_text, body)
            if check_class is not None and bussiness_code is not None:
                enterprise_name_text = check_class.inner_text()
                enterprise_bussines_text = part_business_code(bussiness_code.inner_text())
                print(f'bussines code: {enterprise_bussines_text}')
                print(f'Enterprise Name: {enterprise_name_text}')
                page1 = ctx.new_page()
                page1.goto(f"{os.getenv('url_find_bcdn')}")
                page1.locator("#ctl00_C_ANNOUNCEMENT_TYPE_IDFilterFld").select_option("NEW")
                page1.wait_for_timeout(5000)
                page1.locator("#ctl00_C_ENT_GDT_CODEFld").click()
                page1.locator("#ctl00_C_ENT_GDT_CODEFld").fill(f"{enterprise_bussines_text}")
                response = motion(page1)
                print(response)
                
                page1.get_by_role("button", name="Tìm kiếm", exact=True).click()
                with page1.expect_download() as download_info:
                    page1.locator("#ctl00_C_CtlList_ctl02_LnkGetPDFActive").click()
                download = download_info.value
                
            else:
                continue
        browser.close()



if __name__ == "__main__":
    bytedance()
