from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://bocaodientu.dkkd.gov.vn/egazette/Forms/Egazette/DefaultAnnouncements.aspx")
    page.wait_for_timeout(3000)
    pagition =  1
    while pagition < 5:
         pagition += 1
         if not page.is_closed():
            page.wait_for_timeout(5000)
            result = page.evaluate(f"""
                __doPostBack('ctl00$C$CtlList','Page${pagition}');
                "Script executed successfully!"
            """)
            print(result,pagition)
    
    print(f'Page${pagition}')
    page.wait_for_timeout(5000)

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
