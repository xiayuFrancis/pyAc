import csv
import os
import json
import configparser

material = {}
filename = 'not_exits_guid_file.json'

def dump_json():
    with open("db_guid.csv", "r", encoding="utf-8") as f:
        f_csv = csv.reader(f)
        for row in f_csv:
            for col in row:
                if col.find('.') == -1 or col.find("u-4w406h4y2u9bn7h5") == -1:
                    continue
                else:
                    #str = col.strip(";")
                    clips = col.split("|")
                    origin_path = clips[0]
                    str = clips[0]
                    guid = clips[1]
                    str = str.replace(
                        "u-4w406h4y2u9bn7h5://",
                        r"\\smb-msc-srg.media.int\hivefiles\sobeyhive\common\buckets\u-4w406h4y2u9bn7h5")
                    str = str.replace("/", "\\")
                    if not os.access(str, os.F_OK):
                        print(str)
                        if guid in material.keys():
                            filelist = material.get(guid)
                            filelist.append(str)
                            material[guid] = filelist
                        else:
                            filelist = []
                            filelist.append(str)
                            material[guid] = filelist

    filename = 'not_exits_guid_file.json'
    with open(filename, 'w') as file_obj:
        json.dump(material, file_obj)
        

if __name__ == '__main__':
    if not os.access(filename, os.F_OK):
        dump_json()
    else:
        with open(filename) as file_obj:
            material = json.load(file_obj)

    config = configparser.ConfigParser()
    path = r"setting.ini"
    config.read(path)
    suffix_name = config['fillter']['suffix']
    file_guid_suffix = "guid_" + suffix_name + ".log"
    file_All_suffix = "guid_file_" + suffix_name + ".log"

    with open(file_All_suffix, 'w', encoding="utf-8") as f_all:
        with open(file_guid_suffix, 'w', encoding="utf-8") as f_guid:
            with open("emtpy_guid_file.log", 'w', encoding="utf-8") as f:
                for key, value in material.items():
                    if(key == ""):
                        for filelist in value:
                            f.write(filelist + "\n")
                            f.flush()
                    else:
                        has_suffix = False
                        for filelist in value:
                            if filelist.endswith(suffix_name):
                                has_suffix = True
                                break

                        if has_suffix == False:
                            continue

                        f_guid.write(key + "\n")
                        f_guid.flush()
                        f_all.write(key + "\n")
                        for filelist in value:
                            f_all.write(filelist + "\n")
                            f_all.flush()
