# Copyright (c) 2025 AshokShau
# Licensed under the GNU AGPL v3.0: https://www.gnu.org/licenses/agpl-3.0.html
# Part of the TgMusicBot project. All rights reserved where applicable.

from pytdbot import Client, types

from TgMusic.core import Filter, db, admins_only
from TgMusic.logger import LOGGER
from TgMusic.modules.utils.play_helpers import extract_argument


@Client.on_message(filters=Filter.command(["buttons"]))
@admins_only(only_owner=True)
async def buttons(_: Client, msg: types.Message) -> None:
    """Toggle button controls."""
    chat_id = msg.chat_id
    if chat_id > 0:
        return

    current = await db.get_buttons_status(chat_id)
    args = extract_argument(msg.text)

    if not args:
        status = "enabled ✅" if current else "disabled ❌"
        reply = await msg.reply_text(
            f"⚙️ <b>Button Control Status:</b> {status}\n\n"
            "Usage: <code>/buttons [on|off|enable|disable]</code>"
        )
        if isinstance(reply, types.Error):
            LOGGER.warning(reply.message)
        return

    arg = args.lower()
    if arg in ["on", "enable"]:
        await db.set_buttons_status(chat_id, True)
        reply = await msg.reply_text("✅ Button controls enabled.")
    elif arg in ["off", "disable"]:
        await db.set_buttons_status(chat_id, False)
        reply = await msg.reply_text("❌ Button controls disabled.")
    else:
        reply = await msg.reply_text(
            "⚠️ Invalid command usage.\n"
            "Correct usage: <code>/buttons [enable|disable|on|off]</code>"
        )
    if isinstance(reply, types.Error):
        LOGGER.warning(reply.message)


@Client.on_message(filters=Filter.command(["thumbnail", "thumb"]))
@admins_only(only_owner=True)
async def thumbnail(_: Client, msg: types.Message) -> None:
    """Toggle thumbnail settings."""
    chat_id = msg.chat_id
    if chat_id > 0:
        return

    current = await db.get_thumbnail_status(chat_id)
    args = extract_argument(msg.text)

    if not args:
        status = "enabled ✅" if current else "disabled ❌"
        reply = await msg.reply_text(
            f"🖼️ <b>Thumbnail Status:</b> {status}\n\n"
            "Usage: <code>/thumbnail [on|off|enable|disable]</code>"
        )
        if isinstance(reply, types.Error):
            LOGGER.warning(reply.message)
        return

    arg = args.lower()
    if arg in ["on", "enable"]:
        await db.set_thumbnail_status(chat_id, True)
        reply = await msg.reply_text("✅ Thumbnails enabled.")
    elif arg in ["off", "disable"]:
        await db.set_thumbnail_status(chat_id, False)
        reply = await msg.reply_text("❌ Thumbnails disabled.")
    else:
        reply = await msg.reply_text(
            "⚠️ Invalid command usage.\n"
            "Correct usage: <code>/thumbnail [enable|disable|on|off]</code>"
        )
    if isinstance(reply, types.Error):
        LOGGER.warning(reply.message)
