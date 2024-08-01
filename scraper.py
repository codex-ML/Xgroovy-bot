import asyncio
import json
from loguru import logger
from playwright.async_api import async_playwright

class VideoScraper:
    def __init__(self, headless=True):
        self.headless = headless
        self.playwright = None
        self.browser = None
        self.page = None

    async def _launch_browser(self):
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(headless=self.headless)
        self.page = await self.browser.new_page()

    async def scrape_videos(self, query):
        logger.info(f"Starting video scrape with query: {query}")
        await self._launch_browser()

        try:
            await self.page.goto(f"https://xgroovy.com/search/{query}")
            await self.page.wait_for_selector('.list-videos .item', timeout=15000)

            videos_data = await self.page.evaluate('''() => {
                const video_elements = document.querySelectorAll('.list-videos .item');
                const videos = [];

                video_elements.forEach(video => {
                    const thumbnail_url = video.querySelector('img.thumb').src;
                    const preview_url = video.querySelector('img.thumb').getAttribute('data-preview');
                    const video_url = video.querySelector('.popito').href;
                    const title = video.querySelector('.title').textContent;

                    videos.push({
                        thumbnail_url: thumbnail_url,
                        preview_url: preview_url,
                        video_url: video_url,
                        title: title
                    });
                });

                return videos;
            }''')

            json_data = json.dumps(videos_data, indent=2)
            logger.info(f"Scraped {len(videos_data)} videos")
            return json_data
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

# # Example usage:
# async def main():
#     scraper = VideoScraper()
#     query = "russian"
#     result = await scraper.scrape_videos(query)
#     print(result)
#     await scraper.close()

# asyncio.run(main())

# # https://xgroovy.com/videos/78856/russian-harlot-gets-facial-after-rough-anal-amateur-porn
