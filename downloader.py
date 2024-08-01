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

    async def download_video(self, url):
        logger.info(f"Starting video download from: {url}")
        await self._launch_browser()

        try:
            await self.page.goto(url)
            await self.page.wait_for_selector('video', timeout=15000)
            video_source_url = await self.page.evaluate('''() => {
                const videoElement = document.querySelector('video');
                return videoElement ? videoElement.src : null;
            }''')

            if video_source_url:
                await self.page.goto(video_source_url)
                await asyncio.sleep(5)
                current_url = self.page.url
                logger.info(f"Video URL found: {current_url}")
                return current_url
            else:
                logger.warning("No video element found on the page")
                return None
        except Exception as e:
            logger.error(f"An error occurred: {e}")
            return None
        finally:
            if self.browser:
                await self.browser.close()
            if self.playwright:
                await self.playwright.stop()

    async def close(self):
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()

# Example usage:
# async def main():
#     downloader = VideoDownloader()
#     url = "https://xgroovy.com/videos/78856/russian-harlot-gets-facial-after-rough-anal-amateur-porn"
#     video_url = await downloader.download_video(url)
#     print(f"Downloaded video URL: {video_url}")
#     await downloader.close()

# asyncio.run(main())
