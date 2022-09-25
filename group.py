import random
import game
import errno,os,sys,json,tempfile
from argparse import ArgumentParser
from flask import Flask, request, abort
class Group:
    #state noGame Start A
    def __init__(self,g_id=''):
        self.group_id=g_id
        self.boastGame = None

    def checkModel(self,command,userID,userName):
        if command.find('吹牛熊')==0:
            if self.boastGame is None:
                self.boastGame=game.Boast()
                print('group:'+command)
            return self.boastGame.boastGameTranser(command,userID,userName)
        else:
            return None
            
    def getGroupId(self):
        return self.group_id

    def getDice(self,user_id):
        return self.boastGame.getDice(user_id)
'''
    inputJson=json.loads(str(event))
    info = line_bot_api.get_profile(inputJson["source"]["userId"])
    userID=inputJson["source"]["userId"]
    userName=str(info.display_name)
    response=''
    reply=0
    if str(inputJson["source"]["type"])=='group':
        groupID=inputJson["source"]["groupId"]
        if str(event.message.text).find('吹牛熊')==0:
            if str(event.message.text).find('**開始吹牛')==0:
                obj=getObjs(groupID)
                response=obj.initName()
            elif str(event.message.text).find('**加入')==0:
                obj=getObjs(groupID)
                response=obj.addUser(userID,userName)
            elif str(event.message.text).find('**完成')==0:
                obj=getObjs(groupID)
                response=obj.startName()
            elif str(event.message.text).find('**結束')==0:
                obj=getObjs(groupID)
                obj.clearGame()
                response='可再使用 "**開始吹牛" 來開始新的遊戲'
            elif str(event.message.text).find('**重新')==0:
                obj=getObjs(groupID)
                response=obj.againGame()
            elif str(event.message.text).find('**狀態')==0:
                obj=getObjs(groupID)
                response=obj.nowStatus()
            elif str(event.message.text).find('**抓')==0:
                obj=getObjs(groupID)
                response=obj.catchGame(userID,userName)
            else:
                if str(event.message.text).find('個')>0:
                    print('!!'+ str(event.message.text) +'!!')
                    temp=str(event.message.text)
                    temp=temp[2:]
                    gue=temp.split('個')
                    pattern = re.compile("^[0-9]*$")
                    if pattern.match(gue[0]) and pattern.match(gue[1]):
                        obj=getObjs(groupID)
                        response=obj.guessGame(userID,userName,str(event.message.text))
                    else:
                        response='你可能想猜點數，但是你的格式錯誤了\n正確格式: "**x個y" ，x為任意整數，y為1~6點數'
                else:
                    response='你可能想跟我溝通，打錯了一些，建議你可以打，"**狀態"，來學習操作'
            reply=1 
    elif str(inputJson["source"]["type"])=='user':
        temps=getUserDice(userID)
        for temp in temps:
            response+=',' + str(temp) 
        print(response)
        reply=1        
    if reply==1:
        message=TextSendMessage(text=str(response))
        line_bot_api.reply_message(
            event.reply_token,
            message)


    
    if str(event.message.text).find('機掰')==0:
        message=TextSendMessage(text=str('沙小'))
        line_bot_api.reply_message(
            event.reply_token,
            message)
            '''


