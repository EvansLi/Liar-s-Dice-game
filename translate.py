#!/usr/bin/python3
#coding=utf-8
from __future__ import print_function
import http.client
import hashlib,httplib2
import urllib.request, urllib.parse, urllib.error
import random
import json,os,io
from googleapiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from apiclient.http import MediaFileUpload, MediaIoBaseDownload


try:
  import argparse
  flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
  flags = None

class Translate:
    def get_credentials(self):
        SCOPES = 'https://www.googleapis.com/auth/drive'
        CLIENT_SECRET_FILE = 'client_id.json'
        APPLICATION_NAME = 'LineTranslateBot'

        credential_path = os.path.join("./", 'google-ocr-credential.json')
        store = Storage(credential_path)
        credentials = store.get()
        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
            flow.user_agent = APPLICATION_NAME
            if flags:
                credentials = tools.run_flow(flow, store, flags)
            else: # Needed only for compatibility with Python 2.6
                credentials = tools.run(flow, store)
            #print(credential_path)
        return credentials
        
    def imageTranslate(self,fileName):
        # get auth and google api object
        credentials = self.get_credentials()
        http = credentials.authorize(httplib2.Http())
        service = discovery.build('drive', 'v3', http=http)
        route = '/tmp/'
        txtfile = fileName + '.txt'
        imagenName = fileName + '.png'
        # upload file
        mime = 'application/vnd.google-apps.document'
        res = service.files().create(
            body={
            'name': imagenName,
            'mimeType': mime
            },
            media_body=MediaFileUpload(route + imagenName, mimetype=mime, resumable=True)
        ).execute()

        # download file
        downloader = MediaIoBaseDownload(
            io.FileIO(route + txtfile, 'wb'),
            service.files().export_media(fileId=res['id'], mimeType="text/plain")
        )
        done = False
        while done is False:
            status, done = downloader.next_chunk()

        # del file
        service.files().delete(fileId=res['id']).execute()

        f = open(route + txtfile , 'r' , encoding = 'utf8')
        fileResult=str(f.read())
        fileResult=fileResult.replace('_','')
        #print(fileResult)
        #print('#############################')
        return self.transResquest('auto','cht',fileResult)

    def transResquest(self,fromLang,toLang,langContent):
        appid = '20180814000194069' #appid
        secretKey = 'AhASWL5vWOIYVQptTGBa' #screct
        httpClient = None
        myurl = '/api/trans/vip/translate'
        salt = random.randint(32768, 65536)
        sign = appid+langContent+str(salt)+secretKey

        mdEncode = hashlib.md5()
        mdEncode.update(sign.encode('utf-8'))
        sign = mdEncode.hexdigest()
        myurl = myurl+'?appid='+appid+'&q='+urllib.parse.quote(langContent)+'&from='+fromLang+'&to='+toLang+'&salt='+str(salt)+'&sign='+sign
        try:
            httpClient = http.client.HTTPConnection('api.fanyi.baidu.com')
            httpClient.request('GET', myurl)
            response = httpClient.getresponse().read()
            restemp=response.decode('utf-8').replace("'", '"')
            res=json.loads(restemp)
            dst = res['trans_result'][0]['dst']
            dst = ''
            for temp in res['trans_result']:
                dst = dst + temp['dst']
        except:
            dst = 'error'
        finally:
            if httpClient:
                httpClient.close()
        print(dst)
        return dst
    '''
    def trans(self,lang_Type,lang_Content):
        
        appid = '20180814000194069' #appid
        secretKey = 'AhASWL5vWOIYVQptTGBa' #screct
        httpClient = None
        myurl = '/api/trans/vip/translate'
        q = lang_Content
        fromLang = 'cht'
        toLang = lang_Type
        salt = random.randint(32768, 65536)

        sign = appid+q+str(salt)+secretKey
        m1 = hashlib.md5()
        m1.update(sign.encode('utf-8'))
        sign = m1.hexdigest()
        myurl = myurl+'?appid='+appid+'&q='+urllib.parse.quote(q)+'&from='+fromLang+'&to='+toLang+'&salt='+str(salt)+'&sign='+sign
        try:
            httpClient = http.client.HTTPConnection('api.fanyi.baidu.com')
            httpClient.request('GET', myurl)
            response = httpClient.getresponse().read()
            restemp=response.decode('utf-8').replace("'", '"')
            res=json.loads(restemp)
            dst = res['trans_result'][0]['dst']
        except:
            dst = 'error'
        finally:
            if httpClient:
                httpClient.close()
        return dst
    '''
    def textTranslate(self,lineInput):
        langSupport={}
        langSupport['日語'] = 'jp'
        langSupport['文言'] = 'wyw'
        langSupport['韓語'] = 'kor'
        langSupport['德語'] = 'de'
        langSupport['英語'] = 'en'
        langSupport['泰語'] = 'th'
        langSupport['法語'] = 'fra'
        langSupport['繁體'] = 'cht'
        langSupport['越南'] = 'vie'

        toLang=lineInput[0:2]
        langContent=lineInput[2:]
        if toLang in langSupport:
            toLang=langSupport[toLang]
            return self.transResquest('cht',toLang,langContent)
        else:
            return 'not response'
 








'''

import translate
a = translate.Translate()
print(a.imageTranslate('translate.png'))
'''

        










