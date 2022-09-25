import random
import re
class Boast:
    #state noGame Start A
    def __init__(self):
        self.clearGame()

    def clearGame(self):
        self.now=2
        self.count=0
        self.playPeople=0
        self.dice={}
        self.order={}
        self.state='no_game'
        self.already1=0
        self.preName=''
        self.preGuess=''

    def initName(self):
        if self.state=='no_game':
            self.state='add_user'
            return self.nowStatus()
        else:
            #self.errorCommand(self)
            return self.nowStatus()
    def addUser(self,add_User_ID,add_User_Name):
        if self.state=='add_user':
            if not(add_User_ID in self.dice):
                #dice amount
                list=[]
                for i in range(0,6):
                    list.append(random.randrange(1,7))
                list.sort()
                self.dice[add_User_ID]=list
                #order
                self.playPeople+=1
                temp={}
                temp[0]=str(add_User_ID)
                temp[1]=str(add_User_Name)            
                self.order[self.playPeople]=temp
                return self.order[self.playPeople][1] + ' 已經加入遊戲\n' + \
                            '--------------------------\n' + \
                            '參與遊戲: "吹牛熊 加入" \n' + \
                            '開始遊戲: "吹牛熊 完成" \n'

            else:
                return add_User_ID + "你早就已經加入遊戲，以為我不知道嗎?\n"
        else:
            #self.errorCommand()
            return self.nowStatus()
    def startName(self):
        if self.state=='add_user':
            self.state='in_game'
            return '由 '+ self.order[1][1] +' 先行開始 \n' + \
                    '--------------------------\n' + \
                    '遊戲開始，私訊我可以看點數\n' + \
                    '遊戲過程中操作:\n'+ \
                    '1.喊: "吹牛熊 x個y" \n' +\
                    '2.抓: "吹牛熊 抓"'
        else:
           #self.errorCommand()
           return self.nowStatus()
    def guessGame(self,user_id,user_name,user_guess):
        #the true status and true people
        if self.state=='in_game' :
            print(str(self.order[self.now-1][0]))
            if user_id==self.order[self.now-1][0]:
                
                new_split=str(user_guess[4:]).split('個')
                if (self.count!=0):
                    pre_split=str(self.preGuess[4:]).split('個')
                else:
                    pre_split=["0","0"]
                    self.count+=1
                
                if int(new_split[0])>0 and int(new_split[0])<= self.playPeople*6 and int(new_split[1])>=1 and int(new_split[1])<=6:
                    if int(new_split[0])>int(pre_split[0]) or (int(new_split[0])==int(pre_split[0]) and int(new_split[1])>int(pre_split[1])):
                        if self.now > self.playPeople: 
                            self.now=1
                        if int(new_split[1])==1: self.already1=1
                        #memory the pre guess to compare
                        self.preGuess=user_guess
                        self.preName=user_name
                        #reply next people
                        nowPeople= self.order[self.now][1]
                        self.now+=1
                        self.count+=1
                        return '下一個輪到 ' +nowPeople + ' \n' \
                                '--------------------------\n' + \
                                '遊戲過程中操作:\n'+ \
                                '1.喊: "吹牛熊 x個y" \n' +\
                                '2.抓: "吹牛熊 抓"'
                    else:
                        return '點數需符合遊戲規則\n  上一個人點數為: \n'+str(self.preGuess[4:]) + \
                                '-------------------------\n' + self.getRule()
                else:
                    return '低於最小數量0或超過最大數量'+self.playPeople*6
            else:
                return user_name+' 還沒輪到你'
        else:
            return '遊戲尚未進行至此進度'
            #self.errorCommand()
            print('error')
    def catchGame(self,user_id,user_name):
        if user_id==self.order[self.now-1][0] and self.state=='in_game':
            response= user_name + ' 抓了' \
                + self.preName + ' 喊的 : ' + self.preGuess[4:] +'\n' \
                + '-------------------------\n' + '所有人點數:\n'
            if self.already1==1: response+= '1 已經喊過了\n'
            sumDice=0 
            print(response)
            pre_split=str(self.preGuess[4:]).split('個')
            for i in range(1,(self.playPeople+1)):
                response+= self.order[i][1] + ' : ' +str(self.dice[self.order[i][0]]) + '\n'
                sumDice+=self.dice[self.order[i][0]].count(int(pre_split[1]))
                if self.already1==0: sumDice+=self.dice[self.order[i][0]].count(1) 
                #print(sumDice)
            response+='-------------------------\n'
            self.state='end_game'
            if sumDice < int(pre_split[0]):
                response+=user_name + '獲勝'
            else:
                response+=self.preName + '獲勝'
            
            return response
        else:
            return user_name+' 別亂抓，還沒輪到你'
    
    def nowStatus(self):
        response='目前遊戲狀況為:'
        if self.state=='no_game':
            response+='無遊戲狀態\n 輸入 "吹牛熊 開始" '
        elif self.state=='add_user':
            response+='加入階段\n'+ \
                    '--------------------------\n' +\
                    '參與遊戲: "吹牛熊 加入" \n' +\
                    '開始遊戲: "吹牛熊 完成" \n'
        elif self.state=='in_game':
            response+='遊戲已經開始，私訊我可以看點數\n' +\
                    '--------------------------\n' +\
                    '遊戲過程中操作:\n'+ \
                    '喊點: "吹牛熊 x個y" \n' +\
                    '抓人: "吹牛熊 抓"'
        elif self.state=='end_game':
            response+='這輪遊戲結束\n' +\
                    '--------------------------\n' +\
                    '重新開始: "吹牛熊 重新"' +\
                    '整個結束: "吹牛熊 結束"'
        return response
        # no_game add_user in_game end_game 
    
    def againGame(self):
        self.now=2
        self.count=0
        self.dice={}
        self.already1=0
        self.preName=''
        self.preGuess=''
        list=[]
        for i in range(1,(self.playPeople+1)):
            list=[]
            for j in range(0,6):
                list.append(random.randrange(1,7))
                list.sort() 
            self.dice[self.order[i][0]]=list
        self.state='in_game'
        return '已重新開始，由:' + self.order[1][1] + '開始\n' +\
                '--------------------------\n' + \
                '遊戲開始，私訊我可以看點數\n' +\
                '遊戲過程中操作:\n'+ \
                '1.喊: "吹牛熊 x個y" \n' +\
                '2.抓: "吹牛熊 抓"'
    def getGroupId(self):
        return self.group_id
    def getDice(self,user_id):
        if user_id in self.dice:
            return str(self.dice[user_id])
        else:
            return 'no'
 

    def boastGameTranser(self,command,userID,userName):
        response=''
        if command.find('吹牛熊 開始')==0:
            response=self.initName()
        elif command.find('吹牛熊 加入')==0:
            response=self.addUser(userID,userName)
        elif command.find('吹牛熊 完成')==0:
            response=self.startName()
        elif command.find('吹牛熊 結束')==0:
            self.clearGame()
            response='可再使用 "吹牛熊 開始" 來開始新的遊戲'
        elif command.find('吹牛熊 重新')==0:
            response=self.againGame()
        elif command.find('吹牛熊 狀態')==0:
            response=self.nowStatus()
        elif command.find('吹牛熊 抓')==0:
            response=self.catchGame(userID,userName)
        else:
            if command.find('個')>0:
                print('!!'+ command +'!!')
                temp=command
                temp=temp[4:]
                gue=temp.split('個')
                pattern = re.compile("^[0-9]*$")
                if pattern.match(gue[0]) and pattern.match(gue[1]):
                    response=self.guessGame(userID,userName,command)
                else:
                    response='你可能想猜點數，但是你的格式錯誤了\n' +\
                            '--------------------------\n' + \
                            '遊戲過程中操作:\n'+ \
                            '1.喊: "吹牛熊 x個y" \n' +\
                            '2.抓: "吹牛熊 抓"'
            else:
                    response='你可能想跟我溝通，打錯了一些\n 打，"吹牛熊 狀態"，來學習操作'
        print('game:'+response)
        return response