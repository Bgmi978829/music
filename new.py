from pyrogram import Client, filters
from yt_dlp import YoutubeDL
import os

# --- Configuration ---
API_ID =   20692838  # Replace with your Telegram API ID
API_HASH = "4ecce96e4c626342c08d2424eccc619e"  # Replace with your Telegram API Hash
BOT_TOKEN = "7023010693:AAGZYUavjUzgifc0YtFb1f-IfWhxTLuxD2Y"  # Replace with your Telegram Bot Token

# Initialize Bot
app = Client("music_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# --- Helper Functions ---
def download_audio_from_youtube(query):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'downloads/%(id)s.%(ext)s',
        'quiet': True
    }
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(f"ytsearch:{query}", download=True)
        file_path = ydl.prepare_filename(info['entries'][0])
        return file_path, info['entries'][0]['title']

# --- Commands ---
@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply_text(
        "🎵 **Welcome to the Music Bot!**\n\n"
        "Commands:\n"
        "/play [song name] - Download and send a song\n"
        "/spotify [song name] - Get Spotify link (optional)\n\n"
        "Made by @SHADE_OWNER"
    )

@app.on_message(filters.command("play"))
async def play(client, message):
    if len(message.command) < 2:
        await message.reply_text("❌ **Please specify a song name or URL!**")
        return

    query = " ".join(message.command[1:])
    await message.reply_text(f"🔄 **Searching and downloading:** {query} ...")

    try:
        file_path, title = download_audio_from_youtube(query)
        await message.reply_text(f"🎶 **Now Playing:** {title}")
        await message.reply_audio(audio=file_path, caption=f"**🎵 {title}**")
        os.remove(file_path)  # Clean up downloaded file
    except Exception as e:
        await message.reply_text(f"❌ **Error:** {str(e)}")

@app.on_message(filters.command("spotify"))
async def spotify(client, message):
    if len(message.command) < 2:
        await message.reply_text("❌ **Please specify a song name!**")
        return

    query = " ".join(message.command[1:])
    # Dummy response (Spotify integration removed for simplicity)
    await message.reply_text(f"🔗 **Spotify Link for '{query}':** [Click Here](https://open.spotify.com/search/{query})")

# --- Run Bot ---
if __name__ == "__main__":
    os.makedirs("downloads", exist_ok=True)
    app.run()