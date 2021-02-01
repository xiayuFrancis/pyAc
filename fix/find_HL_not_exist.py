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


def print_filelist_by_json_dump(guid, f):
    if len(material) == 0:
        return
    else:
        if guid in material.keys():
            filelists = material.get(guid)
            for line in filelists:
                f.write(line + "\n")
            f.write("\r\n")
            f.flush()


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

if not os.path.exists("high_low"):
    os.mkdir("high_low")
ficon_lose_low = open("./high_low/lose_icon_lose_low.log", 'w', encoding="utf-8")
ficon = open("./high_low/lose_icon.log", 'w', encoding="utf-8")

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


def get_high_low_clip_file(clip):
    try:
        clipfiles = clip.get("ext").get("entity").get("item").get("clipfile")
        high_clip_file = []
        low_clip_file = []
        for clipfile in clipfiles:
            qualitytype = clipfile.get('qualitytype')
            if qualitytype == 0:
                if clipfile.get('filename')[-4:].lower() != '.otc':
                    high_clip_file.append(clipfile.get('filename'))
            elif qualitytype == 1:
                low_clip_file.append(clipfile.get('filename'))

        return high_clip_file, low_clip_file
    except BaseException:
        return None, None


def is_high_or_low_loss(clip):
    if clip is None:
        return -1
    else:
        try:
            type = clip.get("ext").get("entity").get("type")
            subtype = clip.get("ext").get("entity").get("subtype")
            try:
                icon = clip.get('ext').get('entity').get('iconfilename')
                print('icon:' + icon)
            except Exception:
                icon = ''
# if(type == 32 and (subtype == 1 or subtype == 2 or subtype == 4 or
# subtype == 8 or subtype == 1024 or subtype == 64 or subtype == 2048 or
# subtype == 4096 or subtype == 1048576 or subtype == 2097152)):
            if(type == 32 and (subtype == 1 or subtype == 2 or subtype == 4 or subtype == 8 or subtype == 32)):
                high_clip_file, low_clip_file = get_high_low_clip_file(clip)
                if ((high_clip_file is None) or (low_clip_file is None)):
                    return -1
                else:
                    guid = clip.get("ext").get("entity").get("guid")
                    cannot_acess_files = material.get(guid)
                    for file in cannot_acess_files:  # 有高质量丢失的情况
                        if file in high_clip_file:
                            if subtype == 32:
                                return 2
                            return 1

                    if icon in cannot_acess_files: # 统计丢失icon的素材
                        ficon_lose_low.write(mat + "\n")
                        ficon_lose_low.flush()

                    for file in cannot_acess_files:  # 没有高质量丢失 有低质量丢失
                        if file in low_clip_file:
                            return 0

                    if icon in cannot_acess_files: # 统计丢失icon的素材
                        ficon.write(mat + "\n")
                        ficon.flush()

                    return -1  # 高低都没有丢失
            else:
                return -1
        except BaseException:
            return -1


print("start query.....")

if __name__ == '__main__':
    # 注释部分为205环境测试代码
    # material.clear()
    # material["8f7d7866cd494d078d25bcd4a65efcf2"] = [
    #     "\\\\172.16.0.202\\hivefiles\\sobeyhive\\buckets\\u-x583i30f58xanx8w\\tld\\333120\\333120_0.bmp"]
    # material["95581ef0a3bb4179a1990f75c9ff7d02"] = [
    #     "\\\\172.16.0.202\\hivefiles\\sobeyhive\\buckets\\u-q3p523b4mem82k63\\2020\\12\\04\\zgg6vf029fco15q9\\95ec3bf16aae42e19e022c6671afe807.mxf"]
    # material["fa6a78f46e3444a4b225079c183b4122"] = [
    #     "\\\\172.16.0.202\\hivefiles\\sobeyhive\\buckets\\u-q3p523b4mem82k63\\2020\\12\\04\\4dg652sr2yubuksj\\92bd615b1a1c4f079c55de68a67c3d8a.mp4"]
    # material["0e76ac5e694245db8b15454d9796d968"] = [
    #     "\\\\172.16.0.202\\hivefiles\\sobeyhive\\buckets\\u-q3p523b4mem82k63\\2020\\12\\04\\3uk3adi65lf40ge2\\887e11f8bea1424f961cea2012995523.mxf"]
    # material["522a566f26b6438d96bcea9265592e94"] = [
    #     "\\\\172.16.0.202\\hivefiles\\sobeyhive\\buckets\\u-q3p523b4mem82k63\\2020\\12\\04\\r20nqm8zj2w2xvff\\ea232a2d5e314d78b8676b5fffc7bce8.mp3"]

    #日志都写在high_low文件夹内


    with open("./high_low/high_lose_guid.log", 'w', encoding="utf-8") as f_high_lose_guid:
        with open("./high_low/high_lose_guid_and_file.log", 'w', encoding="utf-8") as f_high_lose_guid_and_file:
            with open("./high_low/low_lose_guid.log", 'w', encoding="utf-8") as f_low_lose_guid:
                with open("./high_low/low_lose_guid_and_file.log", 'w', encoding="utf-8") as f_low_lose_guid_and_file:
                    with open("./high_low/lose_pic_clip.log", 'w', encoding="utf-8") as f_lose_pic_clip:
                        with open("./high_low/lose_pic_clip_and_file.log", 'w', encoding="utf-8") as f_lose_pic_clip_and_file:
                            for mat in material.keys():
                                clip = get_clip_info(mat)
                                b_high_or_low = is_high_or_low_loss(clip)
                                if (b_high_or_low == -1):  # 丢失文件不存在与高低文件中，或者没有此素材 或者不符合类型
                                    continue
                                elif b_high_or_low == 2: #图片素材
                                    f_lose_pic_clip.write(mat + "\n")
                                    f_lose_pic_clip.flush()

                                    filelists = material.get(mat)
                                    f_lose_pic_clip_and_file.write(
                                    "guid:" + mat + "\n")
                                    for filelist in filelists:
                                        f_lose_pic_clip_and_file.write(filelist + "\n")
                                        f_lose_pic_clip_and_file.flush()
                                elif b_high_or_low == 0:  # 低质量缺失
                                    f_low_lose_guid.write(mat + "\n")
                                    f_low_lose_guid.flush()

                                    filelists = material.get(mat)
                                    f_low_lose_guid_and_file.write(
                                        "guid:" + mat + "\n")
                                    for filelist in filelists:
                                        f_low_lose_guid_and_file.write(filelist + "\n")
                                        f_low_lose_guid_and_file.flush()
                                else:  # 高质量缺失
                                    f_high_lose_guid.write(mat + "\n")
                                    f_high_lose_guid.flush()

                                    filelists = material.get(mat)
                                    f_high_lose_guid_and_file.write(
                                        "guid:" + mat + "\n")
                                    for filelist in filelists:
                                        f_high_lose_guid_and_file.write(
                                            filelist + "\n")
                                        f_high_lose_guid_and_file.flush()
    ficon.close()
    ficon_lose_low.close()
