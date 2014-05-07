# -*- coding:utf8 -*-
#! /usr/bin/env python
import sys
reload(sys) 
sys.setdefaultencoding('utf8')
import time
import json

from sdk import *

PLATFORM = "sina_weibo"

# 换成你的 APPKEY
APP_KEY = "1619491175"
APP_SECRET = "daeb1e1b3cc4fb2d3312f16a2d609c31"
CALLBACK_URL = "http://127.0.0.1:8080/sos/callback"
# 请先按照 https://github.com/upbit/tweibo-pysdk/wiki/OAuth2Handler 的鉴权说明填写 ACCESS_TOKEN 和 OPENID
AUTH_URL = "https://api.weibo.com/oauth2/"
ACCESS_TOKEN = ""
OPENID = ""
CODE = ""
    
if PLATFORM == "sina_weibo":
    # 换成你的 APPKEY
    APP_KEY = "1619491175"
    APP_SECRET = "daeb1e1b3cc4fb2d3312f16a2d609c31"
    CALLBACK_URL = "http://127.0.0.1:8080/sos/callback"
    AUTH_URL = "https://api.weibo.com/oauth2/"
    ACCESS_TOKEN = "2.00vS7kECkPCGRDef79f63ce6P247_D"
    OPENID = "1902435213"
    CODE = ""
else:
    pass

def code_test():
    """ 访问get_access_token_url()的URL并授权后，会跳转callback页面，其中包含如下参数：
        #access_token=00000000000ACCESSTOKEN0000000000&expires_in=8035200&openid=0000000000000OPENID0000000000000&openkey=0000000000000OPENKEY000000000000&refresh_token=0000000000REFRESHTOKEN00000000&state=
    保存下其中的 access_token, openid 并调用
        oauth.set_access_token(access_token)
        oauth.set_openid(openid)
    即可完成 OAuth2Handler() 的初始化。可以记录 access_token 等信息
    """
    oauth = OAuth2Handler(auth_url = AUTH_URL)
    oauth.set_app_key_secret(APP_KEY, APP_SECRET, CALLBACK_URL)
    print oauth.get_access_token_url()

def main():
    oauth = OAuth2Handler(auth_url = AUTH_URL)
    oauth.set_app_key_secret(APP_KEY, APP_SECRET, CALLBACK_URL)
    oauth.set_access_token(ACCESS_TOKEN)
    oauth.set_openid(OPENID)

    api = SinaWeiboAPI(oauth)
    #api = API(oauth, host="127.0.0.1", port=8888)       # Init API() with proxy
    json1 = api.get.call("trends/hourly.json")()
    #print ">> %s: %s" % (json1.as_of, json1.trends)
    i = 0
    print type(json1)
    time_key = json1.trends.keys()[0]
    print time_key
    options = []
    for option in json1.trends[time_key]:
        options.append({"content":option["name"]})
        i = i + 1
    
    #oauth = OAuth2Handler(auth_url = AUTH_URL)
    
    
    
    api = SosAPI(oauth)
    #title = u'新浪微博最新话题，你参与了几个'
    title= u'\u53f6\u4e00\u831c'
    desp = u'新浪微博最新话题，你参与了几个？'
    tag_name = u'自助餐'
    # local MTAwMDAxOTg0MTM5NTIxNTMwNzAwNw== outer  MTAwMDAxNjIxMTM4NTEyNjY1MTE3NQ== 6211385126651175
    json2 = api.get.call("vote/create")(
        token="MTAwMDAxOTg0MTM5NTIxNTMwNzAwNw==", 
        uid=9841395215307007, title = title, 
        class_id = 1000609, pic_url = "", 
        descp = desp, died_at = 1456281599999, tag_names = tag_name, 
        voteOptions = json.dumps(options), has_open_option = 0, 
        asyncSendStatus = "false", maxSelect = len(options))
    
    print json2
    
    # GET /t/show
    #tweet1 = api.get.t__show(format="json", id=301041004850688)
    #print ">> %s: %s" % (tweet1.data.nick, tweet1.data.text)

    # POST /t/add
    #content_str = "[from PySDK] %s says: %s" % (tweet1.data.nick, tweet1.data.origtext)
    #tweet2 = api.post.t__add(format="json", content=content_str, clientip="10.0.0.1")
    #print ">> time=%s, http://t.qq.com/p/t/%s" % (tweet2.data.time, tweet2.data.id)

    # GET /statuses/user_timeline
    #user_timeline = api.get.statuses__user_timeline(format="json", name="qqfarm", reqnum=3, pageflag=0, lastid=0, pagetime=0, type=3, contenttype=0)
    #for idx, tweet in enumerate(user_timeline.data.info):
    #    print "[%d] http://t.qq.com/p/t/%s, (type:%d) %s" % (idx+1, tweet.id, tweet.type, tweet.text)

    # UPLOAD /t/upload_pic
    #pic1 = api.upload.t__upload_pic(format="json", pic_type=2, pic=open(IMG_EXAMPLE, "rb"))
    #print ">> IMG: %s" % (pic1.data.imgurl)

    # POST /t/add_pic_url
    #content_str2 = "[from PySDK] add pic demo: %s, time %s" % (IMG_EXAMPLE, time.time())
    #pic_urls = "%s" % (pic1.data.imgurl)
    #tweet_pic1 = api.post.t__add_pic_url(format="json", content=content_str2, pic_url=pic_urls, clientip="10.0.0.1")
    #print ">> time=%s, http://t.qq.com/p/t/%s" % (tweet_pic1.data.time, tweet_pic1.data.id)

if __name__ == '__main__':
    #code_test()
    main()
