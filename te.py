from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
   

    result = page.evaluate("""
        hidden = document.getElementById('return')
        hidden.style.display = 'none'
        __doPostBack('ctl00$C$CtlList','Page$5');
        "Script executed successfully!"
    """)
    print(result)
    page.wait_for_timeout(50000)

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
