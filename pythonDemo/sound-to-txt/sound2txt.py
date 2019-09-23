'''
@Description: 语音转文本
@Version: 1.0
@Autor: lhgcs
@Date: 2019-06-15 12:46:16
@LastEditors: lhgcs
@LastEditTime: 2019-09-02 17:07:32
'''


'''
百度语音识别：
https://cloud.baidu.com/campaign/experience/index.html?unifrom=eventpage

注册流程说明：
https://ai.baidu.com/docs#/Begin/top
API说明：
http://ai.baidu.com/docs#/ASR-API/top

在应用列表里创建应用：
http://console.bce.baidu.com/ai/?fromai=1#/ai/speech/app/list
得到：
AppID：16526970
API Key：Mvebbb4kTZKoeKXqNcultZ5j
Secret Key：cVYDCnwTKqGslGlDvfsH0ampogAQ2AaX


demo:https://github.com/Baidu-AIP/speech-demo.git

语音格式
格式支持：pcm（不压缩）、wav（不压缩，pcm编码）、amr（压缩格式）。推荐pcm 采样率 ：16000 固定值。 编码：16bit 位深的单声道。
'''

'''
pip install jieba

'''

import wave
import requests
import json


'''
@description: 根据API Key及Secret Key，进行Access Token（用户身份验证和授权的凭证）的生成（有效期为30天）
@param {type} 
@return: 
'''
def get_token():
    AppID = "16526970"
    # 公钥
    API_Key = "Mvebbb4kTZKoeKXqNcultZ5j"
    # 密钥
    Secret_Key = "cVYDCnwTKqGslGlDvfsH0ampogAQ2AaX"
    # 用POST方式
    data = {}
    #data["grant_type"] = "client_credentials"
    data["client_id"] = API_Key
    data["client_secret"] = Secret_Key
    print(json.dumps(data))

    # 失败   {"error":"unsupported_grant_type","error_description":"The authorization grant type is not supported"}
    # url = "https://openapi.baidu.com/oauth/2.0/token"
    # response = requests.post(url=url, json=json.dumps(data))

    # 用GET方式
    url = "https://openapi.baidu.com/oauth/2.0/token?grant_type=client_credentials&client_id=" + API_Key + "&client_secret=" + Secret_Key
    response = requests.get(url=url)

    jsondata = response.text
    print(jsondata)

    token = None
    if response.status_code == 200:
        token = json.loads(jsondata)['access_token']
    return token

'''
@description: get_text 语音转文本
@param {type} 
@return: 

格式支持：pcm（不压缩）、wav（不压缩，pcm编码）、amr（压缩格式）；固定16k 采样率；
系统支持语言种类 普通话
文件大小不超过10M，时长不超过60s。 
'''
def get_text(token, wavefile):
    fp = wave.open(wavefile, 'rb')
    # 已经录好音的音频片段内容
    nframes = fp.getnframes()
    filelength = nframes*2
    audiodata = fp.readframes(nframes)

    cuid = '71XXXX663'  # 用户唯一标识，建议填写能区分用户的机器 MAC 地址或 IMEI 码，长度为60字符以内。
    dev_pid = 1537      # 不填写lan参数生效，都不填写，默认1537（普通话 输入法模型）
    lan = "zh"          # 如果dev_pid填写，该参数会被覆盖。语种选择,默认中文（中文=zh、粤语=ct、英文=en，不区分大小写）
    server_url = 'http://vop.baidu.com/server_api' + '?cuid={}&token={}'.format(cuid, token)
    headers = {
        # 语音格式（pcm 或者 wav 或者 amr）,采样率固定16000
        'Content-Type': 'audio/wav; rete=8000',
        'Content-Length': '{}'.format(filelength),
    }

    response = requests.post(url=server_url, headers=headers, data=audiodata)
    jsondata = response.text

    if response.status_code == 200:
        data = json.loads(jsondata)
        if "err_msg" in data and "result" in data and data["err_no"] == 0:
            return data["result"]
    return token

import jieba
if __name__ == '__main__':
    # access_token = get_token()
    # print(access_token)
    # result = get_text(token=access_token, wavefile='/home/ubuntu/Desktop/111.wav')
    # print(result)

    # 语义分割
    seg_list = jieba.cut("我来到北京清华大学", cut_all=False)# 精确模式
    # 精确模式，试图将句子最精确地切开，适合文本分析；
    # 全模式，把句子中所有的可以成词的词语都扫描出来, 速度非常快，但是不能解决歧义；
    # 搜索引擎模式，在精确模式的基础上，对长词再次切分，提高召回率，适合用于搜索引擎分词。
    print(type(seg_list))
    print(seg_list)
