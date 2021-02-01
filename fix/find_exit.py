import csv
import os
import requests

all_origin_list = []
filename = 'not_exits.log'

material = {}

# find all not exits origin path
# with open("db.csv", "r", encoding="utf-8") as f:
#     with open(filename, 'w', encoding="utf-8") as file_object:
#         f_csv = csv.reader(f)
#         for row in f_csv:
#             for col in row:
#                 if col.find('.')== -1 or col.find("u-4w406h4y2u9bn7h5")== -1:
#                     continue
#                 else:
#                     origin_path = col
#                     str = col.strip(";")
#                     str = str.replace("u-4w406h4y2u9bn7h5://", r"\\smb-msc-srg.media.int\hivefiles\sobeyhive\common\buckets\u-4w406h4y2u9bn7h5")
#                     str = str.replace("/", "\\")
#                     if not os.access(str, os.F_OK):
#                         all_origin_list.append(origin_path)
#                         print(str)
#                         file_object.write(str+"\n")
#                         file_object.flush()
#                        #alist.append(str)

#use origin path find guid
with open("db_guid.csv", "r", encoding="utf-8") as f:
    with open(filename, 'w', encoding="utf-8") as file_object:
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
                        all_origin_list.append(origin_path)
                        print(str)
                        file_object.write(str + "\n")
                        file_object.flush()

                        if guid in material.keys():
                            filelist = material.get(guid)
                            filelist.append(str)
                            material[guid] = filelist
                        else:
                            filelist = []
                            filelist.append(str)
                            material[guid] = filelist

                       # alist.append(str)


with open("guid_filepath.log", 'w', encoding="utf-8") as file_object:
    with open("guid.log", 'w', encoding="utf-8") as f:
        for key, value in material.items():
            str = key
            f.write(str + "\n")
            f.flush()
            file_object.write("guid:  " + str + "\n")
            file_object.flush()
            for file in value:
                file_object.write(file + "\n")
                file_object.flush()



