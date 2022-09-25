from __future__ import unicode_literals
import errno,os,sys,json,tempfile,translate
from argparse import ArgumentParser
from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)   
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
from io import BytesIO
from PIL import Image
import group,re
import test

app = Flask(__name__)



# Channel Access Token
line_bot_api = LineBotApi('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')
# Channel Secret
handler = WebhookHandler('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')

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
'''
user windows
{
    "message": {
        "id": "8003606106554",
        "text": "0.0",
        "type": "text"
    },
    "replyToken": "8142655d1c844ed9a5fd13fd081797d3",
    "source": {
        "type": "user",
        "userId": "U3a5b8cd69d793699d16e3900b76172ea"
    },
    "timestamp": 1527061185830,
    "type": "message"
}
'''
'''
group windows
{
    "message": {
        "id": "8003608840273",
        "text": "搞定",
        "type": "text"
    },
    "replyToken": "4aeadec0990641ffbc031c6538e1fa2f",
    "source": {
        "groupId": "Cd2d9bbb32f869f0667b3389476754d6a",
        "type": "group",
        "userId": "U3a5b8cd69d793699d16e3900b76172ea"
    },
    "timestamp": 1527061226015,
    "type": "message"
}   
'''
def getObjs(groupID):
    
    for obj in objs:
        if obj.getGroupId() == groupID:
            return obj
    obj = group.Group(groupID)
    objs.append(obj)
    return obj

  
def getUserDice(userID):
    for obj in objs:
        response=obj.getDice(userID)
        if response!='no':
            return response
    return '你並沒有加入任何遊戲'

@handler.add(MessageEvent, message=ImageMessage)
def handle_text_message(event):
    print(str(event))

    message_content = line_bot_api.get_message_content(str(event.message.id))
    i = Image.open(BytesIO(message_content.content))
    filename = '/tmp/' + str(event.message.id) + '.png'
    i.save(filename)
    print('save:' + filename)

    '''
    i = Image.open(BytesIO(message_content.content))
    filename = './tmp/' + '8439159969303' + '.png'
    i.save('8439159969303')
    return filename
    '''
    
    response=trans.imageTranslate(str(event.message.id))

    os.remove('/tmp/' + str(event.message.id) + '.png')
    os.remove('/tmp/' + str(event.message.id) + '.txt')
    
    message=TextSendMessage(text=str(response))
    line_bot_api.reply_message(
        event.reply_token,
        message)
    
@handler.add(MessageEvent, message=VideoMessage)   
def handle_video_message(event):
    response = '你六根不清淨，抄弟子規\n\
-------------\n\
弟子規　聖人訓\n\
首孝弟　次謹信\n\
汎愛眾　而親仁\n\
有餘力　則學文\n\
父母呼　應勿緩\n\
父母命　行勿懶\n\
父母教　須敬聽\n\
父母責　須順承\n\
冬則溫　夏則凊\n\
晨則省　昏則定\n\
出必告　反必面\n\
居有常　業無變\n\
事雖小　勿擅為\n\
苟擅為　子道虧\n\
物雖小　勿私藏\n\
苟私藏　親心傷\n\
親所好　力為具\n\
親所惡　謹為去\n\
身有傷　貽親憂\n\
德有傷　貽親羞\n\
親愛我　孝何難\n\
親憎我　孝方賢\n\
親有過　諫使更\n\
怡吾色　柔吾聲\n\
諫不入　悅復諫\n\
號泣隨　撻無怨\n\
親有疾　藥先嘗\n\
晝夜侍　不離床\n\
喪三年　常悲咽\n\
居處變　酒肉絕\n\
喪盡禮　祭盡誠\n\
事死者　如事生\n\
'
    message=TextSendMessage(text=str(response))
    line_bot_api.reply_message(
        event.reply_token,
        message)


@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event): 
    inputJson=json.loads(str(event))
    info = line_bot_api.get_profile(inputJson["source"]["userId"])
    userID=inputJson["source"]["userId"]
    userName=str(info.display_name)
    response=''
    reply=0
    print(str(event))
    print('--------------------------')
    print(str(info.picture_url))
    if str(event.message.text).find('UI吹牛')>-1:
        message = TemplateSendMessage(
            alt_text='Buttons template',
            template=ButtonsTemplate(
                thumbnail_image_url='https://i.imgur.com/prDn7Fv.jpg',
                title='吹牛開始',
                text='先按開始,在開始一個一個加入',
                actions=[
                    MessageTemplateAction(
                        label='開始吹牛',
                        text='吹牛熊 開始'
                    ),
                    MessageTemplateAction(
                        label='加入',
                        text='吹牛熊 加入'
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, message)
    elif str(event.message.text).find('問我一個問題')>-1:
        picUrl=str(info.picture_url)
        picUrl=picUrl.replace('http://','https://')
        print(picUrl)
        message = TemplateSendMessage(
            alt_text='Buttons template',
            template=ButtonsTemplate(
                #thumbnail_image_url=str(info.picture_url)+'.jpg',
                thumbnail_image_url=picUrl,
                title='這個人帥嗎',
                text='adsf',
                actions=[
                    MessageTemplateAction(
                        label='帥',
                        text='帥'
                    ),
                    MessageTemplateAction(
                        label='不帥',
                        text='不帥'
                    ) 

                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, message)
    elif str(event.message.text).find('語')>-1 or str(event.message.text).find('文言')==0 or str(event.message.text).find('越南')==0:
        response=trans.textTranslate(str(event.message.text))
        if response!='not response':
            reply=1
        if reply==1:
            message=TextSendMessage(text=str(response))
            line_bot_api.reply_message(
                event.reply_token,
                message)
    elif str(event.message.text).find('myid')>-1:
        message=TextSendMessage(text=str(inputJson["source"]["userId"]))
        line_bot_api.reply_message(
            event.reply_token,
            message)
    else:
        if str(inputJson["source"]["type"])=='group':
            groupID=inputJson["source"]["groupId"]
            obj=getObjs(groupID)
            print(obj.getGroupId())
            response=obj.checkModel(str(event.message.text),userID,userName)
            if not(response is None):
                reply=1
        elif str(inputJson["source"]["type"])=='user':
            print('----------check dice----------')
            response=getUserDice(userID)
            print(response)
            reply=1

        if reply==1:
            message=TextSendMessage(text=str(response))
            line_bot_api.reply_message(
                event.reply_token,
                message)


    

    '''
    # get id
    if str(event.message.text).find('myid')==0:
        message=TextSendMessage(text=str(inputJson["source"]["userId"]))
        line_bot_api.reply_message(
            event.reply_token,
            message)
    
    if str(event.message.text).find('info')==0:
        info = line_bot_api.get_profile(inputJson["source"]["userId"])
        ouput=info.display_name+'\n'+info.user_id
        message=TextSendMessage(text=ouput)
        line_bot_api.reply_message(
            event.reply_token,
            message)

    if str(event.message.text).find('groupinfo')==0:
        info = line_bot_api.get_group_member_profile(inputJson["source"]["groupId"],inputJson["source"]["userId"])
        ouput=info.display_name+'\n'+info.user_id
        message=TextSendMessage(text=ouput)
        line_bot_api.reply_message(
            event.reply_token,
            message)
    '''





objs=[]
trans=translate.Translate()
if __name__ == "__main__":
    
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)





