from config import *
import pymongo
import json
from excel_saver import save_as_excel
from utils import *
<<<<<<< HEAD
from weather_dict import weather_dict

client = pymongo.MongoClient(MONGO_URL)
db = client[MONGO_DB_PEDESTRIAN]
mode = 'train'

path = r'D:\数据分布\行人\zyy_pedestrian\{}_data'.format(mode)
=======

client = pymongo.MongoClient(MONGO_URL)
db = client[MONGO_DB_PEDESTRIAN]

<<<<<<< HEAD
path = r'D:\数据分布\行人\zyy_pedestrian\train_data'
=======
path = r'D:\数据分布\行人\zyy_pedestrian\test_json'
>>>>>>> cb0e496a283b6874c848a1b94b1faa84d3c14646
>>>>>>> 499f49f6800a8bbb8afeb9c7a40c26813897b7ed


def parse_pedestrian_json(path_name, j):
    image_name = os.path.splitext(j['image_key'])[0]
    # if image_name.find('ADAS'):
    #     image_name = image_name.replace('-', '_')
    #     image_key = image_name[1] + '_' + image_name[2] + '_' + '0'
    if image_name.find('Michigan') != -1:
        # print(image_name, 'find Michigan')
        return None
    # 暂时先不关带ADAS的数据
    if image_name.find('ADAS') != -1:
        image_name = image_name.replace('-', '_')
        image_name = image_name.split('_')
<<<<<<< HEAD
        image_key = image_name[1] + "_" + image_name[2] + "_" + "0"
=======
<<<<<<< HEAD
        image_key = image_name[1] + "_" + image_name[2] + "_" + "0"
=======
        image_key = image_name[1] + '_' + image_name[2] + '_' + '0'
>>>>>>> cb0e496a283b6874c848a1b94b1faa84d3c14646
>>>>>>> 499f49f6800a8bbb8afeb9c7a40c26813897b7ed
        # print(image_key)
    else:
        image_key = os.path.splitext(j['image_key'])[0]
    # print('now parsing', image_key)
    video_index = j['video_index']
    try:
        persons = j['person']
    except:
<<<<<<< HEAD
=======
        # print('no person')
>>>>>>> 499f49f6800a8bbb8afeb9c7a40c26813897b7ed
        return None
    # 当前json中方框的list
    rect_list = []
    if persons == []:
        d = {}
        d['path'] = path_name
        d['image_key'] = image_key
        d['video_index'] = int(video_index)
    else:
        for person in persons:
            try:
                d = {}
                d['path'] = path_name
                d['image_key'] = image_key
                d['video_index'] = video_index
<<<<<<< HEAD
                d['height'] = abs(round(float(person['data'][3]) - float(person['data'][1]),1))
                d['width'] = abs(round(float(person['data'][2]) - float(person['data'][0]),1))
=======
<<<<<<< HEAD
                d['height'] = abs(int(float(person['data'][0]) - float(person['data'][1])))
                d['width'] = abs(int(float(person['data'][3]) - float(person['data'][2])))
=======
                d['height'] = abs(float(person['data'][0]) - float(person['data'][1]))
                d['width'] = abs(float(person['data'][3]) - float(person['data'][2]))
>>>>>>> cb0e496a283b6874c848a1b94b1faa84d3c14646
>>>>>>> 499f49f6800a8bbb8afeb9c7a40c26813897b7ed
                # d['score'] = person['attrs'].get('score', None)
                d['hard_sample'] = person['attrs'].get('hard_sample', None)
                d['occlusion'] = person['attrs'].get('occlusion', None)
                d['humanCheck'] = person['attrs'].get('humanCheck', None)
                d['ignore'] = person['attrs'].get('ignore', None)
                d['part'] = person['attrs'].get('part', None)
                d['blur'] = person['attrs'].get('blur', None)
                d['type'] = person['attrs'].get('type', None)
<<<<<<< HEAD
                d['id'] = int(person['id'])
                # 自定义的特征
                d['h/w'] = round(float(d['height'] / d['width']),1)
                d['area'] = round(float(d['height'] * d['width']),0)
=======
<<<<<<< HEAD
                d['id'] = int(person['id'])
=======
                d['id'] = person['id']
>>>>>>> cb0e496a283b6874c848a1b94b1faa84d3c14646
>>>>>>> 499f49f6800a8bbb8afeb9c7a40c26813897b7ed
                # 获取时间
                time_list = image_key.split('_')
                date = time_list[0]
                time = time_list[1]
                frame = int(time_list[-1])
                d['time'] = parse_time(date, time, frame)
<<<<<<< HEAD
                d['hour'] = int(d['time'][:2])

                d['data_id'] = d['path'].split('_')[0]
                d['weather'] = weather_dict.get(d['data_id'], None)
=======
>>>>>>> 499f49f6800a8bbb8afeb9c7a40c26813897b7ed
                rect_list.append(d)
            except:
                print('error-------', person)
                print('imageKey----', image_key)
                print('j-----------', j)
                continue
    # print('rect_list', rect_list)
    return rect_list


def save_to_mongo(results):
    for result in results:
        if db[MONGO_TABLE_PEDESTRIA].insert(result):
            # print('存储到mongodb成功', result)
            pass
        else:
            print('存储到mongodb失败', result)


def save_memory(result):
    with open('temp.json', 'a')as f:
        for _ in result:
            json.dump(_, f)
            f.write('\n')


<<<<<<< HEAD
=======
<<<<<<< HEAD
>>>>>>> 499f49f6800a8bbb8afeb9c7a40c26813897b7ed
def main():
    file_list = get_json_file(path)  # 返回所有文件名
    json_list = get_json_list(file_list)
    result = []
    i = 1
<<<<<<< HEAD
=======
=======

def main():
    file_list = get_json_file(path)  # 返回所有文件名
    json_list = get_json_list(file_list)
    file_list = None  # 释放内存
    result = []
>>>>>>> cb0e496a283b6874c848a1b94b1faa84d3c14646
>>>>>>> 499f49f6800a8bbb8afeb9c7a40c26813897b7ed
    for json_dict in json_list:  # json_dict = ['文件名':list]
        for path_name, each_json_list in json_dict.items():
            for j in each_json_list:
                l = parse_pedestrian_json(path_name.split('\\')[-1], j)
                if l:
                    for _ in l:
                        result.append(_)
                        # 当list中内容过多时，存储进本地文件中
<<<<<<< HEAD
                        if len(result) > 400000:
                            # save_memory(result)
                            save_as_excel(result, r'D:\数据分布\行人\pedestrian_{0}_{1}.xlsx'.format(mode,i))
                            i += 1
                            result = []
    save_as_excel(result, r'D:\数据分布\行人\pedestrian_{0}_{1}.xlsx'.format(mode,i))
    # save_memory(result)
=======
<<<<<<< HEAD
                        if len(result) > 400000:
                            # save_memory(result)
                            save_as_excel(result, r'D:\数据分布\行人\{}.xlsx'.format(i))
                            i += 1
                            result = []
    save_as_excel(result, r'D:\数据分布\行人\train_{}.xlsx'.format(i))
    # save_memory(result)
=======
                        if len(result) > 10000:
                            save_memory(result)
                            result = []
    save_memory(result)
>>>>>>> cb0e496a283b6874c848a1b94b1faa84d3c14646
>>>>>>> 499f49f6800a8bbb8afeb9c7a40c26813897b7ed
    # for _ in result:
    #     save_to_mongo(_)
    # print(result)

<<<<<<< HEAD
=======
<<<<<<< HEAD
=======
    # save_as_excel(result, r'D:\数据分布\行人\pedestrian.xlsx')
>>>>>>> cb0e496a283b6874c848a1b94b1faa84d3c14646
>>>>>>> 499f49f6800a8bbb8afeb9c7a40c26813897b7ed
    # save_to_mongo(result)
    print('OK')


if __name__ == '__main__':
    main()
    # parse_time('20161108', '222307', 915)
