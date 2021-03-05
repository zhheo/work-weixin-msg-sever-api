# -*- coding: UTF-8 -*-
import requests
import json
from wsgiref.simple_server import make_server
from flask import Flask,request
import re
import urlparse
from http.server import BaseHTTPRequestHandler


def getTocken(id,secert,msg,agentId):
    url = "https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=" + id + "&corpsecret=" + secert

    r =requests.get(url)
    tocken_json = json.loads(r.text)
    # print(tocken_json['access_token'])
    sendText(tocken=tocken_json['access_token'],agentId=agentId,msg=msg)

def sendText(tocken,agentId,msg):
    result_str = 'none'
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
    try:
        requests.post(sendUrl,data)
    except:
        result_str = "发生了错误"
    else:
        result_str = "发送成功"

    return result_str

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        enc = "UTF-8"              #设置返回的编码格式
        path = str(self.path)     #获取请求的url
        # length = int(self.headers.getheader('content-length'))  #获取除头部后的请求参数的长度
        datas = urlparse.parse_qs(self.rfile.read(length), keep_blank_values=1)  #获取请求参数数据，请求数据为json字符串
        if path=="/scandatas":   
            # 读取参数
            apiid = datas["id"][0]
            apisecert= datas["secert"][0]
            apiagentId = datas["agentId"][0]
            apimsg = datas["msg"][0]
            # 运行函数
            getTocken(id=apiid,secert=apisecert,msg=apimsg,agentId=apiagentId)
            #以下是返回报文
            self.send_response(200)        #返回状态码
            self.send_header("Content-type", "text/html;charset=%s" % enc) #返回响应头内容
            self.end_headers()              #返回响应头结束
            buf = {"status": 0,                 #返回包体数据
                "data": {
                    "msg": apimsg}}
            self.wfile.write(json.dumps(buf))  #发送json格式的返回包体







# app=Flask(__name__)
 
# # 只接受POST方法访问
# @app.route("/sendmsg",methods=["POST"])
# def check():
#     # 默认返回内容
#     return_dict= {'return_code': '200', 'return_info': '处理成功', 'result': False}
#     # 判断传入的json数据是否为空
#     if request.get_data() is None:
#         return_dict['return_code'] = '5004'
#         return_dict['return_info'] = '请求参数为空'
#         return json.dumps(return_dict, ensure_ascii=False)
#     # 获取传入的参数
#     get_Data=request.get_data()
#     # 传入的参数为bytes类型，需要转化成json
#     get_Data=json.loads(get_Data)
#     apiid=get_Data.get('id')
#     apisecert=get_Data.get('secert')
#     apiagentId = get_Data.get('agentId')
#     apimsg = get_Data.get('msg')
#     # 对参数进行操作
    
#     getTocken(id=apiid,secert=apisecert,msg=apimsg,agentId=apiagentId)

#     return_dict['result']=tt(apimsg)
 
#     return json.dumps(return_dict, ensure_ascii=False)


# def tt(msg):
#     result_str="%s" %(msg)
#     return result_str


# if __name__ == "__main__":
#     app.run(debug=True)