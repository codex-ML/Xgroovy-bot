import asyncio
from playwright.async_api import async_playwright
from loguru import logger

class VideoDownloader:
    def __init__(self, headless=True):
        self.headless = headless
        self.playwright = None
        self.browser = None
        self.page = None

    async def _launch_browser(self):
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(headless=self.headless)
        self.page = await self.browser.new_page()

    async def download_video(self, url, retries=3):
        logger.info(f"Starting video download from: {url}")
        await self._launch_browser()

        attempt = 0
        while attempt < retries:
            try:
                await self.page.goto(url, timeout=30000)
                await self.page.wait_for_selector('video', timeout=30000)
                video_source_url = await self.page.evaluate('''() => {
                    const videoElement = document.querySelector('video');
                    return videoElement ? videoElement.src : null;
                }''')

                if video_source_url:
                    await self.page.goto(video_source_url, timeout=30000)
                    await asyncio.sleep(5)
                    current_url = self.page.url
                    logger.info(f"Video URL found: {current_url}")
                    return current_url
                else:
                    logger.warning("No video element found on the page")
                    return None
            except Exception as e:
                logger.error(f"An error occurred: {e}")
                attempt += 1
                if attempt < retries:
                    logger.info(f"Retrying ({attempt}/{retries})...")
                    await asyncio.sleep(5)  # Backoff before retrying

        logger.error("Failed to download video after multiple attempts.")
        return None

    async def close(self):
        if self.browser:
            try:
                await self.browser.close()
            except Exception as close_exception:
                logger.error(f"An error occurred while closing the browser: {close_exception}")
        if self.playwright:
            await self.playwright.stop()
