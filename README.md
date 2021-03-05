# work-weixin-msg-sever-api

使用腾讯云函数和企业微信给自己微信发送消息

## 发送方式

post

## 参数

```
{
    "id": "ww42a2d7e*********",
    "secert": "xD_XhQxL_6hVymgTBZuTaZviu9i3P**************",
    "msg": "这里是需要发送的文本",
    "agentId": 1000001
}
```

| 参数      | 类型  | 必选   | 描述               |
|---------|-----|------|------------------|
| id      | str | true | 企业微信公司id         |
| secert  | str | true | 企业微信应用的应用secert  |
| agentId | int | true | 企业微信应用的应用agentId |
| msg     | str | true | 需要发送的内容          |