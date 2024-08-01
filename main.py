import asyncio
import uuid
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, WebAppInfo
from scraper import VideoScraper
from downloader import VideoDownloader
import json

# Pyrogram configuration
API_ID = 29920508
API_HASH = "10676e77085a5214bcea5ca17cda5778"
BOT_TOKEN = "7228041236:AAFgNivGjOg4hMiBGfKo77Z_W9izjUpeaGE"

lodu = Client(":xgroovy_bot:", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

scraper = VideoScraper()
downloader = VideoDownloader()

# Store video identifiers and URLs
video_mapping = {}

@lodu.on_message(filters.command("start"))
async def start(client, message: Message):
    await message.reply("Hello! Send me a query to search for videos.")

@lodu.on_message(filters.text & ~filters.command("start"))
async def search_videos(client, message: Message):
    query = message.text
    # Replace spaces with hyphens
    formatted_query = query.replace(' ', '-')
    await message.reply(f"Searching for videos with query: {formatted_query}")

    scraped_data = await scraper.scrape_videos(formatted_query)

    if scraped_data:
        videos = json.loads(scraped_data)[:10]  # Take only the first 10 results

        for video in videos:
            # Generate a unique identifier for each video
            video_id = str(uuid.uuid4())
            video_mapping[video_id] = video['video_url']

            response = (
                f"Title: {video['title']}\n"
                f"Preview: {video['preview_url']}\n"
            )
            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("View Video", callback_data=f"download_{video_id}")]
            ])
            await message.reply_video(video=video['preview_url'], caption=video['title'], reply_markup=keyboard)
    else:
        await message.reply("No videos found.")

@lodu.on_callback_query(filters.regex(r"^download_(.+)"))
async def download_video(client, callback_query: CallbackQuery):
    video_id = callback_query.data.split("_")[1]
    video_url = video_mapping.get(video_id)

    if video_url:
        # Generate a download link (ensure it's a valid HTTPS URL)
        download_link = await downloader.download_video(video_url)
        if download_link:
            # Use WebAppInfo to open the link
            dl_keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("Watch Video", web_app=WebAppInfo(url=download_link))]
            ])
            await callback_query.message.edit_text(
                text="Click the button to view the video:",
                reply_markup=dl_keyboard
            )
            # await client.reply_video("Click the button to view the video",reply_markup=dl_keyboard)
        else:
            await callback_query.answer("Failed to get download link.", show_alert=True)
    else:
        await callback_query.answer("Invalid video ID.", show_alert=True)

if __name__ == "__main__":
    lodu.run()
