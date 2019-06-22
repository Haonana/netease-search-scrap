#coding = utf-8
from Crypto.Cipher import AES
import base64
import requests
import json
import binascii
import os
import sys
import recarg
import urllib.request


FAKE_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',  # noqa
    'Accept-Charset': 'UTF-8,*;q=0.5',
    'Accept-Encoding': 'gzip,deflate,sdch',
    'Accept-Language': 'en-US,en;q=0.8',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:60.0) Gecko/20100101 Firefox/60.0',  # noqa
    'referer': 'https://www.google.com'
}


def encode_netease_data(data) -> str:
    data = json.dumps(data)
    key = binascii.unhexlify('7246674226682325323F5E6544673A51')
    encryptor = AES.new(key, AES.MODE_ECB)
    # 补足data长度，使其是16的倍数
    pad = 16 - len(data) % 16
    fix = chr(pad) * pad
    byte_data = (data + fix).encode('utf-8')
    return binascii.hexlify(encryptor.encrypt(byte_data)).upper().decode()

def netease_search(keyword) -> list:
    count = 8
    eparams = {
        'method': 'POST',
        'url': 'http://music.163.com/api/cloudsearch/pc',
        'params': {
            's': keyword,
            'type': 1,
            'offset': 0,
            'limit': count
        }
    }
    data = {'eparams': encode_netease_data(eparams)}

    s = requests.Session()
    s.headers.update(FAKE_HEADERS)
    s.headers.update({
        'referer': 'http://music.163.com/',
    })

    r = s.post('http://music.163.com/api/linux/forward', data=data)

    if r.status_code != requests.codes.ok:
        raise RequestError(r.text)
    j = r.json()
    if j['code'] != 200:
        raise ResponseError(j)
    return j

def get(songname):

    songlist = netease_search(songname)['result']['songs']
    x = songlist[0]
    downNum = 0
    artists = ''
    for i in range(len(x['ar'])):
        if i != 0:
            artists += ('&'+ x['ar'][i]['name'])
        else:
            artists += x['ar'][i]['name']
    #print(artists)
    
    savepath = './downloads/'
    if not os.path.exists(savepath + x['name']+ '-' + artists + '.mp3'):
            print('***** ' +  x['name']+ '-' + artists + '.mp3 ***** Downloading...')
            url = 'http://music.163.com/song/media/outer/url?id=' + str(x['id']) + '.mp3'
            try:
                urllib.request.urlretrieve(url, savepath + x['name'].replace('/','') + '-' + artists +'.mp3')
                downNum += 1
                print("-----\""+ x['name'] + '" has been downloaded into %s'%(savepath))
            except:
                failf = open('failsongs', 'a+')
                failf.write(x['name'] + str(x['id']) + '\n')
                failf.close()
                print('Download wrong~')
                downNum = 0
    return downNum


def get_localmmenu(path):
    song_list = []
    with open(path, 'r') as f:
        for line in f:
            song_list.append(line.split('.')[1].strip())
    return(song_list)

def download_menu(txtpath):
    downNum = 0
    myplaylist = get_localmmenu(txtpath)
    for song in myplaylist:
        isok = get(song)
        downNum += isok
    print('Download complete ' + str(downNum) + ' files !')

def main():
    if not (recarg.get_option('keyword') or recarg.get_option('txt')):
        # 如果未设置关键词
        exit('Input error')
    else:
        if recarg.get_option('keyword') != '':
            sname = recarg.get_option('keyword')
            get(sname)
        elif recarg.get_option('txt') != '':
            tpath = recarg.get_option('txt')
            download_menu(tpath)
    
if __name__ == "__main__":
    recarg.init_option()
    if len(sys.argv) > 1:
        recarg.set_opts(sys.argv[1:])
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)