import os
import cv2
from glob import glob

images_uncovered_0 = glob('images_uncovered_0/*.jpg')  # images_uncovered;images_uncovered_1;images_garbage_0;images_garbage_1
images_uncovered_1 = glob('images_uncovered_1/*.jpg')
images_uncovered_2 = glob('images_uncovered_2/*.jpg')
images_garbage_1 = glob('images_garbage_1/*.jpg')
images_garbage_2 = glob('images_garbage_2/*.jpg')


def img_count(images, img_file):
    count = 0
    for image in images:
        img = cv2.imread(image)
        if img is not None:
            # print(image)
            count = count + 1
    print(img_file + '共有' + str(count) + '张图片')


if __name__ == '__main__':
    img_count(images_uncovered_0, 'images_uncovered_0')
    img_count(images_uncovered_1, 'images_uncovered_1')
    img_count(images_uncovered_2, 'images_uncovered_2')
    img_count(images_garbage_1, 'images_garbage_1')
    img_count(images_garbage_2, 'images_garbage_2')
# def file_name(file_dir):
#     for root, dirs, files in os.walk(file_dir):
#         for file in files:
#             if os.path.splitext(file)[1] == '.jpg':
#                 img = cv2.imread(image)
#                 if img is None:
#                     # print(image)
#                     os.remove(image)  # 删除有问题的图片
