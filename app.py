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
    KeyWordDict = {"你好":["text","你也好啊"],
                   "你是誰":["text","才不告訴逆雷"],
                   "帥":["sticker",'1','120'],
                   "捷運":["img","https://web.metro.taipei/img/all/routemap2018.jpg"]
                   
                   
                   }

    for k in KeyWordDict.keys():
        if event.message.text.find(k) != -1:
            if KeyWordDict[k][0] == "text":
                line_bot_api.reply_message(event.reply_token,TextSendMessage(text = KeyWordDict[k][1]))
            elif KeyWordDict[k][0] == "sticker":
                line_bot_api.reply_message(event.reply_token,StickerSendMessage(
                    package_id=KeyWordDict[k][1],
                    sticker_id=KeyWordDict[k][2]))
            elif KeyWordDict[k][0] == "img":
                line_bot_api.reply_message(event.reply_token,
                    ImageSendMessage(
                        original_content_url=KeyWordDict[k][1],
                        preview_image_url=KeyWordDict[k][1]
                    )
                )
            return True
    return False

#按鈕版面系統
'''
def Button(event):
    line_bot_api.reply_message(event.reply_token,
        TemplateSendMessage(
            alt_text='特殊訊息，請進入手機查看',
            template=ButtonsTemplate(
                thumbnail_image_url='https://pic.pimg.tw/bwyd67/1471350593-2114545014.jpg',
                title='有沒有認真聽報告?',
                text='還不快點選擇',
                actions=[
                    PostbackTemplateAction(
                        label='有',
                        data='有'
                    ),
                    MessageTemplateAction(
                        label='沒有',
                        text='沒有'
                    ),
                    URITemplateAction(
                        label='google',
                        uri='https://www.google.com.tw/'
                    )
                ]
            )
        )
    )
'''
#指令系統，若觸發指令會回傳True
def Command(event):
    tempText = event.message.text.split(",")
    if tempText[0] == "發送" and event.source.user_id == "Ub0778ded2c8eff813455c5a270089f46":
        line_bot_api.push_message(tempText[1], TextSendMessage(text=tempText[2]))
        return True
    else:
        return False

#回覆函式，指令 > 關鍵字 > 按鈕
def Reply(event):
    if not Command(event):
        Keyword(event)
            

# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    try:
        Reply(event)
        
        line_bot_api.push_message("Ub0778ded2c8eff813455c5a270089f46", TextSendMessage(text=event.source.user_id + "說:"))
        line_bot_api.push_message("Ub0778ded2c8eff813455c5a270089f46", TextSendMessage(text=event.message.text))
        
    except Exception as e:
        line_bot_api.reply_message(event.reply_token, 
            TextSendMessage(text=str(e)))

#處理Postback
'''@handler.add(PostbackEvent)
def handle_postback(event):
    command = event.postback.data.split(',')
    if command[0] == "有":
        line_bot_api.reply_message(event.reply_token, 
            TextSendMessage(text="恩恩很好"))
        
@handler.add(MessageEvent, message=StickerMessage)
def handle_sticker_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        StickerSendMessage(
            package_id=event.message.package_id,
            sticker_id=event.message.sticker_id)
    )
'''
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
