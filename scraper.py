import asyncio
from pyppeteer import launch
import json
from loguru import logger

class VideoScraper:
    def __init__(self, headless=True):
        self.headless = headless

    async def _launch_browser(self):
        browser = await launch(headless=self.headless)
        page = await browser.newPage()
        return browser, page

    async def scrape_videos(self, query):
        logger.info(f"Starting video scrape with query: {query}")
        browser, page = await self._launch_browser()

        try:
            await page.goto(f"https://xgroovy.com/search/{query}")
            await page.waitForSelector('.list-videos .item', {'timeout': 15000})

            videos_data = await page.evaluate('''() => {
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
            await browser.close()
