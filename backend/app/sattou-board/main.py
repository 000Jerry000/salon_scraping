import asyncio
from login import login
from getting_schedule import getting_schedule
from playwright.async_api import async_playwright
import asyncio
import random

async def human_wait(base=300, variance=200):
    """人間のような微妙な待機（ミリ秒）"""
    await asyncio.sleep((base + random.randint(-variance, variance)) / 1000)


async def main():
    print("▶ Step 0: Starting browser...")
    async with async_playwright() as p:
        user_agent = (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/124.0.0.0 Safari/537.36"
        )
    
        async with async_playwright() as p:
            browser = await p.chromium.launch(
                headless=False,
                args=[
                    "--start-maximized",
                    "--disable-blink-features=AutomationControlled",
                ]
            )
    
            context = await browser.new_context(
                user_agent=user_agent,
                viewport={'width': 1024, 'height': 768}
            )
    
            page = await context.new_page()

            # Hide navigator.webdriver
            await page.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            });
            """)

            print("▶ Step 1: Logging in to Sattou...")
            await login(page, human_wait)

            print("▶ Step 2: Getting schedule page...")
            await getting_schedule(page, human_wait)

            print("✅ All steps completed successfully.")
            # await asyncio.sleep(9999)  # ページを保持したままにする（終了防止）

if __name__ == "__main__":
    asyncio.run(main())
