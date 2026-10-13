import os
from pyrogram import Client, filters
import yt_dlp

API_ID = 38783407
API_HASH = "B3bb213e642a8053f53fe273edf078d4"
BOT_TOKEN = "8892983715:AAGh0VsEIxFQvngWqXgJYaL9ymJ4sweTXzA"

app = Client("tiktok_downloader_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply_text("👋 স্বাগতম! আমাকে যেকোনো টিকটক ভিডিওর লিংক পাঠান, আমি ওয়াটারমার্ক ছাড়া ডাউনলোড করে দিচ্ছি।")

@app.on_message(filters.regex(r"https?://"))
async def download_video(client, message):
    url = message.text.strip()
    if "tiktok" not in url:
        await message.reply_text("❌ দয়া করে সঠিক টিকটক লিংক দিন।")
        return

    msg = await message.reply_text("⏳ ভিডিও ডাউনলোড হচ্ছে, একটু অপেক্ষা করুন...")
    out_file = f"tiktok_{message.id}.mp4"

    ydl_opts = {'format': 'best', 'outtmpl': out_file, 'quiet': True}

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        await message.reply_video(video=out_file, caption="✨ ওয়াটারমার্ক ছাড়া আপনার ভিডিও রেডি!")
        await msg.delete()
    except Exception as e:
        await message.reply_text(f"❌ সমস্যা হয়েছে: {str(e)}")
        await msg.delete()
    finally:
        if os.path.exists(out_file):
            os.remove(out_file)

if __name__ == "__main__":
    app.run()
