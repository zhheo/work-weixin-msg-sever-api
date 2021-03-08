# -*- coding: utf8 -*-
import requests
import json
from http.server import BaseHTTPRequestHandler
import json
import urllib.parse as urlparse

def getTocken(id,secert,msg,agentId):
    url = "https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=" + id + "&corpsecret=" + secert

    r =requests.get(url)
    tocken_json = json.loads(r.text)
    # print(tocken_json['access_token'])
    sendText(tocken=tocken_json['access_token'],agentId=agentId,msg=msg)

def sendText(tocken,agentId,msg):
    sendUrl = "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=" + tocken
    # print(sendUrl)
    data = json.dumps({
        "safe": 0,
        "touser" : "@all",
        "msgtype" : "text",
        "agentid" : agentId,
        "text" : {
            "content" : msg
        }
    })
    requests.post(sendUrl,data)
    return '发送成功'

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        path = self.path
        parsed = urlparse.urlparse(path)
        querys = urlparse.parse_qs(parsed.query)
        querys = {k: v[0] for k, v in querys.items()}

        # 执行方法
        apiid=querys['id']
        apisecert=querys['secert']
        apiagentId = querys['agentId']
        apimsg = querys['msg']

        if apiagentId && apiid && apimsg && apisecert:
            funcinfo = getTocken(id=apiid,secert=apisecert,msg=apimsg,agentId=apiagentId)
            backmsg = json.dumps({
            "status":"0",
            "msg":apimsg,
            "info": funcinfo
        }
        else:
            backmsg = json.dumps({
            "status":"1",
            "msg":apimsg,
            "info":"缺少参数，发送失败，请检查是否有参数缺少"
        }

        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(backmsg).encode('utf-8'))
        return