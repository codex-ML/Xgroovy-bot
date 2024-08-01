import asyncio
from pyppeteer import launch
from loguru import logger

class VideoDownloader:
    def __init__(self, headless=True):
        self.headless = headless

    async def _launch_browser(self):
        browser = await launch(headless=self.headless)
        page = await browser.newPage()
        return browser, page

    async def download_video(self, url):
        logger.info(f"Starting video download from: {url}")
        browser, page = await self._launch_browser()

        try:
            await page.goto(url)
            await page.waitForSelector('video', {'timeout': 15000})
            video_source_url = await page.evaluate('''() => {
                const videoElement = document.querySelector('video');
                return videoElement ? videoElement.src : null;
            }''')

            if video_source_url:
                await page.goto(video_source_url)
                await asyncio.sleep(5)
                current_url = page.url
                logger.info(f"Video URL found: {current_url}")
                return current_url
            else:
                logger.warning("No video element found on the page")
                return None
        except Exception as e:
            logger.error(f"An error occurred: {e}")
            return None
        finally:
            await browser.close()
