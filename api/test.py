# -*- coding: utf8 -*-
import requests
import json
from http.server import HTTPServer,BaseHTTPRequestHandler
import json
import urllib.parse as urlparse

def getTocken(id,secert,msg,agentId):
    url = "https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=" + id + "&corpsecret=" + secert

    r =requests.get(url)
    tocken_json = json.loads(r.text)
    # print(tocken_json['access_token'])
    sendText(tocken=tocken_json['access_token'],agentId=agentId,msg=msg)
    return ['0','发送成功']

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
        apiid=querys['id']
        apisecert=querys['secert']
        apiagentId = querys['agentId']
        apimsg = querys['msg']

        if apiagentId and apiid and apimsg and apisecert:
            funcback = getTocken(id=apiid,secert=apisecert,msg=apimsg,agentId=apiagentId)
            funcinfo = funcback[1]
            funcstatus = funcback[0]
            funcmsg = apimsg
        else:
            funcinfo = '缺少参数，发送失败，请检查是否有参数缺少'
            funcstatus = '1'
            if apimsg:
                funcmsg = apimsg
            else:
                funcmsg = '没有填写msg参数'

        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        backmsg = json.dumps({
            "status":funcstatus,
            "msg":funcmsg,
            "info": funcinfo
        })

        self.wfile.write(backmsg).encode('utf-8')
        return


# host = ('localhost', 7777)
# # host = ('0.0.0.0', 7777)

# if __name__ == '__main__':
#     server = HTTPServer(host, handler)
#     print("Starting Server....")
#     server.serve_forever()