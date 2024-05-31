#(c) Ansh - Vachhani

import os
import asyncio
from asyncio import TimeoutError
from biisal.bot import StreamBot
from biisal.utils.database import Database
from biisal.utils.human_readable import humanbytes
from biisal.vars import Var
# from urllib.parse import quote_plus
from pyrogram import filters, Client
from pyrogram.errors import FloodWait, UserNotParticipant
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from shortzy import Shortzy

from urllib.parse import quote as quote_plus

MY_PASS = os.environ.get("MY_PASS", None)
pass_dict = {}
pass_db = Database(Var.DATABASE_URL, "ag_passwords")

from biisal.utils.file_properties import get_name, get_hash, get_media_file_size
db = Database(Var.DATABASE_URL, Var.name)
BIN_CHANNEL = -1001832234721

@StreamBot.on_message((filters.private) & (filters.document | filters.video | filters.audio | filters.photo) , group=4)
async def private_receive_handler(c: Client, m: Message):

    if m.from_user.id not in Var.ADMINS and not Var.USERS_CAN_USE:
        return

    if not await db.is_user_exist(m.from_user.id):
        await db.add_user(m.from_user.id)
        await c.send_message(
            Var.BIN_CHANNEL,
            f"New User Joined! : \n\n Name : [{m.from_user.first_name}](tg://user?id={m.from_user.id}) Started Your Bot!!"
        )
    if Var.UPDATES_CHANNEL != "None":
        try:
            user = await c.get_chat_member(Var.UPDATES_CHANNEL, m.chat.id)
            if user.status == "kicked":
                await c.send_message(
                    chat_id=m.chat.id,
                    text="You are banned!",
                    
                    disable_web_page_preview=True
                )
                return 
        except UserNotParticipant:
            await c.send_message(
                chat_id=m.chat.id,
                text="""<i>𝙹𝙾𝙸𝙽 UPDATES CHANNEL 𝚃𝙾 𝚄𝚂𝙴 𝙼𝙴 🔐</i>""",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton("Jᴏɪɴ ɴᴏᴡ 🔓", url=f"https://t.me/{Var.UPDATES_CHANNEL}")
                        ]
                    ]
                ),
                
            )
            return
        except Exception as e:
            await m.reply_text(e)
            await c.send_message(
                chat_id=m.chat.id,
                text="**Sᴏᴍᴇᴛʜɪɴɢ ᴡᴇɴᴛ Wʀᴏɴɢ. Cᴏɴᴛᴀᴄᴛ ᴍʏ ʙᴏss** [Adarsh Goel](https://github.com/adarsh-goel)",
                
                disable_web_page_preview=True)
            return
    try:
        user = await db.get_user(m.from_user.id)
        log_msg = await m.forward(chat_id=Var.BIN_CHANNEL)

        og_stream_link = f"{Var.URL}watch/{get_hash(log_msg)}{str(log_msg.id)}"
        stream_link = await short_link(og_stream_link, user)

        og_online_link = f"{Var.URL}{str(log_msg.id)}/{quote_plus(get_name(log_msg))}?hash={get_hash(log_msg)}"
        online_link = await short_link(og_online_link, user) if Var.IS_DISPLAY_DL_LINK else stream_link

        msg_text ="""<i><u>𝗬𝗼𝘂𝗿 𝗟𝗶𝗻𝗸 𝗚𝗲𝗻𝗲𝗿𝗮𝘁𝗲𝗱 !</u></i>\n\n<b>📂 Fɪʟᴇ ɴᴀᴍᴇ :</b> <i>{}</i>\n\n<b>📦 Fɪʟᴇ ꜱɪᴢᴇ :</b> <i>{}</i>\n\n<b>📥 Dᴏᴡɴʟᴏᴀᴅ / 🖥WATCH :</b> <i>{}</i>\n\n<b>🚸 Nᴏᴛᴇ : LINK WON'T EXPIRE TILL I DELETE</b>"""

        await log_msg.reply_text(text=f"**RᴇQᴜᴇꜱᴛᴇᴅ ʙʏ :** [{m.from_user.first_name}](tg://user?id={m.from_user.id})\n**Uꜱᴇʀ ɪᴅ :** `{m.from_user.id}`\n**Stream ʟɪɴᴋ :** {og_stream_link}", disable_web_page_preview=True,  quote=True)
        await m.reply_text(
            text=msg_text.format(get_name(log_msg), humanbytes(get_media_file_size(m)), online_link),
            quote=True,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("📥 Dᴏᴡɴʟᴏᴀᴅ / STREAM 🖥", url=stream_link)]]) #Download Link
        )
    except FloodWait as e:
        print(f"Sleeping for {str(e.x)}s")
        await asyncio.sleep(e.x)
        await c.send_message(chat_id=Var.BIN_CHANNEL, text=f"Gᴏᴛ FʟᴏᴏᴅWᴀɪᴛ ᴏғ {str(e.x)}s from [{m.from_user.first_name}](tg://user?id={m.from_user.id})\n\n**𝚄𝚜𝚎𝚛 𝙸𝙳 :** `{str(m.from_user.id)}`", disable_web_page_preview=True)


@StreamBot.on_message(filters.channel & ~filters.group & (filters.document | filters.video | filters.photo)  & ~filters.forwarded, group=-1)
async def channel_receive_handler(bot, broadcast):

    if int(broadcast.chat.id) in Var.BANNED_CHANNELS:
        await bot.leave_chat(broadcast.chat.id)

        return
    try:
        log_msg = await broadcast.forward(chat_id=BIN_CHANNEL)
        await asyncio.sleep(1)        
        og_stream_link = f"{Var.URL}watch/{str(log_msg.id)}/{quote_plus(get_name(log_msg))}?hash={get_hash(log_msg)}"
        stream_link = await short_link(og_stream_link)
        oi_stream_link = f"{get_hash(log_msg)}{str(log_msg.id)}"
        og_online_link = f"{Var.URL}{str(log_msg.id)}/{quote_plus(get_name(log_msg))}?hash={get_hash(log_msg)}"
        online_link = await short_link(og_online_link) if Var.IS_DISPLAY_DL_LINK else stream_link        
        caption=f"{oi_stream_link}"
        await bot.edit_message_caption(
            chat_id=broadcast.chat.id,
            message_id=broadcast.id,
            caption=caption            
        )
    except FloodWait as w:
        print(f"Sleeping for {str(w.x)}s")
        await asyncio.sleep(w.x)
        


async def short_link(link, user=None):
    if not user:
        return link

    # encoded_url = quote(link, safe='/:?=')
    api_key = user.get("shortener_api")
    base_site = user.get("base_site")

    if bool(api_key and base_site) and Var.USERS_CAN_USE:
        shortzy = Shortzy(api_key, base_site)
        link = await shortzy.convert(link)

    return link
