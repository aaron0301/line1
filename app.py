from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
import requests

app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi('6ol/TkzOsx2Ej9mikY8+FU6SegSuiLpMWg8v9aLR+VJ/ERdnRFmEYoLQ2QCXZQb34Mhr5saLpkSH+5FeyQa3zaDekwISNXef8rq8FVSyuSAiSVFiQakv9u9PM6qq3dMrZ7YxbsxB2pyItBZaISwdRgdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('e73f4ba68c0127b885304278fe5fd152')

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

#----------從這裡開始複製----------

#設定帳號class
class user:
    def __init__(self,ID,Name,Situation):
        self.Name = Name
        self.ID = ID
        self.Situation = Situation

#新增一個新使用者
def Signup(user_id,name):
    url = "https://script.google.com/macros/s/AKfycbxn7Slc2_sKHTc6uEy3zmm3Bh_4duiGCXLavUM3RB0a3yzjAxc/exec"
    payload = {
        'sheetUrl':"https://docs.google.com/spreadsheets/d/1kL7p464r_KwUN2RWZrFhBlR7yhaLEgpsxaKAWAR9m6I/edit#gid=0",
        'sheetTag':"工作表1",
        'data':user_id+','+name+',-1'
    }
    requests.get(url, params=payload)

#取得所有會員資料
def GetUserList():
    url = "https://script.google.com/macros/s/AKfycbwVs2Si91yKz6m3utpaPtsttbh_lUQ8LOQM3Zud2hPFxXCgW3u1/exec"
    payload = {
        'sheetUrl':"https://docs.google.com/spreadsheets/d/1kL7p464r_KwUN2RWZrFhBlR7yhaLEgpsxaKAWAR9m6I/edit#gid=0",
        'sheetTag':"工作表1",
        'row': 1,
        'col': 1,
        'endRow' : 51,
        'endCol' : 20
    }
    resp = requests.get(url, params=payload)
    temp = resp.text.split(',')
    userlist = []
    i = 0
    while i < len(temp):
        if temp[i] != "":
            userlist.append(user(temp[i],temp[i+1],temp[i+2]))
            i+=3
        else:
            break
    return userlist

#取得目前使用者的index
def Login(user_id,userlist):
    for user in userlist:
        if user.ID == user_id:
            return userlist.index(user)
    return -1

#寫入資料
def Write(Row,data,Col):
    url = "https://script.google.com/macros/s/AKfycbyBbQ1lsq4GSoKE0yiU5d6x0z2EseeBNZVTewWlSZhQ6EVrizo/exec"
    payload = {
        'sheetUrl':"https://docs.google.com/spreadsheets/d/1kL7p464r_KwUN2RWZrFhBlR7yhaLEgpsxaKAWAR9m6I/edit#gid=0",
        'sheetTag':"工作表1",
        'data':data,
        'x':str(Row+1),
        'y':str(Col)
    }
    requests.get(url, params=payload)

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

#指令系統，若觸發指令會回傳True
def Command(event):
    tempText = event.message.text.split(",")
    if tempText[0] == "發送" and event.source.user_id == "U95418ebc4fffefdd89088d6f9dabd75b":
        line_bot_api.push_message(tempText[1], TextSendMessage(text=tempText[2]))
        return True
    else:
        return False

#回覆函式，指令 > 關鍵字 > 按鈕
def Reply(event,userlist,clientindex):
    if userlist[clientindex].Situation == '-1':
        if not Command(event):
            if not Keyword(event):
                line_bot_api.reply_message(event.reply_token,
                    TextSendMessage(text = "你知道台灣最稀有、最浪漫的鳥是哪一種鳥嗎？"))
                Write(clientindex,'0',3)
    elif userlist[clientindex].Situation == '0':
        if event.message.text.find("黑面琵鷺") != -1:
            line_bot_api.reply_message(event.reply_token,
                TextSendMessage(text = "你居然知道答案!!!"))
        else:
            line_bot_api.reply_message(event.reply_token,
                TextSendMessage(text = "答案是：黑面琵鷺!!!因為每年冬天，他們都會到台灣來\"壁咚\""))
        Write(clientindex,'-1',3)

# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    try:
        userlist = GetUserList()
        clientindex = Login(event.source.user_id,userlist)
        if clientindex > -1:
            #開始使用功能
            line_bot_api.push_message(event.source.user_id, TextSendMessage(text=userlist[clientindex].Name))
            Reply(event,userlist,clientindex)
        else:
            message = TemplateSendMessage(
                alt_text='確認姓名(手機限定)',
                template=ConfirmTemplate(
                    text='初次使用需要登記姓名\n您叫做'+event.message.text+'嗎?',
                    actions=[
                        PostbackTemplateAction(
                            label='對',
                            data='0`t`'+event.message.text
                        ),
                        PostbackTemplateAction(
                            label='不對',
                            data='0`f'
                        )
                    ]
                )
            )
            line_bot_api.reply_message(event.reply_token, message)
    except Exception as e:
        line_bot_api.reply_message(event.reply_token, 
            TextSendMessage(text=str(e)))

#處理Postback
@handler.add(PostbackEvent)
def handle_postback(event):
    userlist = GetUserList()
    clientindex = Login(event.source.user_id,userlist)
    data = event.postback.data.split('`')
    #註冊用
    if data[0] == '0' and clientindex < 0:
        if data[1] == 't':
            Signup(event.source.user_id,data[2])
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text="註冊成功，歡迎來到LineBot世界"))
        elif data[1] == 'f':
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text="請再次輸入您的姓名"))

#處理貼圖事件
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