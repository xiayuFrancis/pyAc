import requests
import json
import configparser
import os
import time

print("load setting.ini.....")

config = configparser.ConfigParser()
path = r"setting.ini"
config.read(path)
ip_create_low = config['api']['ip_create_low']
url = config['api']['createLowUrl']
param = config['api']['param']
requestUrl = ip_create_low + url + param

site = config['header']['sobeyhive-http-site']
system = config['header']['sobeyhive-http-system']
token = config['header']['sobeyhive-http-token']
tool = config['header']['sobeyhive-http-tool']
usercode = config['header']['sobeyhive-http-usercode']

headers = {
    "Accept": "application/json",
}

headers["sobeyhive-http-site"] = site
headers["sobeyhive-http-system"] = system
headers["sobeyhive-http-token"] = token
headers["sobeyhive-http-tool"] = tool
headers["sobeyhive-http-usercode"] = usercode


def create_low(guid):
    if guid == "":
        return None, None
    else:
        queryUrl = requestUrl.replace("{}", guid)
        print("create_low, guid : " + guid + "\n")
        r = requests.get(queryUrl, headers=headers)
        if r.status_code == 200:
            clip = json.loads(r.text)
            if (clip.get("code") == "0"):
                try:
                    print("create_low, suc" + "\n")
                    return 0, None
                except BaseException:
                    return None, None
            else:
                try:
                    msg = clip.get("msg")
                    print("create_low, failed " + "\n")
                    return 1, clip.get("msg")
                except BaseException:
                    return 1, "have no response"
        else:
            print("can't acess server")


if __name__ == '__main__':
    print("load high_low/low_lose_guid.log.....")
    if not os.path.exists("high_low"):
        print("there is no high_low folder")
    else:
        guid = []
        with open("./high_low/low_lose_guid.log", "r", encoding="utf-8") as f:
            for line in f:
                guid.append(line.strip())

        with open("./high_low/create_low_suc.log", "w", encoding="utf-8") as f_suc:
            with open("./high_low/create_low_failed.log", "w", encoding="utf-8") as f_failed:
                count = 0
                for id in guid:
                    count += 1
                    if(count > 10):
                        time.sleep(10)
                        count = 0
                    ret, msg = create_low(id)
                    if ret is None:
                        f_failed.write("failed cause guid is null" + "\n")
                        f_failed.flush()
                    elif ret == 1:
                        if msg is None:
                            f_failed.write(
                                "failed create low guid: " + id + " msg: None" + "\n")
                            f_failed.flush()
                        else:
                            f_failed.write(
                                "failed create low guid: " + id + " msg: " + msg + "\n")
                            f_failed.flush()
                    else:
                        f_suc.write("suc create low guid: " + id + "\n")
                        f_suc.flush()
