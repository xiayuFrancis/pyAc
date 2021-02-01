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

ficon_all_guid = open(
    "./high_low/guid.log",
    'r',
    encoding="utf-8")

f_high_lose_guid = open(
    "./high_low/high_lose_guid.log",
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
                print("hive not have this guid:" + guid)
                return None
        else:
            print("can't acess server")
            return None


def get_markpoints(clip):
    if clip is None:
        return -1
    else:
        try:
            markpoints = clip.get("ext").get("entity").get("item").get("markpoints")
            return markpoints
        except BaseException:
            print("this clip has no markpoints, guid: " +
                  clip.get("ext").get("entity").get("guid") + "\n")
            return None


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


def is_need_type(clip):
    try:
        type = clip.get("ext").get("entity").get("type")
        subtype = clip.get("ext").get("entity").get("subtype")
        if type == 32 and (subtype == 1 or subtype == 2 or subtype == 8):
            return True
        else:
            ficon_create.write(
                "type、subtype not in (type==32, subtype == (1,2,8)), guid: " + contentid + "\n")
            ficon_create.flush()
            return False
    except BaseException:
        return False

if __name__ == '__main__':

    guid = []
    high_lose_guid =[]
    for id in ficon_all_guid:
        guid.append(id.strip())

    for id in f_high_lose_guid:
        high_lose_guid.append(id.strip())

    ficon_all_guid.close()
    f_high_lose_guid.close()

    ficon_create = open(
        "./high_low/create_mark_icon.log",
        'w',
        encoding="utf-8")

    for contentid in guid:
        if contentid in high_lose_guid :
            print("this file high lose, guid: " + contentid + "\n")
            ficon_create.write(
                "this file high lose, guid: " + contentid + "\n")
            ficon_create.flush()
            continue
            
        clip = get_clip_info(contentid)
        if clip is None:
            ficon_create.write(
                "can not get this from hive, guid: " +
                contentid +
                "\n")
            ficon_create.flush()
        else:
            is_need = is_need_type(clip=clip)
            if not is_need:
                continue

            markpoints = get_markpoints(clip=clip)
            if (markpoints is None) or len(markpoints) == 0:
                ficon_create.write(
                    "this clip has no markpoints, guid: " +
                  contentid + "\n")
                ficon_create.flush()
                continue

            for mark in markpoints:
                markguid = mark.get("markguid")
                keyframe = mark.get("keyframe")
                iconfilename = mark.get("iconfilename")
                
                if iconfilename is None or not os.access(iconfilename, os.F_OK):
                    ret = create_icon(contentid, keyframe)
                    if ret == True :
                        ficon_create.write(
                            "create markkeyframe suc, clipguid: " + contentid  + " markguid:" + markguid  + " keyframeno: " + str(keyframe) + "\n")
                        ficon_create.flush()

                    else:
                        ficon_create.write(
                            "create markkeyframe failed, clipguid: " + contentid + " markguid:" + markguid +" keyframeno: " + str(keyframe) + "\n")
                        ficon_create.flush()

    ficon_create.close()
