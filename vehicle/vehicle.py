from config import *
import pymongo
from excel_saver import save_as_excel
from utils import *
from weather_dict import weather_dict

client = pymongo.MongoClient(MONGO_URL)
db = client[MONGO_DB_VEHICLE]
mode = 'train'

path = r'D:\数据分布\车辆\{}_data'.format(mode)


def parse_vehicle_json(path_name, j):
    image_name = os.path.splitext(j['image_key'])[0]

    if image_name.find('Adas') != -1:
        image_name = image_name.replace('-', '_')
        image_name = image_name.split('_')
        image_key = image_name[1] + "_" + image_name[2] + "_" + "0"
        # print(image_key)
    else:
        image_key = os.path.splitext(j['image_key'])[0]

    video_index = int(j['video_index'])
    try:
        vehicles = j['vehicle']
    except:
        return None
    # 当前json中方框的list
    rect_list = []
    if vehicles == []:
        d = {}
        d['path'] = path_name
        d['image_key'] = image_key
        d['video_index'] = video_index
    else:
        for vehicle in vehicles:
            try:
                d = {}
                d['path'] = path_name
                d['image_key'] = image_key
                d['video_index'] = video_index
                d['height'] = abs(round(float(vehicle['data'][3]) - float(vehicle['data'][1]), 1))
                d['width'] = abs(round(float(vehicle['data'][2]) - float(vehicle['data'][0]), 1))
                # d['score'] = vehicle['attrs'].get('score', None)
                d['hard_sample'] = vehicle['attrs'].get('hard_sample', None)
                d['occlusion'] = vehicle['attrs'].get('occlusion', None)
                d['humanCheck'] = vehicle['attrs'].get('humanCheck', None)
                d['ignore'] = vehicle['attrs'].get('ignore', None)
                d['part'] = vehicle['attrs'].get('part', None)
                d['blur'] = vehicle['attrs'].get('blur', None)
                d['type'] = vehicle['attrs'].get('type', None)
                d['id'] = int(vehicle['id'])
                # 自定义的特征
                try:
                    d['h/w'] = round(float(d['height'] / d['width']), 1)
                except ZeroDivisionError:
                    d['h/w'] = None
                d['area'] = round(float(d['height'] * d['width']), 0)
                d['data_id'] = d['path'].split('_')[0]
                d['weather'] = weather_dict.get(d['data_id'], None)
                # 获取时间
                time_list = image_key.split('_')
                if len(time_list) > 2:
                    date = time_list[0]
                    time = time_list[1]
                    frame = int(time_list[-1])
                    d['time'] = parse_time(date, time, frame)
                    d['hour'] = int(d['time'][:2])
                else:
                    d['time'] = None
                    d['hour'] = None

                rect_list.append(d)
            except:
                print('image_key---', image_key)
                print('j-----------', j)
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
    # for j in json_list:
    #     l = parse_vehicle_json(j)
    #     if l:
    #         for _ in l:
    #             result.append(_)

    i = 1
    for json_dict in json_list:  # json_dict = ['文件名':list]
        for path_name, each_json_list in json_dict.items():
            for j in each_json_list:
                l = parse_vehicle_json(path_name.split('\\')[-1], j)
                if l:
                    for _ in l:
                        result.append(_)
                        # 当list中内容过多时，存储进本地文件中
                        if len(result) > 400000:
                            # save_memory(result)
                            save_as_excel(result, r'D:\数据分布\车辆\vehicle_{0}_{1}.xlsx'.format(mode, i))
                            i += 1
                            result = []
    save_as_excel(result, r'D:\数据分布\车辆\vehicle_{0}_{1}.xlsx'.format(mode, i))

    # for _ in result:
    #     save_to_mongo(_)
    save_as_excel(result, r'D:\数据分布\车辆\vehicle_{0}_{1}.xlsx'.format(mode, i))


if __name__ == '__main__':
    main()
    # parse_time('20161108', '222307', 915)
