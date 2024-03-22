import os
import asyncio
from playwright.async_api import async_playwright
from dotenv import load_dotenv
from recognizer.agents.playwright import AsyncChallenger
from GoogleDriver import upload_basic
from Model.ElectronicReport import Electronic_report
import botright

load_dotenv()


async def process_page_data(enterprise_code_text, page_find):
    CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
    DOWNLOAD_DIR = os.path.join(CURRENT_DIR, "downloads")
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)

    for _ in range(3):
        try:
            await page_find.locator(
                "#ctl00_C_ANNOUNCEMENT_TYPE_IDFilterFld"
            ).select_option("NEW")
            await page_find.wait_for_timeout(5000)
            await page_find.locator("#ctl00_C_ENT_GDT_CODEFld").click()
            await page_find.locator("#ctl00_C_ENT_GDT_CODEFld").fill(
                f"{enterprise_code_text}"
            )
            await page_find.wait_for_timeout(2000)

            challenger = AsyncChallenger(page_find)
            await challenger.solve_recaptcha()
            await page_find.wait_for_timeout(5000)

            await page_find.get_by_role("button", name="Tìm kiếm", exact=True).click()
            async with page_find.expect_download() as download_info:
                await page_find.locator(
                    "#ctl00_C_CtlList_ctl02_LnkGetPDFActive"
                ).click()
            download = await download_info.value
            file_name = f"{enterprise_code_text}.pdf"
            download_path = os.path.join(DOWNLOAD_DIR, file_name)
            await download.save_as(download_path)
            with open(download_path, "rb") as file:
                file_content = file.read()
            os.remove(download_path)
            folder_id = os.getenv("folder_id")
            upload_basic(folder_id, file_content, file_name, "application/pdf")
            print(f"Successfully downloaded and uploaded {file_name}")
            return True
        except Exception as e:
            print(f"Error occurred: {e}")
            await page_find.reload()
            await page_find.wait_for_load_state("networkidle")
            await page_find.wait_for_timeout(5000)

    else:
        print("Failed after multiple attempts.")
        return False


async def bytedance():
    async with async_playwright() as p:
        browser = await botright.Botright( headless=True)
        ctx = await browser.new_browser()
        Electronic = await Electronic_report.objects.filter(status=False).all()

        for business_obj in Electronic:
            page = await ctx.new_page()
            print(os.getenv("url_find_bcdn"))

            await page.goto(os.getenv("url_find_bcdn"))
            await page.wait_for_load_state("networkidle")
            await page.wait_for_timeout(5000)

            enterprise_code_text = business_obj.business_code
            success = await process_page_data(enterprise_code_text, page)
            await Electronic_report.objects.filter(
                business_code=business_obj.business_code
            ).update(status=True)
            if success:
                await page.close()
            else:
                print(
                    f"Skipping to the next business object due to failure.enterprise_code_text: {enterprise_code_text}"
                )
                await page.close()
                continue

        await browser.close()


if __name__ == "__main__":
    asyncio.run(bytedance())
