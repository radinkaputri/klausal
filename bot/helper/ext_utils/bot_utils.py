from httpx import AsyncClient
from random import choice
from asyncio import (
    create_subprocess_exec,
    create_subprocess_shell,
    run_coroutine_threadsafe,
    sleep,
)
from asyncio.subprocess import PIPE
from pyrogram.types import BotCommand
from functools import partial, wraps
from concurrent.futures import ThreadPoolExecutor
from aiohttp import ClientSession

from bot import user_data, config_dict, bot_loop, OWNER_ID
from bot.helper.ext_utils.help_messages import YT_HELP_DICT, MIRROR_HELP_DICT
from bot.helper.telegram_helper.button_build import ButtonMaker
from bot.helper.ext_utils.telegraph_helper import telegraph
from bot.helper.telegram_helper.bot_commands import BotCommands

THREADPOOL = ThreadPoolExecutor(max_workers=1000)

COMMAND_USAGE = {}


class setInterval:
    def __init__(self, interval, action, *args, **kwargs):
        self.interval = interval
        self.action = action
        self.task = bot_loop.create_task(self._set_interval(*args, **kwargs))

    async def _set_interval(self, *args, **kwargs):
        while True:
            await sleep(self.interval)
            await self.action(*args, **kwargs)

    def cancel(self):
        self.task.cancel()

async def delete_links(message):
    if message.from_user.id == OWNER_ID and message.chat.type == message.chat.type.PRIVATE:
        return

    if config_dict['DELETE_LINKS']:
        try:
            if reply_to := message.reply_to_message:
                await reply_to.delete()
                await message.delete()
            else:
                await message.delete()
        except Exception as e:
            LOGGER.error(str(e))

def create_help_buttons():
    buttons = ButtonMaker()
    for name in list(MIRROR_HELP_DICT.keys())[1:]:
        buttons.ibutton(name, f"help m {name}")
    buttons.ibutton("Close", f"help close")
    COMMAND_USAGE["mirror"] = [MIRROR_HELP_DICT["main"], buttons.build_menu(3)]
    buttons.reset()
    for name in list(YT_HELP_DICT.keys())[1:]:
        buttons.ibutton(name, f"help yt {name}")
    buttons.ibutton("Close", f"help close")
    COMMAND_USAGE["yt"] = [YT_HELP_DICT["main"], buttons.build_menu(3)]


def bt_selection_buttons(id_):
    gid = id_[:12] if len(id_) > 20 else id_
    pincode = "".join([n for n in id_ if n.isdigit()][:4])
    buttons = ButtonMaker()
    BASE_URL = config_dict["BASE_URL"]
    if config_dict["WEB_PINCODE"]:
        buttons.ubutton("Select Files", f"{BASE_URL}/app/files/{id_}")
        buttons.ibutton("Pincode", f"btsel pin {gid} {pincode}")
    else:
        buttons.ubutton(
            "Select Files", f"{BASE_URL}/app/files/{id_}?pin_code={pincode}"
        )
    buttons.ibutton("Done Selecting", f"btsel done {gid} {id_}")
    buttons.ibutton("Cancel", f"btsel cancel {gid}")
    return buttons.build_menu(2)


async def get_telegraph_list(telegraph_content):
    path = [
        (
            await telegraph.create_page(
                title="𝚇𝚈𝚁𝙰𝙳 𝙳𝚁𝙸𝚅𝙴 𝚂𝙴𝙰𝚁𝙲𝙷", content=content
            )
        )["path"]
        for content in telegraph_content
    ]
    if len(path) > 1:
        await telegraph.edit_telegraph(path, telegraph_content)
    buttons = ButtonMaker()
    buttons.ubutton("🔎 VIEW", f"https://telegra.ph/{path[0]}")
    return buttons.build_menu(1)

async def set_commands(client):
    await client.set_bot_commands([
        BotCommand(
            f"{BotCommands.StartCommand}",
            "Start the bot and get basic information."
        ),
        BotCommand(
            f"{BotCommands.MirrorCommand[0]}",
            f"or /{BotCommands.MirrorCommand[1]} to mirror links and files to the cloud."
        ),
        BotCommand(
            f"{BotCommands.QbMirrorCommand[0]}",
            f"or /{BotCommands.QbMirrorCommand[1]} to mirror links with qBittorrent."
        ),
        BotCommand(
            f"{BotCommands.YtdlCommand[0]}",
            f"or /{BotCommands.YtdlCommand[1]} to mirror links supported by yt-dlp."
        ),
        BotCommand(
            f"{BotCommands.LeechCommand[0]}",
            f"or /{BotCommands.LeechCommand[1]} to leech links and files to Telegram."
        ),
        BotCommand(
            f"{BotCommands.QbLeechCommand[0]}",
            f"or /{BotCommands.QbLeechCommand[1]} to leech links using qBittorrent."
        ),
        BotCommand(
            f"{BotCommands.YtdlLeechCommand[0]}",
            f"or /{BotCommands.YtdlLeechCommand[1]} to leech links supported by yt-dlp."
        ),
        BotCommand(
            f"{BotCommands.CloneCommand[0]}",
            f"or /{BotCommands.CloneCommand[1]} to copy files or folders to Google Drive."
        ),
        BotCommand(
            f"{BotCommands.CountCommand}",
            "[Drive URL]: to count files or folders in Google Drive."
        ),
        BotCommand(
            f"{BotCommands.StatusCommand}",
            "to get the status of all tasks."
        ),
        BotCommand(
            f"{BotCommands.StatsCommand}",
            "to check bot statistics."
        ),
        BotCommand(
            f"{BotCommands.CancelTaskCommand[0]}",
            f"or /{BotCommands.CancelTaskCommand[1]} to cancel a task."
        ),
        BotCommand(
            f"{BotCommands.CancelAllCommand}",
            "to cancel all tasks added by you."
        ),
        BotCommand(
            f"{BotCommands.ListCommand}",
            "to search for something in Google Drive."
        ),
        BotCommand(
            f"{BotCommands.SearchCommand}",
            "to search for something on torrent sites."
        ),
        BotCommand(
            f"{BotCommands.UserSetCommand[0]}",
            f"or /{BotCommands.UserSetCommand[1]} to access user settings."
        ),
        BotCommand(
            f"{BotCommands.HelpCommand}",
            "to get complete assistance."
        ),
        BotCommand(
            f"{BotCommands.SpeedCommand}",
            "Check the speed of the bot's host."
        ),
    ])

def safemode_message():
    messages = [
        "The future feels so uncertain. Will I find my way?",
        "What if my dreams fade away as life changes?",
        "Sometimes, expectations feel too heavy. Will I know what I want?",
        "I'm scared of making the wrong choices for my future.",
        "Will I ever find true happiness, or will I always be searching?",
        "The pressure to succeed is real. What if I fall short?",
        "I worry that I’ll get stuck in a routine and miss out on life.",
        "What if I choose a path and realize it's not for me?",
        "Can I really trust myself to make the right decisions?",
        "The future seems so far away, yet it feels like it’s closing in."
    ]
    return choice(messages)

def arg_parser(items, arg_base):
    if not items:
        return arg_base
    bool_arg_set = {"-b", "-e", "-z", "-s", "-j", "-d", "-sv", "-ss"}
    t = len(items)
    i = 0
    arg_start = -1

    while i + 1 <= t:
        part = items[i]
        if part in arg_base:
            if arg_start == -1:
                arg_start = i
            if i + 1 == t and part in bool_arg_set or part in ["-s", "-j"]:
                arg_base[part] = True
            else:
                sub_list = []
                for j in range(i + 1, t):
                    item = items[j]
                    if item in arg_base:
                        if part in bool_arg_set and not sub_list:
                            arg_base[part] = True
                        break
                    sub_list.append(item)
                    i += 1
                if sub_list:
                    arg_base[part] = " ".join(sub_list)
        i += 1
    link = []
    if items[0] not in arg_base:
        if arg_start == -1:
            link.extend(iter(items))
        else:
            link.extend(items[r] for r in range(arg_start))
        if link:
            arg_base["link"] = " ".join(link)
    return arg_base


async def get_content_type(url):
    try:
        async with AsyncClient() as client:
            response = await client.get(url, allow_redirects=True, verify=False)
            return response.headers.get("Content-Type")
    except:
        return None


def update_user_ldata(id_, key, value):
    user_data.setdefault(id_, {})
    user_data[id_][key] = value


async def cmd_exec(cmd, shell=False):
    if shell:
        proc = await create_subprocess_shell(cmd, stdout=PIPE, stderr=PIPE)
    else:
        proc = await create_subprocess_exec(*cmd, stdout=PIPE, stderr=PIPE)
    stdout, stderr = await proc.communicate()
    stdout = stdout.decode().strip()
    stderr = stderr.decode().strip()
    return stdout, stderr, proc.returncode


def new_task(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return bot_loop.create_task(func(*args, **kwargs))

    return wrapper


async def sync_to_async(func, *args, wait=True, **kwargs):
    pfunc = partial(func, *args, **kwargs)
    future = bot_loop.run_in_executor(THREADPOOL, pfunc)
    return await future if wait else future


def async_to_sync(func, *args, wait=True, **kwargs):
    future = run_coroutine_threadsafe(func(*args, **kwargs), bot_loop)
    return future.result() if wait else future


def new_thread(func):
    @wraps(func)
    def wrapper(*args, wait=False, **kwargs):
        future = run_coroutine_threadsafe(func(*args, **kwargs), bot_loop)
        return future.result() if wait else future

    return wrapper
