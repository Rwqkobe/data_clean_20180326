import json
import os

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
    video_index = j['video_index']
    vehicles = j['vehicle']
    # 当前json中方框的list
    rect_list = []
    for vehicle in vehicles:
        d = {}
        d['image_key'] = image_key
        d['video_index'] = video_index
        d['height'] = abs(vehicle['data'][0] - vehicle['data'][1])
        d['width'] = abs(vehicle['data'][3] - vehicle['data'][2])
        # d['time'] =


def main():
    file_list = get_json_file(path)
    json_list = get_json_list(file_list)


if __name__ == '__main__':
    main()
