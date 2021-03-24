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
    try:
        apiid=event['queryStringParameters']['id']
        apisecert=event['queryStringParameters']['secert']
        apiagentId = event['queryStringParameters']['agentId']
        apimsg = event['queryStringParameters']['msg']
    except:
        apimsg = '有必填参数没有填写，请检查是否填写正确和格式是否错误。详情可以参阅：https://blog.zhheo.com/p/1e9f35bc.html'
        status = 1
    else:
        try:
            # 执行主程序
            getTocken(id=apiid,secert=apisecert,msg=apimsg,agentId=apiagentId)
        except:
            status = 1
            apimsg = '主程序运行时出现错误，请检查参数是否填写正确。详情可以参阅：https://blog.zhheo.com/p/1e9f35bc.html'
        else:
            status = 0
    # print(event)
    # print("Received event: " + json.dumps(event, indent = 2)) 
    # print("Received context: " + str(context))
    # print("Hello world")
    status_str = json.dumps({
            "status":status,
            "msg":apimsg
        })
    return(status_str)