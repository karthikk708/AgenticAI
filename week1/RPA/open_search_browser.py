from playwright.sync_api import sync_playwright

def search_bing_with_xpath_and_click():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=100)
        page = browser.new_page()

        # Step 1: Go to Bing
        page.goto("https://www.bing.com")

        # Step 2: Wait for search box using XPath
        search_input = page.locator('xpath=//*[@id="sb_form_q"]')
        search_input.wait_for(timeout=10000)
        search_input.fill("AI Agent")
        search_input.press("Enter")

        # Step 3: Wait for results and click the first one
        page.wait_for_selector("li.b_algo h2 a", timeout=10000)
        first_result = page.locator("li.b_algo h2 a").first
        print("🔍 Clicking:", first_result.inner_text())
        first_result.click()

        # Step 4: Wait for navigation
        page.wait_for_load_state("load")
        print("✅ Navigated to:", page.url)

        page.wait_for_timeout(5000)  # Optional: keep browser open
        browser.close()

if __name__ == "__main__":
    search_bing_with_xpath_and_click()
