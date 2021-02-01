import requests
import json
import configparser
import os

print("load setting.ini.....")

config = configparser.ConfigParser()
path = r"setting.ini"
config.read(path)
ip = config['api']['ip']
url = config['api']['url']
param = config['api']['param']
requestUrl = ip + url + param

create_frame_url = "CMApi/api/entity/object/createframe"

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

if not os.path.exists("high_low"):
    os.mkdir("high_low")
ficon_lose_low = open(
    "./high_low/lose_icon_lose_low.log",
    'r',
    encoding="utf-8")

def get_clip_info(guid):
    if guid == "":
        return None
    else:
        queryUrl = requestUrl.replace("{}", guid)
        r = requests.get(queryUrl, headers=headers)
        if r.status_code == 200:
            clip = json.loads(r.text)
            if clip.get("code") == "0":
                try:
                    print("guid:  " + clip.get("ext").get("entity").get("guid"))
                    return clip
                except BaseException:
                    return None
            else:
                print("hive not have this guid:" + guid + '\n' + r.text)
                return None
        else:
            print("can't acess server")
            return None


def get_clip_keyframeno(clip):
    if clip is None:
        return -1
    else:
        try:
            keyframeno = clip.get("ext").get("entity").get("iconframe")
            return keyframeno
        except BaseException:
            print("this clip has no keyframeno, guid: " +
                  clip.get("ext").get("entity").get("guid") + "\n")
            return -1


def create_icon(id, keyframeno):
    url = ip + create_frame_url
    url = url + "?contentid=" + id + "&groupName=videogroup"

    body = []
    body_json = {}
    body_json["keyFrameNo"] = keyframeno
    body.append(body_json)

    r = requests.post(url, data=json.dumps(body), headers=headers)
    if r.status_code == 200:
        res = json.loads(r.text)
        if (res.get("code") == "0"):
            print("create keyframe suc, guid: " +id  + " keyframeno: " + str(keyframeno) + "\n" )
            return True
        else:
            print("create keyframe failed, guid: " +id  + " keyframeno: " + str(keyframeno) + "\n" )
            return False


if __name__ == '__main__':

    guid = []
    for id in ficon_lose_low:
        guid.append(id.strip())
    ficon_lose_low.close()

    ficon_create = open(
        "./high_low/create_clip_icon.log",
        'w',
        encoding="utf-8")

    for contentid in guid:
        clip = get_clip_info(contentid)
        if clip is None:
            ficon_create.write(
                "can not get this from hive, guid: " +
                contentid +
                "\n")
            ficon_create.flush()

        else:
            keyframeno = get_clip_keyframeno(clip=clip)
            if keyframeno == -1:
                ficon_create.write(
                    "this clip has no keyframeno, guid: " + contentid + "\n")
                ficon_create.flush()

            else:
                ret = create_icon(contentid, keyframeno)
                if ret == True :
                    ficon_create.write(
                        "create keyframe suc, guid: " + contentid  + " keyframeno: " + str(keyframeno) + "\n")
                    ficon_create.flush()

                else:
                    ficon_create.write(
                        "create keyframe failed, guid: " + contentid + " keyframeno: " + str(keyframeno) + "\n")
                    ficon_create.flush()

    ficon_create.close()
