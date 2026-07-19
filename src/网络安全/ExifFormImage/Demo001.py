from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
import argparse


def get_exif_data(image_path):
    """从图片中提取完整的 EXIF 信息"""
    try:
        img = Image.open(image_path)
    except FileNotFoundError:
        print(f"[!] 文件未找到: {image_path}")
        return None
    except Exception as e:
        print(f"[!] 无法打开图片: {e}")
        return None

    exif_raw = img._getexif()
    if not exif_raw:
        print("[!] 该图片不包含 EXIF 信息")
        return None

    exif = {}
    for tag_id, value in exif_raw.items():
        tag_name = TAGS.get(tag_id, tag_id)
        exif[tag_name] = value

    return exif


def parse_gps_info(gps_raw):
    """解析 GPS 原始数据为可读格式"""
    gps = {}
    for key, value in gps_raw.items():
        name = GPSTAGS.get(key, key)
        gps[name] = value

    lat = None
    lon = None
    altitude = None

    # 解析纬度
    if "GPSLatitude" in gps and "GPSLatitudeRef" in gps:
        ref = gps["GPSLatitudeRef"]
        d, m, s = gps["GPSLatitude"]
        lat = float(d) + float(m) / 60 + float(s) / 3600
        if ref == "S":
            lat = -lat

    # 解析经度
    if "GPSLongitude" in gps and "GPSLongitudeRef" in gps:
        ref = gps["GPSLongitudeRef"]
        d, m, s = gps["GPSLongitude"]
        lon = float(d) + float(m) / 60 + float(s) / 3600
        if ref == "W":
            lon = -lon

    # 解析海拔
    if "GPSAltitude" in gps:
        alt = gps["GPSAltitude"]
        if isinstance(alt, tuple) and len(alt) == 2:
            altitude = float(alt[0]) / float(alt[1]) if alt[1] else float(alt[0])
        else:
            altitude = float(alt)
        if gps.get("GPSAltitudeRef") == 1:
            altitude = -altitude

    return {
        "纬度": lat,
        "经度": lon,
        "海拔(m)": altitude,
        "地图链接": f"https://www.google.com/maps?q={lat},{lon}" if lat and lon else None,
        "原始数据": gps,
    }


def format_value(value):
    """将值格式化为可读字符串"""
    if isinstance(value, bytes):
        try:
            return value.decode("utf-8", errors="replace")
        except Exception:
            return value[:20].hex() + "..."
    if isinstance(value, tuple):
        if len(value) == 2 and value[1] != 0:
            return f"{value[0]}/{value[1]} ({value[0] / value[1]:.4f})"
        return ", ".join(str(v) for v in value)
    if isinstance(value, int) and value > 100000:
        return f"{value} (0x{value:08X})"
    return value


def print_basic_info(exif):
    """打印基本 EXIF 信息"""
    important_keys = [
        "Make", "Model", "Software",
        "DateTime", "DateTimeOriginal", "DateTimeDigitized",
        "ExposureTime", "FNumber", "ISOSpeedRatings",
        "FocalLength", "Flash", "WhiteBalance",
        "ImageWidth", "ImageLength", "Orientation",
        "XResolution", "YResolution",
        "LensMake", "LensModel",
        "Copyright", "Artist",
    ]

    print("=" * 60)
    print("  基本 EXIF 信息")
    print("=" * 60)
    for key in important_keys:
        if key in exif:
            print(f"  {key:<25} {format_value(exif[key])}")


def print_gps_info(exif):
    """解析并打印 GPS 地理信息"""
    print()
    print("=" * 60)
    print("  GPS 地理位置信息")
    print("=" * 60)

    gps_raw = exif.get("GPSInfo")
    if not gps_raw:
        print("  [!] 该图片不包含 GPS 信息")
        return

    gps = parse_gps_info(gps_raw)

    if gps["纬度"] is not None and gps["经度"] is not None:
        print(f"  {'纬度':<20} {gps['纬度']:.6f}°")
        print(f"  {'经度':<20} {gps['经度']:.6f}°")
    else:
        print("  [!] 无法解析经纬度")

    if gps["海拔(m)"] is not None:
        print(f"  {'海拔':<20} {gps['海拔(m)']:.2f} m")

    if gps["地图链接"]:
        print(f"  {'Google 地图':<20} {gps['地图链接']}")

    print()
    print("  -- GPS 原始标签 --")
    for key, value in gps["原始数据"].items():
        print(f"  {key:<25} {format_value(value)}")


def print_all_exif(exif):
    """打印所有 EXIF 标签"""
    print()
    print("=" * 60)
    print("  全部 EXIF 标签")
    print("=" * 60)
    for key, value in exif.items():
        if key == "GPSInfo":
            continue
        print(f"  {key:<30} {format_value(value)}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="提取并解析图片 EXIF 信息（含 GPS 地理位置）")
    parser.add_argument("-i", "--image", required=True, help="指定图片文件路径")
    parser.add_argument("-a", "--all", action="store_true", help="输出全部 EXIF 标签")
    args = parser.parse_args()

    exif = get_exif_data(args.image)
    if not exif:
        exit(1)

    print_basic_info(exif)
    print_gps_info(exif)

    if args.all:
        print_all_exif(exif)
