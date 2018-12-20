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
#關鍵字系統
def Keyword(event):
    KeyWordDict = {"你好":"我很好","你是誰":"才不告訴逆雷","故少":"臭ㄈㄓ","顧少":"臭ㄈㄓ","幹":"幹屁幹臭ㄈㄓ","靠北":"對 就是在靠北","臭":"你才臭"}

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
        line_bot_api.push_message("Ub0778ded2c8eff813455c5a270089f46", TextSendMessage(text=event.source.user_id))
        line_bot_api.push_message("Ub0778ded2c8eff813455c5a270089f46", TextSendMessage(text=event.message.text))
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
            package_id=event.message.package_id,
            sticker_id=event.message.sticker_id)
    )	   
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)