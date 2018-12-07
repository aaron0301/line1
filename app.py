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
def KeyWord(text):
    KeyWordDict = {"你好":"我很好","你是誰":"才不告訴逆雷","故少":"臭ㄈㄓ","顧少":"臭ㄈㄓ","幹":"幹屁幹臭ㄈㄓ","靠北":"對 就是在靠北","臭":"你才臭"}
    for k in KeyWordDict.keys():
	    if text.find(k) != -1:
		    return[True,KeyWordDict[k]]
    return[False]
def Reply(event):
    Ktemp = KeyWord(event.message.text)
    if Ktemp[0]:
        line_bot_api.reply_message(event.reply_token,
           TextSendMessage(text = Ktemp[1]))
    else:
	    line_bot_api.reply_message(event.reply_token,
           TextSendMessage(text = event.message.text))
def Button(event):
    message = TemplateSendMessage(
        alt_text='Buttons template',
        template=ButtonsTemplate(
        thumbnail_image_url='https://example.com/image.jpg',
        title=text,
        text='快選擇阿',
        actions=[
            PostbackTemplateAction(
                label='選項一',
                text='postback text',
                data='action=buy&itemid=1'
            ),
            MessageTemplateAction(
                label='選項二',
                text='message text'
            ),
            URITemplateAction(
                label='姑狗一波',
                uri='http://google.com/'
            )
        ]
    )
)
    line_bot_api.reply_message(event.reply_token, message)


# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    try:
	    Button(event)
	    #Reply(event)
    except Exception as e:
	    line_bot_api.reply_message(event.reply_token,
		    TextSendMessage(text=str(e)))
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
