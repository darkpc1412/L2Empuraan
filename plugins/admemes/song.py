from __future__ import unicode_literals

import os
import requests
import aiohttp
import yt_dlp
import asyncio
import math
import time

import wget
import aiofiles

from pyrogram import filters, Client
from pyrogram.errors import FloodWait, MessageNotModified
from pyrogram.types import Message
from youtube_search import YoutubeSearch
from youtubesearchpython import SearchVideos
from yt_dlp import YoutubeDL
import youtube_dl
import requests

def time_to_seconds(time):
    stringt = str(time)
    return sum(int(x) * 60 ** i for i, x in enumerate(reversed(stringt.split(':'))))


@Client.on_message(filters.command('song') & ~filters.private & ~filters.channel)
def song(client, message):

    user_id = message.from_user.id 
    user_name = message.from_user.first_name 
    rpk = "["+user_name+"](tg://user?id="+str(user_id)+")"

    query = ''
    for i in message.command[1:]:
        query += ' ' + str(i)
    print(query)
    m = message.reply("**𝕾𝖊𝖆𝖗𝖈𝖍𝖎𝖓𝖌 𝖄𝖔𝖚𝖗 𝕾𝖔𝖓𝖌...!**")
    ydl_opts = {"format": "bestaudio[ext=m4a]"}
    try:
        results = YoutubeSearch(query, max_results=1).to_dict()
        link = f"https://youtube.com{results[0]['url_suffix']}"
        #print(results)
        title = results[0]["title"][:40]       
        thumbnail = results[0]["thumbnails"][0]
        thumb_name = f'thumb{title}.jpg'
        thumb = requests.get(thumbnail, allow_redirects=True)
        open(thumb_name, 'wb').write(thumb.content)


        performer = f"[𝖕𝖍𝖔𝖊𝖓𝖎𝖝]" 
        duration = results[0]["duration"]
        url_suffix = results[0]["url_suffix"]
        views = results[0]["views"]

    except Exception as e:
        m.edit(
            "**𝕱𝖔𝖚𝖓𝖉 𝕹𝖔𝖙𝖍𝖎𝖓𝖌  𝕻𝖑𝖊𝖆𝖘𝖊 𝕮𝖔𝖗𝖗𝖊𝖈𝖙 𝕿𝖍𝖊 𝕾𝖕𝖊𝖑𝖑𝖎𝖓𝖌 𝕺𝖗 𝕾𝖊𝖆𝖗𝖈𝖍 𝕬𝖓𝖞 𝕺𝖙𝖍𝖊𝖗 𝕾𝖔𝖓𝖌**"
        )
        print(str(e))
        return
    m.edit("**𝕯𝖔𝖜𝖓𝖑𝖔𝖆𝖉𝖎𝖓𝖌 𝖄𝖔𝖚𝖗 𝕾𝖔𝖓𝖌...!**")
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(link, download=False)
            audio_file = ydl.prepare_filename(info_dict)
            ydl.process_info(info_dict)
        rep = '**𝕾𝖚𝖇𝖘𝖈𝖗𝖎𝖇𝖊 ›› [𝐌𝐎𝐕𝐈𝐄 𝐂𝐋𝐔𝐁 📺🎥](https://t.me/mnxmovies124)**\n**𝕻𝖔𝖜𝖊𝖗𝖊𝖉 𝕭𝖞 ›› [𝐂𝐋𝐔𝐁 𝐇𝐎𝐔𝐒𝐄 🎬](https://t.me/movieclub1241)**'
        secmul, dur, dur_arr = 1, 0, duration.split(':')
        for i in range(len(dur_arr)-1, -1, -1):
            dur += (int(dur_arr[i]) * secmul)
            secmul *= 60
        message.reply_audio(audio_file, caption=rep, parse_mode='md',quote=False, title=title, duration=dur, performer=performer, thumb=thumb_name)
        m.delete()
    except Exception as e:
        m.edit("**🚫 𝙴𝚁𝚁𝙾𝚁 🚫**")
        print(e)

    try:
        os.remove(audio_file)
        os.remove(thumb_name)
    except Exception as e:
        print(e)

def get_text(message: Message) -> [None,str]:
    text_to_return = message.text
    if message.text is None:
        return None
    if " " not in text_to_return:
        return None
    try:
        return message.text.split(None, 1)[1]
    except IndexError:
        return None


@Client.on_message(filters.command(["video", "mp4"]))
async def vsong(client, message: Message):
    urlissed = get_text(message)

    pablo = await client.send_message(
        message.chat.id, f"**𝕱𝖎𝖓𝖉𝖎𝖓𝖌 𝖄𝖔𝖚𝖗 𝖁𝖎𝖉𝖊𝖔** `{urlissed}`"
    )
    if not urlissed:
        await pablo.edit("Invalid Command Syntax Please Check help Menu To Know More!")
        return

    search = SearchVideos(f"{urlissed}", offset=1, mode="dict", max_results=1)
    mi = search.result()
    mio = mi["search_result"]
    mo = mio[0]["link"]
    thum = mio[0]["title"]
    fridayz = mio[0]["id"]
    mio[0]["channel"]
    kekme = f"https://img.youtube.com/vi/{fridayz}/hqdefault.jpg"
    await asyncio.sleep(0.6)
    url = mo
    sedlyf = wget.download(kekme)
    opts = {
        "format": "best",
        "addmetadata": True,
        "key": "FFmpegMetadata",
        "prefer_ffmpeg": True,
        "geo_bypass": True,
        "nocheckcertificate": True,
        "postprocessors": [{"key": "FFmpegVideoConvertor", "preferedformat": "mp4"}],
        "outtmpl": "%(id)s.mp4",
        "logtostderr": False,
        "quiet": True,
    }
    try:
        with YoutubeDL(opts) as ytdl:
            ytdl_data = ytdl.extract_info(url, download=True)
    except Exception as e:
        await event.edit(event, f"**𝕯𝖔𝖜𝖓𝖑𝖔𝖆𝖉 𝕱𝖆𝖎𝖑𝖊𝖉 𝕻𝖑𝖊𝖆𝖘𝖊 𝕿𝖗𝖞 𝕬𝖌𝖆𝖎𝖓..♥️** \n**Error :** `{str(e)}`")
        return
    c_time = time.time()
    file_stark = f"{ytdl_data['id']}.mp4"
    capy = f"""
**𝕿𝖎𝖙𝖑𝖊 :** [{thum}]({mo})
**𝕽𝖊𝖖𝖚𝖊𝖘𝖙𝖊𝖉 𝕭𝖞 :** {message.from_user.mention}
"""
    await client.send_video(
        message.chat.id,
        video=open(file_stark, "rb"),
        duration=int(ytdl_data["duration"]),
        file_name=str(ytdl_data["title"]),
        thumb=sedlyf,
        caption=capy,
        supports_streaming=True,        
        reply_to_message_id=message.message_id 
    )
    await pablo.delete()
    for files in (sedlyf, file_stark):
        if files and os.path.exists(files):
            os.remove(files)

