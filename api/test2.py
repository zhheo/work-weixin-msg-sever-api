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

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        path = self.path
        parsed = urlparse.urlparse(path)
        querys = urlparse.parse_qs(parsed.query)
        querys = {k: v[0] for k, v in querys.items()}

        # 执行方法
        try:
            apiid=querys['id']
            apisecert=querys['secert']
            apiagentId = querys['agentId']
            apimsg = querys['msg']
        except:
            apimsg = '有必填参数没有填写'
            status = 1
        else:
            try:
                getTocken(id=apiid,secert=apisecert,msg=apimsg,agentId=apiagentId)
            except:
                status = 1
                apimsg = '主程序运行时出现错误'
            else:
                status = 0

        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({
            "status":status,
            "msg":apimsg
        }).encode('utf-8'))
        return