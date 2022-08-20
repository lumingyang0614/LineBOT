import os
import re
import json
import random
from dotenv import load_dotenv
from pyquery import PyQuery
from fastapi import FastAPI, Request, HTTPException
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *

load_dotenv() # Load your local environment variables


CHANNEL_TOKEN = os.environ.get('LINE_TOKEN')
CHANNEL_SECRET = os.getenv('LINE_SECRET')

app = FastAPI()

My_LineBotAPI = LineBotApi(CHANNEL_TOKEN) # Connect Your API to Line Developer API by Token
handler = WebhookHandler(CHANNEL_SECRET) # Event handler connect to Line Bot by Secret key

CHANNEL_ID = os.getenv('LINE_UID') # For any message pushing to or pulling from Line Bot using this ID

# Create my emoji list
my_emoji = [
    [{'index':27, 'productId':'5ac1bfd5040ab15980c9b435', 'emojiId':'005'}],
    [{'index':27, 'productId':'5ac1bfd5040ab15980c9b435', 'emojiId':'019'}],
    [{'index':27, 'productId':'5ac1bfd5040ab15980c9b435', 'emojiId':'096'}]
]
my_event = ['#help']
# Line Developer Webhook Entry Point
@app.post('/')
async def callback(request: Request):
    body = await request.body() # Get request
    signature = request.headers.get('X-Line-Signature', '') # Get message signature from Line Server
    try:
        handler.handle(body.decode('utf-8'), signature) # Handler handle any message from LineBot and 
    except InvalidSignatureError:
        raise HTTPException(404, detail='LineBot Handle Body Error !')
    return 'OK'

# All message events are handling at here !
@handler.add(MessageEvent, message=TextMessage)
def handle_textmessage(event):
    recieve_message = str(event.message.text).split(' ')
    # Get first splitted message as command
    case_ = recieve_message[0].lower().strip()
    # Case 1: get pokemon
    if recieve_message[0].isdigit():
        if(recieve_message[2].isdigit()):
            strcal = recieve_message[1] 
            if(strcal == '+'):
                ans = int(recieve_message[0]) + int(recieve_message[2])
                My_LineBotAPI.reply_message(
                    event.reply_token,
                    TextSendMessage(text=ans)
                )
            elif(strcal == '*'):
                ans = int(recieve_message[0]) * int(recieve_message[2])
                My_LineBotAPI.reply_message(
                    event.reply_token,
                    TextSendMessage(text=ans)
                )
            elif(strcal == '-'):
                ans = int(recieve_message[0]) - int(recieve_message[2])
                My_LineBotAPI.reply_message(
                    event.reply_token,
                    TextSendMessage(text=ans)
                )
            elif(strcal == '/'):
                if(recieve_message[2] != '0'):
                    ans = int(recieve_message[0]) / int(recieve_message[2])
                    My_LineBotAPI.reply_message(
                        event.reply_token,
                        TextSendMessage(text=ans)
                    )
                else:
                    My_LineBotAPI.reply_message(
                        event.reply_token,
                        TextSendMessage(text='b can not be 0 ')
                    )
            else:
                My_LineBotAPI.reply_message(
                    event.reply_token,
                    TextSendMessage(text='Error, please try again. #help have Directions')
                )
        else:
            My_LineBotAPI.reply_message(
                event.reply_token,
                TextSendMessage(text='Error, please try again. #help have Directions')
            )
    elif re.match(my_event[0], case_):
        command_describtion = '$ Directions\n\
        A is first number\n\
        B is second number\n\
        A + B -->A plus B\n\
        A - B -->A minus B\n\
        A * B -->A multiply B\n\
        A / B -->A divided by B\n'
        My_LineBotAPI.reply_message(
            event.reply_token,
            TextSendMessage(
                text=command_describtion,
                emojis=[
                    {
                        'index':0,
                        'productId':'5ac21a18040ab15980c9b43e',
                        'emojiId':'110'
                    }
                ]
            )
        )
    else:
        My_LineBotAPI.reply_message(
            event.reply_token,
            TextSendMessage(
                text='$ Welcome ! #help have directions',
                emojis=[
                    {
                        'index':0,
                        'productId':'5ac2213e040ab15980c9b447',
                        'emojiId':'035'
                    }
                ]
            )
        )

# Line Sticker Class
class My_Sticker:
    def __init__(self, p_id: str, s_id: str):
        self.type = 'sticker'
        self.packageID = p_id
        self.stickerID = s_id

'''
See more about Line Sticker, references below
> Line Developer Message API, https://developers.line.biz/en/reference/messaging-api/#sticker-message
> Line Bot Free Stickers, https://developers.line.biz/en/docs/messaging-api/sticker-list/
'''
# Add stickers into my_sticker list
my_sticker = [My_Sticker(p_id='446', s_id='1995'), My_Sticker(p_id='446', s_id='2012'),
     My_Sticker(p_id='446', s_id='2024'), My_Sticker(p_id='446', s_id='2027'),
     My_Sticker(p_id='789', s_id='10857'), My_Sticker(p_id='789', s_id='10877'),
     My_Sticker(p_id='789', s_id='10881'), My_Sticker(p_id='789', s_id='10885'),
     ]

# Line Sticker Event
@handler.add(MessageEvent, message=StickerMessage)
def handle_sticker(event):
    # Random choice a sticker from my_sticker list
    ran_sticker = random.choice(my_sticker)
    # Reply Sticker Message
    My_LineBotAPI.reply_message(
        event.reply_token,
        StickerSendMessage(
            package_id= ran_sticker.packageID,
            sticker_id= ran_sticker.stickerID
        )
    )
if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app='main:app', reload=True, host='0.0.0.0', port=8787)