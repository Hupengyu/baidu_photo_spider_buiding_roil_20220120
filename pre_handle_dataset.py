import os
import cv2
from glob import glob
import PIL.Image as Image
import numpy as np


# 删除无法读取的图片
def del_error_img(DirList):
    for img_dir in DirList:
        for filename in os.listdir(img_dir):
            image = os.path.join(img_dir, filename)
            img = cv2.imread(image)
            if img is None:
                os.remove(image)  # 删除无法读取的图片


# 删除过小的图片
def del_img_small(DirList):
    for img_dir in DirList:
        print(img_dir)
        tall = 0
        small = 0
        for filename in os.listdir(img_dir):
            fullName = os.path.join(img_dir, filename)
            size = os.path.getsize(fullName)
            if size < 30 * 1024:
                small = small + 1
                os.remove(fullName)
            tall = tall + 1
        # print(tall, small, small / tall * 100)


# 删除重复的图片
def img_2_np(img):
    img_np = np.array(img)
    return img_np


def np_total(np):
    num = 0
    for y in np:
        for x in y:
            for n in x:
                num += n
    return num


def find_same(packet_box):
    mark_box = []
    same_pic_path = []
    for num, packet in enumerate(packet_box):
        data_box = []
        for n in range(len(packet_box)):
            if (num != n):
                if (n in mark_box):
                    continue
                else:
                    data = packet[-1] / packet_box[n][-1]
                    data_box.append(data)
        if (1.0 in data_box):
            mark_box.append(num)
    for mark in mark_box:
        same_pic_path.append(packet_box[mark][0])
    return same_pic_path


def del_same_pic(DirList):
    for img_dir in DirList:
        path_box = []
        packet_box = []
        for pic_name in (os.listdir(img_dir)):
            if pic_name.split('.')[-1] in ["JPG", "png", "jpeg", "jpg", "JPEG", "PNG"]:
                full_path = img_dir + "/" + pic_name
                path_box.append(full_path)
            else:
                continue
        for path in path_box:
            try:
                img = Image.open(path)
                img_np = img_2_np(img)
                np_total_data = np_total(img_np)
                singe_packet = (path, img, img_np, np_total_data)
                packet_box.append(singe_packet)
            except Exception:
                pass
        same = find_same(packet_box)
        for del_path in same:
            os.remove(del_path)
        print("finish, removed {} same pic in all {} pic, same percent is {}%".format(len(same), len(path_box),
                                                                                      (len(same) / len(path_box)) * 100))


if __name__ == '__main__':
    path = 'images_uncovered_test'
    path1 = 'images_uncovered_0'
    path2 = 'images_uncovered_1'
    path3 = 'images_uncovered_2'
    path4 = 'images_garbage_0'
    path5 = 'images_garbage_1'
    path6 = 'images_garbage_2'

    # DirList = [path1, path2, path3, path4, path5, path6]
    DirList = [path]

    # 删除无法读取的图片
    del_error_img(DirList)

    # 删除过小的图片
    del_img_small(DirList)

    # 删除重复的图片
    del_same_pic(DirList)
