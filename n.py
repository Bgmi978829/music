from pyrogram import Client, filters
from pytgcalls import PyTgCalls, idle
from pytgcalls.types.input_stream import InputAudioStream
from yt_dlp import YoutubeDL
from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials
import os

# --- Configuration ---
API_ID = 20692838 # Replace with your API ID
API_HASH = "4ecce96e4c626342c08d2424eccc619e"  # Replace with your API Hash
BOT_TOKEN = "7023010693:AAGZYUavjUzgifc0YtFb1f-IfWhxTLuxD2Y"  # Replace with your Bot Token
SPOTIFY_CLIENT_ID = "c1d3488835bd453abd89bb350a2d44ac"  # Replace with Spotify Client ID
SPOTIFY_CLIENT_SECRET = "6c97c7d5fb724824a2eaa704b267de39"  # Replace with Spotify Client Secret

# Initialize Spotify
spotify = Spotify(client_credentials_manager=SpotifyClientCredentials(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET
))

# Initialize Telegram Bot and PyTgCalls
app = Client("music_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
pytgcalls = PyTgCalls(app)

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
        return file_path

def get_spotify_track_url(query):
    results = spotify.search(q=query, type='track', limit=1)
    if results['tracks']['items']:
        return results['tracks']['items'][0]['external_urls']['spotify']
    return None

# --- Commands ---
@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply_text(
        "🎵 **Welcome to the Music Bot!**\n\n"
        "Commands:\n"
        "/play [song name] - Play a song\n"
        "/pause - Pause playback\n"
        "/resume - Resume playback\n"
        "/stop - Stop playback\n"
        "/spotify [song name] - Get Spotify link\n"
        "/queue - Show current queue\n"
        "/leave - Leave voice chat\n\n"
        "Made by @SHADE_OWNER"
    )

@app.on_message(filters.command("play"))
async def play(client, message):
    chat_id = message.chat.id
    if len(message.command) < 2:
        await message.reply_text("❌ **Please specify a song name or URL!**")
        return
    query = " ".join(message.command[1:])
    audio_file = download_audio_from_youtube(query)
    await pytgcalls.join_group_call(
        chat_id,
        InputAudioStream(audio_file)
    )
    await message.reply_text(f"🎶 **Playing:** {query}")

@app.on_message(filters.command("pause"))
async def pause(client, message):
    chat_id = message.chat.id
    await pytgcalls.pause_stream(chat_id)
    await message.reply_text("⏸ **Playback paused.**")

@app.on_message(filters.command("resume"))
async def resume(client, message):
    chat_id = message.chat.id
    await pytgcalls.resume_stream(chat_id)
    await message.reply_text("▶️ **Playback resumed.**")

@app.on_message(filters.command("stop"))
async def stop(client, message):
    chat_id = message.chat.id
    await pytgcalls.leave_group_call(chat_id)
    await message.reply_text("⏹ **Playback stopped.**")

@app.on_message(filters.command("spotify"))
async def spotify_link(client, message):
    if len(message.command) < 2:
        await message.reply_text("❌ **Please specify a song name!**")
        return
    query = " ".join(message.command[1:])
    url = get_spotify_track_url(query)
    if url:
        await message.reply_text(f"🎵 **Spotify Link:** {url}")
    else:
        await message.reply_text("❌ **Could not find the song on Spotify.**")

@app.on_message(filters.command("leave"))
async def leave(client, message):
    chat_id = message.chat.id
    await pytgcalls.leave_group_call(chat_id)
    await message.reply_text("👋 **Left the voice chat.**")

# --- Run Bot ---
if __name__ == "__main__":
    os.makedirs("downloads", exist_ok=True)
    pytgcalls.start()
    app.run()
    idle()