from PIL import Image
from PIL.ExifTags import TAGS
import argparse


def extract_exif(image_path):
    """从图片中提取 EXIF 信息并返回字典"""
    try:
        img = Image.open(image_path)
    except FileNotFoundError:
        print(f"[!] 文件未找到: {image_path}")
        return None
    except Exception as e:
        print(f"[!] 无法打开图片: {e}")
        return None

    exif_data = img._getexif()
    if not exif_data:
        print("[!] 该图片不包含 EXIF 信息")
        return None

    result = {}
    for tag_id, value in exif_data.items():
        tag_name = TAGS.get(tag_id, tag_id)
        result[tag_name] = value

    return result


def print_exif(exif_dict):
    """格式化打印 EXIF 信息"""
    print(f"{'标签':<30} {'值'}")
    print("-" * 70)
    for key, value in exif_dict.items():
        if isinstance(value, bytes):
            value = value[:20].hex() + "..."
        print(f"{key:<30} {value}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="提取图片中的 EXIF 信息")
    parser.add_argument("-i", "--image", required=True, help="指定图片文件路径")
    args = parser.parse_args()

    exif = extract_exif(args.image)
    if exif:
        print_exif(exif)
