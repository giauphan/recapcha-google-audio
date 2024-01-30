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

def check_element(element, body):
    return body.locator(f".{element}") if element in body.inner_html() else None

def part_business_code(business_code_text):
    code_match = re.search(r'MÃ SỐ DN: (\d+)', business_code_text)
    return code_match.group(1) if code_match else None

def save_unique_file(download_obj, target_directory):
    suggested_filename = download_obj.suggested_filename

    # Check if the file already exists in the target directory
    base_name, extension = os.path.splitext(suggested_filename)
    counter = 1
    
    while True:
        # If it exists, increment the filename
        new_filename = f"{base_name} ({counter}){extension}"
        file_path = os.path.join(target_directory, new_filename)

        if not os.path.exists(file_path):
            # Save the file with the unique filename
            download_obj.save_as(file_path)
            break

        counter += 1


def bytedance():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        ctx = browser.new_context(locale="en-US")

        page = ctx.new_page()
        page.goto(f"{os.getenv('url_bcdn')}")
        bodys =    page.locator("#ctl00_C_CtlList tr").all()
        for body in bodys:
            check_class =  check_element('enterprise_name', body)
            bussiness_code =  check_element('enterprise_code', body)
            if check_class is not None and bussiness_code is not None:
                enterprise_name_text = check_class.inner_text()
                enterprise_bussines_text = part_business_code(bussiness_code.inner_text())
                print(f'bussines code: {enterprise_bussines_text}')
                print(f'Enterprise Name: {enterprise_name_text}')
                page1 = ctx.new_page()
                # find url_find_bcdn
                page1.goto(f"{os.getenv('url_find_bcdn')}")
                page1.locator("#ctl00_C_ANNOUNCEMENT_TYPE_IDFilterFld").select_option("NEW")
                page1.wait_for_timeout(5000)
                page1.locator("#ctl00_C_ENT_GDT_CODEFld").click()
                page1.locator("#ctl00_C_ENT_GDT_CODEFld").fill(f"{enterprise_bussines_text}")
                response = motion(page1)
                
                page1.get_by_role("button", name="Tìm kiếm", exact=True).click()
                with page1.expect_download() as download_info:
                    page1.locator("#ctl00_C_CtlList_ctl02_LnkGetPDFActive").click()
                download_object = download_info.value
                target_directory = 'D:\\Down-bcdn\\'
                save_unique_file(download_object, target_directory)
                page1.close()
                page1.wait_for_timeout(10000)

                
            else:
                continue
        browser.close()



if __name__ == "__main__":
    bytedance()
