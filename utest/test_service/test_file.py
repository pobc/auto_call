import os
import json
from pathlib import Path


def read_directory_contents(directory_path):
    """
    读取指定目录下的所有文件及其内容

    Args:
        directory_path (str): 目录路径

    Returns:
        dict: 包含文件名和内容的字典
    """
    # 使用 Path 对象处理路径，这样更安全且跨平台
    path = Path(directory_path)

    # 存储结果的字典
    results = {}

    try:
        # 确保目录存在
        if not path.exists():
            raise FileNotFoundError(f"目录不存在: {directory_path}")

        # 遍历目录中的所有文件
        for file_path in path.glob('*'):
            if file_path.is_file():  # 只处理文件，不处理子目录
                try:
                    # 尝试以UTF-8读取文件内容
                    with file_path.open('r', encoding='utf-8') as f:
                        content = f.read()

                    # 如果文件看起来像JSON，尝试解析它
                    if file_path.suffix.lower() in ['.json', '']:
                        try:
                            content = json.loads(content)
                        except json.JSONDecodeError:
                            # 如果解析失败，保持原始文本内容
                            pass

                    results[file_path.name] = {
                        'path': str(file_path),
                        'content': content
                    }
                except UnicodeDecodeError:
                    # 如果UTF-8解码失败，尝试其他编码
                    try:
                        with file_path.open('r', encoding='gbk') as f:
                            content = f.read()
                        results[file_path.name] = {
                            'path': str(file_path),
                            'content': content
                        }
                    except Exception as e:
                        results[file_path.name] = {
                            'path': str(file_path),
                            'error': f'无法读取文件内容: {str(e)}'
                        }
                except Exception as e:
                    results[file_path.name] = {
                        'path': str(file_path),
                        'error': f'处理文件时出错: {str(e)}'
                    }

        return results

    except Exception as e:
        raise Exception(f"处理目录时出错: {str(e)}")


# 使用示例
if __name__ == "__main__":
    directory = r"C:\work\chlsData\xianyu\acs.m.goofish.com\gw\mtop.taobao.idle.house.search\1.0"

    try:
        results = read_directory_contents(directory)

        # 打印结果
        for filename, data in results.items():
            print(f"\n文件名: {filename}")
            print(f"路径: {data['path']}")
            if 'error' in data:
                print(f"错误: {data['error']}")
            else:
                print("内容类型:", type(data['content']))
                print("内容预览:",
                      str(data['content'])[:200] + "..." if len(str(data['content'])) > 200 else data['content'])

    except Exception as e:
        print(f"错误: {str(e)}")