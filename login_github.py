# -*- coding: utf-8 -*-
# @Author: Gxn
# @Date:   2018-04-22 15:24:09
# @Last Modified by:   Gxn
# @Last Modified time: 2019-08-04 23:34:42
import requests
import json
import time
def auth_search(url):
    header = {
        'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3710.0 Safari/537.36",
        'method':'GET',
        'Accept':'application/json',
        'Authorization':'token ',
    }
    status = True
    while status:
        try:
            response = requests.get(url,headers=header)
            # print(response.status_code)
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            time.sleep(1)
            status = True
    return None
    # print(response.url)
    # print(response.text)
    # print(response.encoding)

def get_userinfo(username):
    url="https://api.github.com/users/" + username
    userinfo_dict = auth_search(url)
    userinfo = []
    if userinfo_dict != None:
        # print(userinfo_dict)
        userinfo.append(userinfo_dict['email'])
        userinfo.append(userinfo_dict['blog'])
        userinfo.append(userinfo_dict['name'])
        userinfo.append(userinfo_dict['location'])
    return userinfo

if __name__ == "__main__":
    url="https://api.github.com/users/ruanyf"
    print(auth_search(url))
    # print(get_userinfo("ruanyf"))

# https://www.cnblogs.com/zhangxinqi/p/9201594.html
