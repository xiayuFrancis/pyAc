import requests
import json
import configparser
import os
from PIL import Image

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



def alphabg2white_PIL(img):
    img=img.convert('RGBA')
    sp=img.size
    width=sp[0]
    height=sp[1]
    for yh in range(height):
        for xw in range(width):
            dot=(xw,yh)
            color_d=img.getpixel(dot)
            if(color_d[3]==0):
                color_d=(255,255,255,255)
                img.putpixel(dot,color_d)
    return img


def create_icon(clip):
    if clip is None:
        return -1
    else:
        try:
            iconfilename = clip.get("ext").get("entity").get("iconfilename")
            clipfiles = clip.get("ext").get("entity").get("item").get("clipfile")

            if len(clipfiles) > 0 :
                for i in clipfiles:
                    if os.access(i.get('filename'), os.F_OK):
                        clipfile = i
                        break

                img = Image.open(clipfile.get('filename'))

                img = alphabg2white_PIL(img=img)

                width =  img.size[0]
                height = img.size[1]

                t_width = 320
                t_height =int(height * 320 / width)
                img.thumbnail((t_width, t_height))  # resize image with high-quality

                folder = iconfilename[:iconfilename.rfind('\\')]
                if not os.path.exists(folder):
                    os.makedirs(folder)

                type = iconfilename[ iconfilename.rfind('.')+1:len(iconfilename) + 1 ]

                if type == "bmp":
                    type = "bmp"
                elif type == "png":
                    type = "JPEG"
                else:
                    type = "JPEG"
                img = img.convert('RGB')
                img.save(iconfilename, type)

                return 1
            return  -1
        except BaseException as e:
            print("exceptional , guid: " +
                  clip.get("ext").get("entity").get("guid") + "e : " + str(e) + "\n")
            return -1



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
                ret = create_icon(clip)
                if ret == 1 :
                    ficon_create.write(
                        "create keyframe suc, guid: " + contentid  + " keyframeno: " + str(keyframeno) + "\n")
                    ficon_create.flush()

                else:
                    ficon_create.write(
                        "create keyframe failed, guid: " + contentid + " keyframeno: " + str(keyframeno) + "\n")
                    ficon_create.flush()

    ficon_create.close()
