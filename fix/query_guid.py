import requests
import json
import configparser
import os
# query clip by guid

filename = 'not_exits_guid_file.json'

material = {}

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


print("load guid.....")

guid = []
with open("guid.log", "r", encoding="utf-8") as f:
    for line in f:
        guid.append(line.strip())

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

print("start query.....")
with open("material_info.log", 'w', encoding="utf-8") as f:
    for id in guid:
        queryUrl = requestUrl.replace("{}", id)
        r = requests.get(queryUrl, headers=headers)
        if r.status_code == 200:
            clip = json.loads(r.text)
            if(clip.get("code") == "0"):
                try:
                    print("guid:  " + clip.get("ext").get("entity").get("guid"))
                    print("name:  " + clip.get("ext").get("entity").get("name"))
                    print(
                        "folderpath:  " +
                        clip.get("ext").get("entity").get("folderpath"))
                    print("\r\n")
                    f.write(
                        "guid:  " +
                        clip.get("ext").get("entity").get("guid") +
                        "\n")
                    f.write(
                        "name:  " +
                        clip.get("ext").get("entity").get("name") +
                        "\n")
                    f.write(
                        "folderpath:  " +
                        clip.get("ext").get("entity").get("folderpath") +
                        "\n")
                    print_filelist_by_json_dump(id, f)
                except BaseException:
                    continue
            else:
                f.write("not find guid:  " + id + "\n")
                print_filelist_by_json_dump(id, f)
                print("hive not have this guid:" + id)
        else:
            print("can't acess server")
