import asyncio
import telegram

# token account telegram
my_token = "6768843655:AAGL_HDuThL7UgouNQ1fXsefZYSs3O-4uGI"
my_chatid = '-1001996069923'

# create Bot
bot = telegram.Bot(token=my_token)

# send text message


async def send_telegram(photo_path="./data/alert.png"):
    try:
        await bot.sendPhoto(chat_id=my_chatid, photo=open(
            photo_path, "rb"), caption="Có người đang đứng ở quầy hàng!!!")
        print("Send sucess")
    except Exception as ex:
        print("Can not send message telegram ", ex)