from pytdbot import Client
from pytdbot.types import Message, InputFileLocal, Error
from TgMusic.core._downloader import DownloaderWrapper
from TgMusic.modules.utils.play_helpers import get_url
import os


@Client.on_message()
async def private_download_handler(client, message: Message):
    # Only handle private chats and ignore commands
    if message.chat_id < 0 or not message.text or message.text.startswith("/"):
        return

    url = await get_url(message, None)

    if not url:
        query = url or message.text.strip()
        if not query:
            await message.reply_text("❗ Please send a song name or link.")
            return

        temp_wrapper = DownloaderWrapper(query)
        search_result = await temp_wrapper.search()
        if isinstance(search_result, Error):
            return await message.reply_text(
                f"🔍 Search failed: {search_result.message}"
            )

        if not search_result or not search_result.tracks:
            return await message.reply_text(
                "🔍 No results found. Try different keywords."
            )

        url = search_result.tracks[0].url

    wrapper = DownloaderWrapper(url)
    if not wrapper.is_valid():
        await message.reply_text(
            "⚠️ Unsupported or invalid link.\nSupported: YouTube, Spotify, JioSaavn, SoundCloud, Apple Music"
        )
        return

    status = await message.reply_text("🔎 Searching and downloading...")
    track_info = await wrapper.get_track()
    if hasattr(track_info, "message"):
        await status.edit_text(
            f"❌ Couldn't retrieve track info:\n{track_info.message}"
        )
        return

    file_path = await wrapper.download_track(track_info)
    if hasattr(file_path, "message"):
        await status.edit_text(f"❌ Download failed:\n{file_path.message}")
        return

    print(track_info)

    try:
        # still missing `performer` field
        await message.reply_audio(
            audio=InputFileLocal(str(file_path)),
            title=getattr(track_info, "name", None),
            duration=getattr(track_info, "duration", None),
        )
        await status.delete(revoke=True)
    except Exception as e:
        await status.edit_text(f"❌ Failed to send audio: {e}")
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)
