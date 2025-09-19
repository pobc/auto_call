import requests
import os
from PIL import Image
import io


def save_img_network(url, save_path):
    # 发送HTTP请求获得图片
    response = requests.get(url)
    # 将图片内容读成Image对象
    img = Image.open(io.BytesIO(response.content))
    # 调整图片大小
    img = img.resize((312, 312))
    # 检查目录是否存在，如果不存在则创建新的目录
    directory = os.path.dirname(save_path)
    if not os.path.exists(directory):
        os.makedirs(directory)
    # 保存图片
    img.save(save_path)


def save_data_file(data, save_path):
    with open(save_path, 'w') as file:
        file.write(data)
