import json
import os
from datetime import datetime, timedelta
from config import *
import pymongo
from excel_saver import save_as_excel

client = pymongo.MongoClient(MONGO_URL)
db = client[MONGO_DB]

path = r'D:\数据分布\车辆\json_dir'


def get_json_file(path):
    file_list = []
    for file in os.listdir(path):
        file_path = os.path.join(path, file)
        if not os.path.isdir(file_path):
            file_list.append(file_path)
    return file_list


def get_json_list(file_list):
    # 获取所有json
    json_list = []
    for file in file_list:
        with open(file, 'r') as f:
            for line in f.readlines():
                j = json.loads(line)
                json_list.append(j)
    return json_list


def parse_json(j):
    image_key = os.path.splitext(j['image_key'])[0]
    # print('now parsing', image_key)
    video_index = j['video_index']
    try:
        vehicles = j['vehicle']
    except:
        return None
    # 当前json中方框的list
    rect_list = []
    if vehicles == []:
        d = {}
        d['image_key'] = image_key
        d['video_index'] = video_index
    else:
        for vehicle in vehicles:
            try:
                d = {}
                d['image_key'] = image_key
                d['video_index'] = video_index
                d['height'] = abs(vehicle['data'][0] - vehicle['data'][1])
                d['width'] = abs(vehicle['data'][3] - vehicle['data'][2])
                d['score'] = vehicle['attrs'].get('score', None)
                d['hard_sample'] = vehicle['attrs'].get('hard_sample', None)
                d['occlusion'] = vehicle['attrs'].get('occlusion', None)
                d['humanCheck'] = vehicle['attrs'].get('humanCheck', None)
                d['ignore'] = vehicle['attrs'].get('ignore', None)
                d['part'] = vehicle['attrs'].get('part', None)
                d['blur'] = vehicle['attrs'].get('blur', None)
                d['type'] = vehicle['attrs'].get('type', None)
                d['id'] = vehicle['id']
                # 获取时间
                time_list = image_key.split('_')
                date = time_list[0]
                time = time_list[1]
                frame = int(time_list[-1])
                d['time'] = parse_time(date, time, frame)
                rect_list.append(d)
            except:
                print('error-------', vehicle)
                raise
    return rect_list


def parse_time(date, time, frame):
    year = int(date[0:4])
    month = int(date[4:6])
    day = int(date[6:])
    hour = int(time[0:2])
    minute = int(time[2:4])
    sec = int(time[4:6])
    time_origin = datetime(year=year, month=month, day=day, hour=hour, minute=minute, second=sec)
    time_last = time_origin + timedelta(milliseconds=int(62.5 * frame))
    time_str = str(time_last.hour) + str(time_last.minute) + str(time_last.second)
    return time_str


def save_to_mongo(result):
    if db[MONGO_TABLE].insert(result):
        print('存储到mongodb成功', result)


def main():
    file_list = get_json_file(path)
    json_list = get_json_list(file_list)
    result = []
    for j in json_list:
        l = parse_json(j)
        if l:
            for _ in l:
                result.append(_)
    # for _ in result:
    #     save_to_mongo(_)
    save_as_excel(result)


if __name__ == '__main__':
    main()
    # parse_time('20161108', '222307', 915)
