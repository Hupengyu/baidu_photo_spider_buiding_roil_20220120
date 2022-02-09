"""根据搜索词下载百度图片"""
import os
import re
from typing import List, Tuple
from urllib.parse import quote

import requests

from conf import *


def get_page_urls(page_url: str, headers: dict) -> Tuple[List[str], str]:
    """获取当前翻页的所有图片的链接
    Args:
        page_url: 当前翻页的链接
        headers: 请求表头
    Returns:
        当前翻页下的所有图片的链接, 当前翻页的下一翻页的链接
    """
    if not page_url:
        return [], ''
    try:
        html = requests.get(page_url, headers=headers)
        html.encoding = 'utf-8'
        html = html.text
    except IOError as e:
        print(e)
        return [], ''
    pic_urls = re.findall('"objURL":"(.*?)",', html, re.S)
    next_page_url = re.findall(re.compile(r'<a href="(.*)" class="n">下一页</a>'), html, flags=0)
    next_page_url = 'http://image.baidu.com' + next_page_url[0] if next_page_url else ''
    return pic_urls, next_page_url


def down_pic(pic_urls: List[str], max_download_images: int, file_path) -> None:
    """给出图片链接列表，下载所有图片
    Args:
        pic_urls: 图片链接列表
        max_download_images: 最大下载数量
    """
    pic_urls = pic_urls[:max_download_images]
    for i, pic_url in enumerate(pic_urls):
        try:
            pic = requests.get(pic_url, timeout=15)
            image_output_path = file_path + '/' + str(i + 1) + '.jpg'
            with open(image_output_path, 'wb') as f:
                f.write(pic.content)
                print('成功下载第%s张图片: %s' % (str(i + 1), str(pic_url)))
        except IOError as e:
            print('下载第%s张图片时失败: %s' % (str(i + 1), str(pic_url)))
            print(e)
            continue


if __name__ == '__main__':
    keyword = '工地 浮土'  # 扬尘裸土不苫盖;裸土覆盖不到位;裸土;工地 浮土 / 工地建筑垃圾;建筑垃圾裸露;建筑垃圾
    max_download_images = 40000
    file_path = './images_uncovered_3'  # images_uncovered_0;images_uncovered_1;images_uncovered_2;images_uncovered_3
    # images_garbage_0;images_garbage_1;images_garbage_2

    url_init = url_init_first + quote(keyword, safe='/')
    all_pic_urls = []
    page_urls, next_page_url = get_page_urls(url_init, headers)
    all_pic_urls.extend(page_urls)

    page_count = 0  # 累计翻页数
    if not os.path.exists(file_path):
        os.mkdir(file_path)

    # 获取图片链接
    while 1:
        page_urls, next_page_url = get_page_urls(next_page_url, headers)
        page_count += 1
        print('正在获取第%s个翻页的所有图片链接' % str(page_count))
        if next_page_url == '' and page_urls == []:
            print('已到最后一页，共计%s个翻页' % page_count)
            break
        all_pic_urls.extend(page_urls)
        if len(all_pic_urls) >= max_download_images:
            print('已达到设置的最大下载数量%s' % max_download_images)
            break

    down_pic(list(set(all_pic_urls)), max_download_images, file_path)
