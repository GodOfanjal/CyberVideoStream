from random import randint
from pyrogram.types import Message
from pyrogram import Client, filters
from pyrogram.raw.types import InputGroupCall
from pyrogram.errors import UserAlreadyParticipant
from pyrogram.raw.functions.phone import CreateGroupCall
from lib.config import USERNAME_BOT
from lib.tg_stream import app as USER
from lib.helpers.filters import private_filters, public_filters


@Client.on_message(filters.command(["join", "join@{USERNAME_BOT}"]) & public_filters)
async def join(client, message):
    chat_id = message.chat.id
    try:
        link = await client.export_chat_invite_link(chat_id)
    except BaseException:
        await message.reply("**Error:**\nAdd me as admin of your group!")
        return
    try:
        await USER.join_chat(link)
        await message.reply("**Userbot Joined**")
    except UserAlreadyParticipant:
        await message.reply("**Userbot Already Participant**")


@Client.on_message(filters.command(["opengc", "opengc@{USERNAME_BOT"]) & public_filters)
async def opengc(client, message):
    flags = " ".join(message.command[1:])
    channel_id = message.chat.title
    chat_id = message.chat.id
    try:
        if flags == "channel":
            await USER.send(CreateGroupCall(peer=(await USER.resolve_peer(int(channel_id))), random_id=randint(10000, 999999999)))
            await message.reply("**Voice chat started!**")
        else:
            await USER.send(CreateGroupCall(peer=(await USER.resolve_peer(chat_id)), random_id=randint(10000, 999999999)))
            await message.reply("**Voice chat channel started!**")
    except Exception:
        await message.reply("**Error:** Add userbot as admin of your group/channel with permission **Can manage voice chat**")
