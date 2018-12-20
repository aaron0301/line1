from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi('1bQnym3SrZ8xpxNSCAEHfoz9ak01Z5rxcyvSRD2GiaXs62xxNjWV9IXef0Bo1SlndyroOpSyx/Yd5eOfXltMFk39Gaz5ybbnyvnsD13ljBPENhqwjRTKmrUptiFr04PiGcDM+V9Nbmh7PreGwe9WDgdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('96ce5c52eeddbec9448ff852389f017a')

# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'
###========================================
#會員系統
def GetUserlist():
    userlist = {}
    file = open('users','r')
    while True :
        temp = file.readline().strip().split(',')
        if temp[0] == "" : break
        userlist[temp[0]] = temp[1]
    file.close()
    return userlist

#登入系統
def Login(event,userlist):
    i = 0
    for user in userlist.keys():
        if event.source.user_id == user:
            return i
        i+=1
    return -1

#寫入資料
def Update(userlist):
    file = open('users','w')
    for user in userlist.keys():
        file.write(user+','+userlist[user])
    file.close()
#關鍵字系統
def Keyword(event):
    KeyWordDict = {"你好":["text","你也好啊"],
                   "你是誰":["text","我是大帥哥"],
                   "差不多了":["text","讚!!!"],
                   "帥":["sticker",'1','120']}

    for k in KeyWordDict.keys():
        if event.message.text.find(k) != -1:
            if KeyWordDict[k][0] == "text":
                line_bot_api.reply_message(event.reply_token,TextSendMessage(text = KeyWordDict[k][1]))
            elif KeyWordDict[k][0] == "sticker":
                line_bot_api.reply_message(event.reply_token,StickerSendMessage(
                    package_id=KeyWordDict[k][1],
                    sticker_id=KeyWordDict[k][2]))
            return True
    return False

#按鈕版面系統
def Button(event):
    return TemplateSendMessage(
        alt_text='特殊訊息，請進入手機查看',
        template=ButtonsTemplate(
            thumbnail_image_url='https://i.imgur.com/UWMxQ8g.jpg',
            title='瑋桓是?',
            text='快選擇阿',
            actions=[
                PostbackTemplateAction(
                    label='bug',
                    data='bug'
                ),
                MessageTemplateAction(
                    label='87',
                    text='87'               
                ),
                URITemplateAction(
                    label='不知道只好google',
                    uri='https://www.google.com/'
                )
               
             ]
        )
    )

#指令系統，若觸發指令會回傳True
def Command(event):
    tempText = event.message.text.split(",")
    if tempText[0] == "發送" and event.source.user_id == "U95418ebc4fffefdd89088d6f9dabd75b":
        line_bot_api.push_message(tempText[1], TextSendMessage(text=tempText[2]))
        return True
    else:
        return False
#新增一個參數
def Reply(event,userlist):
    if not Command(event):
        Ktemp = KeyWord(event)
        if Ktemp[0]:
            line_bot_api.reply_message(event.reply_token,
                TextSendMessage(text = Ktemp[1]))
        else:
            if userlist[event.source.user_id] == '-1':
                line_bot_api.reply_message(event.reply_token,
                    TextSendMessage(text = "你知道台灣最稀有、最浪漫的鳥是哪一種鳥嗎？"))
                userlist[event.source.user_id] = '0'
            else:
                if event.message.text == "黑面琵鷺":
                    line_bot_api.reply_message(event.reply_token,
                        TextSendMessage(text = "你居然知道答案!!!"))
                else:
                    line_bot_api.reply_message(event.reply_token,
                        TextSendMessage(text = "答案是：黑面琵鷺!!!因為每年冬天，他們都會到台灣來\"壁咚\""))
                userlist[event.source.user_id] = '-1'
#回覆函式，指令 > 關鍵字 > 按鈕
def Reply(event):
    if not Command(event):
        if not Keyword(event):
            Button(event)

# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    try:
        Reply(event)
        '''
        line_bot_api.push_message("Ub0778ded2c8eff813455c5a270089f46", TextSendMessage(text=event.source.user_id + "說:"))
        line_bot_api.push_message("Ub0778ded2c8eff813455c5a270089f46", TextSendMessage(text=event.message.text))
        '''
    except Exception as e:
        line_bot_api.reply_message(event.reply_token, 
            TextSendMessage(text=str(e)))

#處理Postback
@handler.add(PostbackEvent)
def handle_postback(event):
    command = event.postback.data.split(',')
    if command[0] == "bug":
        line_bot_api.reply_message(event.reply_token, 
            TextSendMessage(text="你說的沒錯~~~"))
        
@handler.add(MessageEvent, message=StickerMessage)
def handle_sticker_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        StickerSendMessage(
            package_id='1',
            sticker_id='410')
    )

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
