import requests
import json
import configparser
import os
# query clip by guid

filename = 'not_exits_guid_file.json'

material = {}

print("load not_exits_guid_file.json.....")

if not os.access(filename, os.F_OK):
    material = {}
else:
    with open(filename) as file_obj:
        material = json.load(file_obj)

print("load setting.ini.....")

config = configparser.ConfigParser()
path = r"setting.ini"
config.read(path)
ip = config['api']['ip']
url = config['api']['url']
param = config['api']['param']
requestUrl = ip + url + param

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


def get_clip_info(guid):
    if guid == "":
        return None
    else:
        queryUrl = requestUrl.replace("{}", guid)
        r = requests.get(queryUrl, headers=headers)
        if r.status_code == 200:
            clip = json.loads(r.text)
            if (clip.get("code") == "0"):
                try:
                    print("guid:  " + clip.get("ext").get("entity").get("guid"))
                    return clip
                except BaseException:
                    return None
            else:
                print("hive not have this guid:" + guid)
        else:
            print("can't acess server")


print("start query.....")


def is_pic_keyframe_loss(clip, f_pic):
    if clip is None:
        return -1
    else:
        try:
            type = clip.get("ext").get("entity").get("type")
            subtype = clip.get("ext").get("entity").get("subtype")
            if type == 32 and subtype == 32:
                keyframe = clip.get("ext").get("entity").get("iconfilename")
                f_pic.write("guid: " + clip.get("ext").get("entity").get("guid") + "\n")
                f_pic.flush()
                if not os.access(keyframe, os.F_OK):
                    return 1
                else:
                    return -1
            else:
                return -1
        except BaseException:
            return -1


if __name__ == '__main__':
    # 注释部分为205环境测试代码
    # material.clear()
    # material["88d6ceff7224b806ec57fc8483631c03"] = [
    #     "\\\\172.16.0.202\\hivefiles\\sobeyhive\\buckets\\u-x583i30f58xanx8w\\tld\\333120\\333120_0.bmp"]
    # material["95581ef0a3bb4179a1990f75c9ff7d02"] = [
    #     "\\\\172.16.0.202\\hivefiles\\sobeyhive\\buckets\\u-q3p523b4mem82k63\\2020\\12\\04\\zgg6vf029fco15q9\\95ec3bf16aae42e19e022c6671afe807.mxf"]
    # material["fa6a78f46e3444a4b225079c183b4122"] = [
    #     "\\\\172.16.0.202\\hivefiles\\sobeyhive\\buckets\\u-q3p523b4mem82k63\\2020\\12\\04\\4dg652sr2yubuksj\\92bd615b1a1c4f079c55de68a67c3d8a.mp4"]
    # material["0e76ac5e694245db8b15454d9796d968"] = [
    #     "\\\\172.16.0.202\\hivefiles\\sobeyhive\\buckets\\u-q3p523b4mem82k63\\2020\\12\\04\\3uk3adi65lf40ge2\\887e11f8bea1424f961cea2012995523.mxf"]
    # material["522a566f26b6438d96bcea9265592e94"] = [
    #     "\\\\172.16.0.202\\hivefiles\\sobeyhive\\buckets\\u-q3p523b4mem82k63\\2020\\12\\04\\r20nqm8zj2w2xvff\\ea232a2d5e314d78b8676b5fffc7bce8.mp3"]

    # 日志都写在high_low文件夹内
    if not os.path.exists("high_low"):
        os.mkdir("high_low")
    
    f_pic = open("./high_low/pic_clip_guid.log", 'w', encoding="utf-8")
    
    with open("./high_low/pic_keyframe_loss_guid.log", 'w', encoding="utf-8") as f:
        for mat in material.keys():
            clip = get_clip_info(mat)
            b_pic_keyframe_loss = is_pic_keyframe_loss(clip, f_pic)
            if b_pic_keyframe_loss == 1:
                f.write("pic keyframe loss, guid: " + mat + "\n")
                f.flush()

    f_pic.close()