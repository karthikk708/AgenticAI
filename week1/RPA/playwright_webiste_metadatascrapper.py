from playwright.sync_api import sync_playwright
from pathlib import Path
import json


def get_meta_content(page, selector):
    try:
        return page.locator(selector).get_attribute("content") or "N/A"
    except:
        return "N/A"

def extract_jsonld(page):
    try:
        scripts = page.query_selector_all("script[type='application/ld+json']")
        all_jsonld = []
        for s in scripts:
            content = s.inner_text()
            try:
                parsed = json.loads(content)
                if isinstance(parsed, dict):
                    all_jsonld.append(parsed)
                elif isinstance(parsed, list):
                    all_jsonld.extend(parsed)
            except json.JSONDecodeError:
                continue
        return all_jsonld if all_jsonld else "N/A"
    except:
        return "N/A"

def format_jsonld_as_table(jsonld_data):
    if jsonld_data == "N/A":
        return "N/A"

    lines = ["| Key        | Value                           |", "|------------|-----------------------------------|"]
    for entry in jsonld_data:
        for k, v in entry.items():
            val = json.dumps(v) if isinstance(v, (dict, list)) else str(v)
            lines.append(f"| {k:<10} | {val[:35]:<35} |")
        lines.append("|------------|-----------------------------------|")
    return "\n".join(lines)

def extract_website_metadata(url: str, output_file: str = "website_metadata.txt"):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=100)
        page = browser.new_page()

        # Visit website
        page.goto(url, wait_until="load", timeout=60000)
        page.wait_for_timeout(3000)

        # Extract metadata
        title = page.title()
        meta_desc = get_meta_content(page, "meta[name='description']")
        meta_keywords = get_meta_content(page, "meta[name='keywords']")
        og_title = get_meta_content(page, "meta[property='og:title']")
        og_desc = get_meta_content(page, "meta[property='og:description']")
        og_image = get_meta_content(page, "meta[property='og:image']")
        og_url = get_meta_content(page, "meta[property='og:url']")
        canonical_url = page.locator("link[rel='canonical']").get_attribute("href") or "N/A"
        final_url = page.url

        # JSON-LD Structured Data
        jsonld_data = extract_jsonld(page)
        jsonld_table = format_jsonld_as_table(jsonld_data)
        jsonld_full = json.dumps(jsonld_data, indent=2, ensure_ascii=False) if jsonld_data != "N/A" else "N/A"

        # Build Output
        output = f"""
====================================================
🧠 Deep Website Metadata Report
====================================================

🌍 Website URL       : {url}
🔗 Final Loaded URL  : {final_url}
🧩 Canonical URL     : {canonical_url}

🏷️ Page Title        : {title}
📝 Meta Description  : {meta_desc}
🏷️ Meta Keywords     : {meta_keywords}

📘 Open Graph Title       : {og_title}
📘 Open Graph Description : {og_desc}
📘 Open Graph Image       : {og_image}
📘 Open Graph URL         : {og_url}

📦 Structured Data (JSON-LD) Summary:
-------------------------------------
{jsonld_table}


📦 Structured Data (JSON-LD) Full:
----------------------------------
{jsonld_full}

====================================================
        """.strip()

        Path(output_file).write_text(output, encoding='utf-8')
        print(f"\n✅ Metadata written to '{output_file}' with both summary and full JSON")

        browser.close()

if __name__ == "__main__":
    extract_website_metadata("https://npdigital.com")
