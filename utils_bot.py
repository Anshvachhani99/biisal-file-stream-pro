import logging
import os
import re
import threading
import time
from asyncio import TimeoutError
from pyrogram import filters

LOGGER = logging.getLogger(__name__)
SIZE_UNITS = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']
BLACKLIST_WORDS = ["[Telegram@alpacinodump], www.1TamilMV.dad, @SH_OTT, @New_Movies_1stOnTG", "www_SkymoviesHD", "@Tamil LinkzZ", "@SY MS", "SkymoviesHD", "www 1TamilMV zip", "a8ix live", "@Cinematic_world", "SkymoviesHD", "@MoViEsWeB HeVc", "Filmy4Cab com", "www 7MovieRulz mn", "www 1TamilMV vin", "www 1TamilMV win", "www 1TamilMV cafe", "@ADrama  Lovers", "www 1TamilMV help", "KC", "@CK Moviez", "E4E", "[BindasMovies]", "[Hezz Series]", "[Hezz Movies]", "[CC]", "www Tamilblasters rent", "[CH]", "www 4MovieRulz com", "www TamilBlasters cam", "www Tamilblasters social", "[@The 4x Team]", "@mj link 4u", "[CD]", "@Andhra movies", "@BT MOVIES HD", "@Team_HDT", "Telegram@APDBackup", "Telegram@Alpacinodump", "www 1TamilMV fans", "@Ruraljat Studio", "7HitMovies bio", "[MZM]", "[@UCMOVIE]", "@CC_New", "[MF]", "@Mallu_Movies", "[MC]", "[@MociesVerse]", "@Mm_Linkz", "@BT_MOVIES_HD_@FILMSCLUB04", "www TamilVaathi online", "www 1TamilMV mx", "@BGM LinkzZ", "www 1TamilMV media", "[D&O]", "[MM]", "[", "]", "[FC]", "[CF]", "LinkZz", "[DFBC]", "@New_Movie", "@Infinite_Movies2", "MM", "@R A R B G", "[F&T]", "[KMH]", "[DnO]", "[F&T]", "MLM", "@TM_LMO", "@x265_E4E", "@HEVC MoviesZ", "SSDMovies", "@MM Linkz", "[CC]", "@Mallu_Movies", "@DK Drama", "@luxmv_Linkz", "@Akw_links", "CK HEVC", "@Team_HDT", "[CP]", "www 1TamilMV men", "www TamilRockers", "@MM", "@mm", "[MW]", "@TN68 Linkzz", "@Clipmate_Movie", "[MASHOBUC]", "Official TheMoviesBoss", "www CineVez one", "www 7MovieRulz lv", "www 1TamilMV vip", "[SMM Official]", "[Movie Bazar]", "@BM_Links", "[CG]", "Filmy4wap xyz", "www 1TamilMV pw", "www TamilBlasters pm", "[FH]", "Torrent911 tv", "[MZM]", "www CineVez top", "www CineVez top", "www 7MovieRulz sx", "[YDF]", "www 1TamilMV art", "www TamilBlasters me", "[mwkOTT]", "@Tamil_LinkzZ", "[LV]", "@The_4x_Team", "TheMoviesBoss"]

class setInterval:
    def __init__(self, interval, action):
        self.interval = interval
        self.action = action
        self.stopEvent = threading.Event()
        thread = threading.Thread(target=self.__setInterval)
        thread.start()

    def __setInterval(self):
        nextTime = time.time() + self.interval
        while not self.stopEvent.wait(nextTime - time.time()):
            nextTime += self.interval
            self.action()

    def cancel(self):
        self.stopEvent.set()


def get_readable_file_size(size_in_bytes) -> str:
    if size_in_bytes is None:
        return '0B'
    index = 0
    while size_in_bytes >= 1024:
        size_in_bytes /= 1024
        index += 1
    try:
        return f'{round(size_in_bytes, 2)}{SIZE_UNITS[index]}'
    except IndexError:
        return 'File too large'


def get_readable_time(seconds: int) -> str:
    result = ''
    (days, remainder) = divmod(seconds, 86400)
    days = int(days)
    if days != 0:
        result += f'{days}d'
    (hours, remainder) = divmod(remainder, 3600)
    hours = int(hours)
    if hours != 0:
        result += f'{hours}h'
    (minutes, seconds) = divmod(remainder, 60)
    minutes = int(minutes)
    if minutes != 0:
        result += f'{minutes}m'
    seconds = int(seconds)
    result += f'{seconds}s'
    return result



def readable_time(seconds: int) -> str:
    result = ''
    (days, remainder) = divmod(seconds, 86400)
    days = int(days)
    if days != 0:
        result += f'{days}d'
    (hours, remainder) = divmod(remainder, 3600)
    hours = int(hours)
    if hours != 0:
        result += f'{hours}h'
    (minutes, seconds) = divmod(remainder, 60)
    minutes = int(minutes)
    if minutes != 0:
        result += f'{minutes}m'
    seconds = int(seconds)
    result += f'{seconds}s'
    return result

def replace_username(text):
    prohibited_words = BLACKLIST_WORDS
    big_regex = re.compile('|'.join(map(re.escape, prohibited_words)))
    text = big_regex.sub("", text)

    # Remove usernames
    usernames = re.findall("([@][A-Za-z0-9_]+)", text)
    for username in usernames:
        text = text.replace(username, "")

    # Remove emojis
    
    # Remove multiple spaces with a single space
    text = re.sub(r'\s+', ' ', text).strip()

    return text
