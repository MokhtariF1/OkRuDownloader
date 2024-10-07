from telethon import TelegramClient, events, Button
import config
import requests


if config.proxy is False:

    proxy = None

else:

    proxy = config.proxy_address

print("connecting...")
print(proxy)
bot = TelegramClient("bot", config.api_id, config.api_hash, proxy=proxy)

bot.start(bot_token=config.bot_token)

print("connected!")


@bot.on(events.NewMessage())
async def msg(event):
    user_id = event.sender_id
    text = event.raw_text
    bot_text = config.FA_TEXT
    if text == "/start":
        keys = [
            [
                Button.text(bot_text["get"], resize=1)
            ],
            [
                Button.text(bot_text["user_info"], resize=1),
                Button.text(bot_text["settings"], resize=1)
            ]
        ]
        await event.reply(bot_text["start"], buttons=keys)
    elif text == bot_text["get"]:
        keys = [
            [
                Button.text(bot_text["video"], resize=1),
                Button.text(bot_text["direct_link"])
            ],
            [
                Button.text(bot_text["back"])
            ]
        ]
        await event.reply(bot_text["select"], buttons=keys)
    elif text == bot_text["video"]:
        async with bot.conversation(user_id, timeout=1000) as conv:
            await conv.send_message(bot_text["enter_link"])
            get_url = await conv.get_response()
            keys = [
                [
                    Button.inline("mobile", b'mobile')
                ],
                [
                    Button.inline("lowest", b'lowest'),
                ],
                [
                    Button.inline("low", b'low'),
                ],
                [
                    Button.inline("sd", b'sd'),
                ],
                [
                    Button.inline("hd", b'hd'),
                ],
            ]
            await conv.send_message(bot_text["select_quality"], buttons=keys)
            quality = await conv.wait_event(events.CallbackQuery())
            quality = quality.data.decode()
            url = config.api_address + f"download?url={get_url.raw_text}&quality={quality}"
            dn = await conv.send_message(bot_text["downloading"])
            response = requests.post(url)
            response = response.json()
            response_status = response.get("status")
            print(response_status)
            if response_status != 200:
                await bot.delete_messages(user_id, dn.msg_id)
                await conv.send_message(bot_text["error"])
                return
            else:
                await bot.edit_message(user_id, dn.msg_id, bot_text["uploading"])
                path = response["path"]
                await event.reply(str(path).split("/")[1], file=path)


bot.run_until_disconnected()