from datetime import datetime, timedelta
import json
import os


def parse_time(date, time, frame):
    year = int(date[0:4])
    month = int(date[4:6])
    day = int(date[6:])
    hour = int(time[0:2])
    minute = int(time[2:4])
    sec = int(time[4:6])
    time_origin = datetime(year=year, month=month, day=day, hour=hour, minute=minute, second=sec)
    time_last = time_origin + timedelta(milliseconds=int(62.5 * frame))
    time_str = to_str(time_last.hour) + to_str(time_last.minute) + to_str(time_last.second)
    return time_str


def to_str(i):
    if i < 10:
        s = "0" + str(i)
    else:
        s = str(i)
    return s


def get_json_file(path):
    file_list = []
    for file in os.listdir(path):
        file_path = os.path.join(path, file)
        if not os.path.isdir(file_path):
            file_list.append(file_path)
    return file_list


def get_json_list(file_list):  # 更新：建立了一个dict，以每个文件名path为key，里面放这个文件名里面的json list
    # 获取所有json
<<<<<<< HEAD
=======
<<<<<<< HEAD
>>>>>>> 499f49f6800a8bbb8afeb9c7a40c26813897b7ed
    json_list = []
    for file in file_list:
        l = []
        json_dict = {}
<<<<<<< HEAD
=======
=======
    json_dict = {}
    json_list = []
    for file in file_list:
        l = []
>>>>>>> cb0e496a283b6874c848a1b94b1faa84d3c14646
>>>>>>> 499f49f6800a8bbb8afeb9c7a40c26813897b7ed
        with open(file, 'r') as f:
            for line in f.readlines():
                j = json.loads(line)
                l.append(j)
        json_dict[file] = l
        json_list.append(json_dict)

    return json_list
