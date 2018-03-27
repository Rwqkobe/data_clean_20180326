from config import *
import pymongo
from excel_saver import save_as_excel
from utils import *

client = pymongo.MongoClient(MONGO_URL)
db = client[MONGO_DB_VEHICLE]

path = r'D:\数据分布\车辆\json_dir'


def parse_vehicle_json(j):
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
                d['score'] = vehicle['attrs'].get('score', '未定义')
                d['hard_sample'] = vehicle['attrs'].get('hard_sample', '未定义')
                d['occlusion'] = vehicle['attrs'].get('occlusion', '未定义')
                d['humanCheck'] = vehicle['attrs'].get('humanCheck', '未定义')
                d['ignore'] = vehicle['attrs'].get('ignore', '未定义')
                d['part'] = vehicle['attrs'].get('part', '未定义')
                d['blur'] = vehicle['attrs'].get('blur', '未定义')
                d['type'] = vehicle['attrs'].get('type', '未定义')
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


def save_to_mongo(result):
    if db[MONGO_TABLE_VEHICLE].insert(result):
        print('存储到mongodb成功', result)


def main():
    file_list = get_json_file(path)
    json_list = get_json_list(file_list)
    result = []
    for j in json_list:
        l = parse_vehicle_json(j)
        if l:
            for _ in l:
                result.append(_)
    # for _ in result:
    #     save_to_mongo(_)
    save_as_excel(result, r'D:\数据分布\车辆\vehicle.xlsx')


if __name__ == '__main__':
    main()
    # parse_time('20161108', '222307', 915)
