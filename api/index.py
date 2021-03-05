import requests
import json
from wsgiref.simple_server import make_server
from flask import Flask,request


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

    result_str="%s今年%s岁" %(agentId,msg)
    return result_str
 
app=Flask(__name__)
 
# 只接受POST方法访问
@app.route("/sendmsg",methods=["POST"])
def check():
    # 默认返回内容
    return_dict= {'return_code': '200', 'return_info': '处理成功', 'result': False}
    # 判断传入的json数据是否为空
    if request.get_data() is None:
        return_dict['return_code'] = '5004'
        return_dict['return_info'] = '请求参数为空'
        return json.dumps(return_dict, ensure_ascii=False)
    # 获取传入的参数
    get_Data=request.get_data()
    # 传入的参数为bytes类型，需要转化成json
    get_Data=json.loads(get_Data)
    apiid=get_Data.get('id')
    apisecert=get_Data.get('secert')
    apiagentId = get_Data.get('agentId')
    apimsg = get_Data.get('msg')
    # 对参数进行操作
    
    getTocken(id=apiid,secert=apisecert,msg=apimsg,agentId=apiagentId)

    return_dict['result']=tt(apimsg)
 
    return json.dumps(return_dict, ensure_ascii=False)


def tt(msg):
    result_str="%s" %(msg)
    return result_str


if __name__ == "__main__":
    app.run(debug=True)