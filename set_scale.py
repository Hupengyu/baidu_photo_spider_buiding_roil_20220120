# import PIL.Image as Image
from PIL import Image
import os

traj = 0


def Square_Generated(read_file, save_path, filenames):  # 创建一个函数用来产生所需要的正方形图片转化
    fsize = os.path.getsize(read_file)
    print(read_file, "文件大小：", fsize / 1024, "k")
    image = Image.open(read_file)  # 导入图片
    try:
        image.convert('RGB')
    except(OSError):
        image.close()
        os.remove(read_file)
        return None
    w, h = image.size  # 得到图片的大小
    if (w, h) == (608, 608):
        return image
    # print(w,h)
    new_image = Image.new('RGB', size=(max(w, h), max(w, h)),
                          color=(127, 127, 127))  # 创建新的一个图片，大小取长款中最长的一边，color决定了图片中填充的颜色
    # print(background)
    length = int(abs(w - h) * 0.5)  # 一侧需要填充的长度
    box = (length, 0) if w < h else (0, length)  # 放在box中
    new_image.paste(image, box)  # 产生新的图片
    new_image = new_image.resize((608, 608))  # 对图片进行缩放处理，这一步可以省略，GPU内存不足了，只能缩小跑CNN，试试效果
    # new_image.show()
    new_image.save(save_path + filenames, format='JPEG')  # 保存图片
    return new_image


if __name__ == '__main__':
    source_path = 'img_size_test/'
    save_path = 'res_img_resize/'

    # save_path = r'\\智慧监管-产品-w\1.最新收集照片\1.中国新兴建筑\0.视频\6、中国新兴建筑-火灾预警-图片\火灾视频4-已转换/'           # 新产生的正方形图片存放的路径
    for dirpath, dirnames, filenames in os.walk(source_path):
        # for filenames in os.walk(source_path):
        for file in filenames:
            path_1 = source_path + file
            # for root, _, files in os.walk(path_1):
            Square_Generated(path_1, save_path, file)  # 通过函数批量获取新的正方形图片
            print(path_1)
