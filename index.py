# -*- coding: utf8 -*-
import requests
import json

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

def main(event, context):
    apiid=event['queryStringParameters']['id']
    apisecert=event['queryStringParameters']['secert']
    apiagentId = event['queryStringParameters']['agentId']
    apimsg = event['queryStringParameters']['msg']
    getTocken(id=apiid,secert=apisecert,msg=apimsg,agentId=apiagentId)
    # print(event)
    # print("Received event: " + json.dumps(event, indent = 2)) 
    # print("Received context: " + str(context))
    # print("Hello world")
    status_str = json.dumps({
        "status":"0",
        "msg":apimsg
    })
    return(status_str)