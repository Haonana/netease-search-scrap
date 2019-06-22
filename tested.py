#coding = utf-8
from Crypto.Cipher import AES
import base64
import requests
import json

def aesEncrypt(text, key):

        # 偏移量
    iv = '0102030405060708'
        # 文本

    pad = 16 - len(text) % 16
    text = text + pad * chr(pad)  #补齐文本长度


    encryptor = AES.new(key, AES.MODE_CBC, iv)

       # encryptor = AES.new(key, 2, iv)

    ciphertext = encryptor.encrypt(text)
##        print(bytearray(key,'utf-8'))
    ciphertext = base64.b64encode(ciphertext)
    return ciphertext

def get_params():
    '''获取网易云第一个参数'''
    # 第一个参数
    #second_key = 16 * 'F'
    second_key = "RhlJoTD4Uv77HHqS"
    first_param = '{"s":"lucky","limit":"8","csrf_token":"b1cf8210c36d55a6fc47b66eebfb59da"}'
    first_param = '{"hlpretag":"<span class=\"s-fc7\">","hlposttag":"</span>","s":"lucky","type":"1","offset":"0","total":"true","limit":"8","csrf_token":"b1cf8210c36d55a6fc47b66eebfb59da"}'
    forth_param = "0CoJUm6Qyw8W8jud"
    first_key = forth_param
    params = aesEncrypt(first_param, first_key).decode('utf-8')
    #h_encText = aesEncrypt(first_param, first_key)
    #print('hhhh:',h_encText)
    params = aesEncrypt(params, second_key).decode('utf-8')

    return params

def rsaEncrypt(pubKey, text, modulus):
    '''进行rsa加密'''
    text = text[::-1]
    rs = int(codecs.encode(text.encode('utf-8'), 'hex_codec'), 16) ** int(pubKey, 16) % int(modulus, 16)
    return format(rs, 'x').zfill(256)

def get_encSecKey():
    '''获取第二个参数'''
    #second_key = 16 * 'F'
    second_key = "RhlJoTD4Uv77HHqS"
    second_param = "010001"
    third_param = "00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7"
    pubKey = second_param
    moudulus = third_param
    encSecKey = rsaEncrypt(pubKey, second_key, moudulus)
    return encSecKey

FAKE_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',  # noqa
    'Accept-Charset': 'UTF-8,*;q=0.5',
    'Accept-Encoding': 'gzip,deflate,sdch',
    'Accept-Language': 'en-US,en;q=0.8',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:60.0) Gecko/20100101 Firefox/60.0',  # noqa
    'referer': 'http://music.163.com/'
}
def get_json(url, params, encSecKey):
    data = {
         "params": params,
         "encSecKey": encSecKey
    }
    response = requests.post(url, headers=FAKE_HEADERS, data=data)
    return response.content


if __name__ == "__main__":
    
    url = 'https://music.163.com/weapi/cloudsearch/get/web?csrf_token='
    params = get_params()
    #params = 'vSl17J6gNmFi87QHGY5BHh2BPmOISsYJIUHc+tzlyhPgnnz5BH1fWwXYkk5M3DWwx9NRbZfqTY/IZo3MKRFU0cZVeU5KzkwNhh16xsFiDxCxjnC7iGGti9ShRm3FWp1p8JErxzApyT/ibesUiejmwARUbfHafhlNJKyL42vVNMUynHHOtP1v2tes7vFrWs2pmBNSyXwq1MrO/phmZmbgKyupQywbG6a1mqJOyd8yJj5Wfd6AsWmWYHAjIpg+gSaK6pfcmA81Lsf45JUG2/DnNg=='
    print(params)

    encSecKey = get_encSecKey()
    #encSecKey = '8ea97772e5dbac1be4ca6e796c15974dbbcaf3c71ad43f3b4cd040188d0afa2ca03e5882523755ae91ccd2dc89b11732dd7b1d213cbfcbb8f85775ab04f24268a834eb8ee14886782cca07e9d41cf1ab7f20ef85a4e30d5d7f865c5a1051b593f40c7dd21c4ab55c6af5928580f2add9194566cb88e0d7a36ed9f789a981a8a3'
    print(encSecKey)
    
    json_text = get_json(url, params, encSecKey)
    print(json_text)
    json_dict = json.loads(json_text)
    print(json_dict)
