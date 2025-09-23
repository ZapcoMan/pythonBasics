import pyzbar.pyzbar as pyzbar
from PIL import Image, ImageEnhance, ImageFilter
import sys
import logging
import numpy as np
import requests
from io import BytesIO
import os
import json
import csv
from datetime import datetime
import re
try:
    import colorlog
    COLOR_LOGGING_AVAILABLE = True
except ImportError:
    COLOR_LOGGING_AVAILABLE = False

# 设置带颜色的日志记录
if COLOR_LOGGING_AVAILABLE:
    # 创建带颜色的日志格式
    formatter = colorlog.ColoredFormatter(
        "%(log_color)s%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        log_colors={
            'DEBUG':    'cyan',
            'INFO':     'blue',
            'WARNING':  'yellow',
            'ERROR':    'red',
            'CRITICAL': 'red,bg_white',
        }
    )

    # 创建控制台处理器并设置格式
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    # 配置根日志记录器
    logging.basicConfig(
        level=logging.INFO,
        handlers=[console_handler]
    )
else:
    # 如果colorlog不可用，使用默认的日志记录
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

def decode_data(raw_data, encoding_list):
    """
    尝试按照给定的编码格式列表解码数据。

    :param raw_data: 需要解码的原始字节数据。
    :param encoding_list: 编码格式的列表。
    :return: 解码后的字符串，如果所有格式尝试失败则返回None。
    """
    for encoding in encoding_list:
        try:
            return raw_data.decode(encoding)
        except UnicodeDecodeError:
            continue
    return None

def is_url(path):
    """
    判断给定的路径是否为网络地址

    :param path: 路径字符串
    :return: 如果是网络地址返回True，否则返回False
    """
    return path.startswith('http://') or path.startswith('https://')

def download_image(url):
    """
    从网络地址下载图片

    :param url: 图片的网络地址
    :return: PIL.Image对象，如果下载失败返回None
    """
    try:
        logging.info(f"正在下载网络图片: {url}")
        response = requests.get(url, timeout=30)
        response.raise_for_status()  # 如果响应状态码不是200会抛出异常
        image = Image.open(BytesIO(response.content))
        logging.info("网络图片下载成功")
        return image
    except requests.exceptions.RequestException as e:
        logging.error(f"下载网络图片失败: {e}")
        return None
    except Exception as e:
        logging.error(f"处理网络图片时出错: {e}")
        return None

def preprocess_image(img):
    """
    预处理图像以提高二维码识别率

    :param img: 原始图像
    :return: 预处理后的图像列表（多种处理方式）
    """
    images = []

    # 原始图像
    images.append(("原始图像", img))

    # 转换为灰度图像
    gray_img = img.convert('L')
    images.append(("灰度图像", gray_img))

    # 增强对比度
    enhancer = ImageEnhance.Contrast(gray_img)
    contrast_img = enhancer.enhance(2.0)
    images.append(("高对比度图像", contrast_img))

    # 二值化处理
    threshold = 128
    binary_img = contrast_img.point(lambda x: 0 if x < threshold else 255, '1')
    images.append(("二值化图像", binary_img))

    # 尝试不同的阈值
    for threshold in [64, 192]:
        binary_img = contrast_img.point(lambda x: 0 if x < threshold else 255, '1')
        images.append((f"二值化图像(阈值{threshold})", binary_img))

    # 额外的预处理方法，专门针对Telegram二维码
    # 1. 高斯模糊去噪后再二值化
    blurred = gray_img.filter(ImageFilter.GaussianBlur(radius=1))
    blurred_binary = blurred.point(lambda x: 0 if x < 128 else 255, '1')
    images.append(("高斯模糊+二值化", blurred_binary))

    # 2. 锐化处理
    sharpened = img.filter(ImageFilter.SHARPEN)
    images.append(("锐化图像", sharpened))

    # 3. 颜色反转处理（针对反色二维码）
    inverted = Image.eval(gray_img, lambda x: 255 - x)
    images.append(("颜色反转图像", inverted))

    # 4. 尺寸放大（小尺寸二维码处理）
    large_img = img.resize((img.width * 2, img.height * 2), Image.LANCZOS)
    images.append(("放大图像", large_img))

    return images

def classify_qr_content(content):
    """
    对二维码内容进行分类
    
    :param content: 二维码内容
    :return: 内容类型和风险等级
    """
    if not content:
        return "未知", "无风险"
    
    # URL链接
    if re.match(r'^https?://', content):
        # 检查是否为常见危险网站
        dangerous_keywords = ['phishing', 'malware', 'virus', 'hack', 'crack']
        for keyword in dangerous_keywords:
            if keyword in content.lower():
                return "网址链接", "高风险"
        return "网址链接", "低风险"
    
    # 电话号码
    if re.match(r'^tel:|^sms:|^mailto:', content):
        return "联系方式", "无风险"
    
    # WiFi信息
    if content.startswith('WIFI:'):
        return "WiFi信息", "中风险"
    
    # Bitcoin地址
    if re.match(r'^bitcoin:|^bc1', content):
        return "加密货币地址", "中风险"
    
    # 一般文本
    return "文本内容", "无风险"

def security_check(content):
    """
    对二维码内容进行安全检查
    
    :param content: 二维码内容
    :return: 安全警告信息
    """
    warnings = []
    
    if not content:
        return warnings
    
    # 检查是否包含可疑的JavaScript代码
    if re.search(r'<script.*?>.*?</script>', content, re.IGNORECASE | re.DOTALL):
        warnings.append("内容包含JavaScript代码，可能存在XSS攻击风险")
    
    # 检查是否包含可疑的可执行文件下载链接
    if re.search(r'\.(exe|bat|cmd|scr|dll|msi|apk|dmg)$', content, re.IGNORECASE):
        warnings.append("内容包含可执行文件下载链接，可能存在恶意软件风险")
    
    # 检查是否包含可疑的IP地址
    if re.search(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b', content):
        # 排除常见的合法IP范围
        ip_match = re.search(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b', content)
        if ip_match:
            ip = ip_match.group()
            # 简单检查是否为私有IP地址
            if not (ip.startswith('192.168.') or ip.startswith('10.') or 
                   ip.startswith('172.') and 16 <= int(ip.split('.')[1]) <= 31):
                warnings.append(f"内容包含公网IP地址: {ip}，请谨慎访问")
    
    return warnings

def export_results(results, export_format='json'):
    """
    导出扫描结果
    
    :param results: 扫描结果列表
    :param export_format: 导出格式 ('json' 或 'csv')
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    if export_format == 'json':
        filename = f"qr_scan_results_{timestamp}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        logging.info(f"结果已导出到 {filename}")
    
    elif export_format == 'csv':
        filename = f"qr_scan_results_{timestamp}.csv"
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            if results:
                writer = csv.DictWriter(f, fieldnames=results[0].keys())
                writer.writeheader()
                writer.writerows(results)
        logging.info(f"结果已导出到 {filename}")

def scan_directory(directory_path):
    """
    扫描目录中的所有图片文件
    
    :param directory_path: 目录路径
    :return: 图片文件路径列表
    """
    image_extensions = ('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff', '.webp')
    image_files = []
    
    try:
        for filename in os.listdir(directory_path):
            if filename.lower().endswith(image_extensions):
                image_files.append(os.path.join(directory_path, filename))
        logging.info(f"在目录 {directory_path} 中找到 {len(image_files)} 个图片文件")
    except Exception as e:
        logging.error(f"扫描目录时出错: {e}")
    
    return image_files

def decode_qrcode(image_path):
    """
    解码给定路径下的二维码图像。

    :param image_path: 二维码图像文件的路径或网络地址。
    :return: 解码结果字典
    """
    result = {
        'image_path': image_path,
        'content': None,
        'content_type': None,
        'risk_level': None,
        'security_warnings': [],
        'barcode_type': None,
        'timestamp': datetime.now().isoformat(),
        'success': False
    }

    logging.info(f"开始解码二维码: {image_path}")
    # 尝试打开图像文件
    img = None
    if is_url(image_path):
        # 如果是网络地址，先下载图片
        img = download_image(image_path)
        if img is None:
            return result
    else:
        # 本地文件路径
        try:
            img = Image.open(image_path)
        except FileNotFoundError:
            logging.error(f"文件未找到: {image_path}")
            return result
        except IOError:
            logging.error(f"无法打开文件: {image_path}")
            return result

    # 使用pyzbar解码图像中的二维码
    try:
        # 尝试多种预处理方式
        processed_images = preprocess_image(img)
        decoded_objects = []

        for name, processed_img in processed_images:
            try:
                temp_objects = pyzbar.decode(processed_img)
                if temp_objects:
                    decoded_objects = temp_objects
                    logging.info(f"使用 {name} 成功解码")
                    break
            except Exception as e:
                # 忽略单个预处理图像的解码错误，继续尝试其他处理方式
                logging.debug(f"使用 {name} 解码时出错: {e}")
                continue

        # 如果所有预处理方式都失败，尝试使用不同配置
        if not decoded_objects:
            try:
                # 明确指定只解码二维码，避免PDF417解码器被触发
                decoded_objects = pyzbar.decode(img, symbols=[pyzbar.ZBarSymbol.QRCODE])
            except AttributeError:
                decoded_objects = pyzbar.decode(img)
            except Exception as e:
                logging.debug(f"使用QRCODE符号解码时出错: {e}")

            if not decoded_objects:
                # 尝试除PDF417外的其他支持的符号类型
                symbol_types = [
                    'QRCODE',
                    'EAN13',
                    'EAN8',
                    'CODE128',
                    'CODE39',
                    'UPCA',
                    'UPCE'
                    # 故意排除PDF417相关类型以避免断言错误
                ]

                for symbol_name in symbol_types:
                    if hasattr(pyzbar.ZBarSymbol, symbol_name):
                        symbol = getattr(pyzbar.ZBarSymbol, symbol_name)
                        try:
                            temp_objects = pyzbar.decode(img, symbols=[symbol])
                            if temp_objects:
                                decoded_objects = temp_objects
                                logging.info(f"使用 {symbol_name} 格式成功解码")
                                break
                        except Exception as e:
                            logging.debug(f"使用 {symbol_name} 解码时出错: {e}")
                            continue

        if decoded_objects:
            # 获取第一个解码对象的数据
            raw_data = decoded_objects[0].data
            result['barcode_type'] = str(decoded_objects[0].type)

            # 尝试将原始数据解码为UTF-8字符串
            decoded_data = decode_data(raw_data, ['utf-8', 'gbk', 'gb2312'])
            if decoded_data:
                result['content'] = decoded_data
                logging.info(f"二维码内容: {decoded_data}")
            else:
                # 如果文本解码失败，至少显示原始字节数据的十六进制表示
                hex_data = raw_data.hex()
                result['content'] = hex_data
                logging.info(f"二维码数据(HEX): {hex_data}")
                logging.warning("无法将二维码数据解码为文本格式")
            
            # 分类内容和安全检查
            if result['content']:
                content_type, risk_level = classify_qr_content(result['content'])
                result['content_type'] = content_type
                result['risk_level'] = risk_level
                result['security_warnings'] = security_check(result['content'])
                result['success'] = True
        else:
            logging.warning("标准方法未能解码二维码，尝试额外的处理方法")

            # 针对Telegram二维码的特殊处理
            # 1. 尝试更激进的图像处理
            # 转换为RGBA模式再处理
            if img.mode != 'RGBA':
                rgba_img = img.convert('RGBA')
                try:
                    decoded_objects = pyzbar.decode(rgba_img)
                    if decoded_objects:
                        logging.info("RGBA转换后解码成功")
                except Exception as e:
                    logging.debug(f"RGBA转换后解码出错: {e}")

            # 2. 如果还是无法解码，输出一些诊断信息
            if not decoded_objects:
                # 检查是否包含多个二维码
                # 尝试裁剪图像的四个角分别解码
                width, height = img.size
                crops = [
                    ("左上角", (0, 0, width//2, height//2)),
                    ("右上角", (width//2, 0, width, height//2)),
                    ("左下角", (0, height//2, width//2, height)),
                    ("右下角", (width//2, height//2, width, height))
                ]

                for name, box in crops:
                    cropped_img = img.crop(box)
                    try:
                        temp_objects = pyzbar.decode(cropped_img)
                        if temp_objects:
                            decoded_objects = temp_objects
                            logging.info(f"在裁剪区域 {name} 中成功解码")
                            break
                    except Exception as e:
                        logging.debug(f"裁剪区域 {name} 解码出错: {e}")
                        continue

            if decoded_objects:
                # 获取解码结果
                raw_data = decoded_objects[0].data
                decoded_data = decode_data(raw_data, ['utf-8', 'gbk', 'gb2312'])
                if decoded_data:
                    result['content'] = decoded_data
                    logging.info(f"二维码内容: {decoded_data}")
                else:
                    hex_data = raw_data.hex()
                    result['content'] = hex_data
                    logging.info(f"二维码数据(HEX): {hex_data}")
                    logging.warning("无法将二维码数据解码为文本格式")
                
                # 分类内容和安全检查
                if result['content']:
                    content_type, risk_level = classify_qr_content(result['content'])
                    result['content_type'] = content_type
                    result['risk_level'] = risk_level
                    result['security_warnings'] = security_check(result['content'])
                    result['success'] = True
            else:
                logging.error("经过所有尝试后仍然无法解码二维码")
                logging.info("建议：确保二维码清晰完整，或尝试使用专门的二维码应用扫描")
    except Exception as e:
        logging.error(f"解码过程中发生错误: {e}")
        return result
    
    return result

def generate_qr_code(data, filename=None):
    """
    生成二维码
    
    :param data: 要编码的数据
    :param filename: 保存的文件名
    """
    try:
        import qrcode
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"generated_qr_{timestamp}.png"
        
        img.save(filename)
        logging.info(f"二维码已生成并保存为: {filename}")
        return filename
    except ImportError:
        logging.error("生成二维码需要安装 qrcode 库，请运行: pip install qrcode[pil]")
        return None
    except Exception as e:
        logging.error(f"生成二维码时出错: {e}")
        return None

def print_result_summary(result):
    """
    打印结果摘要
    
    :param result: 解码结果
    """
    if result['success']:
        logging.info("=" * 50)
        logging.info("扫描结果摘要:")
        logging.info(f"文件路径: {result['image_path']}")
        logging.info(f"内容类型: {result['content_type']}")
        logging.info(f"风险等级: {result['risk_level']}")
        logging.info(f"二维码内容: {result['content']}")
        logging.info(f"条码类型: {result['barcode_type']}")
        
        if result['security_warnings']:
            logging.warning("安全警告:")
            for warning in result['security_warnings']:
                logging.warning(f"  - {warning}")
        logging.info("=" * 50)
    else:
        logging.error(f"无法解码二维码: {result['image_path']}")

def main():
    """
    主函数
    """
    try:
        print("二维码扫描器增强版")
        print("功能选项:")
        print("1. 扫描二维码 (默认)")
        print("2. 批量扫描目录")
        print("3. 扫描并导出结果")
        
        choice = input("请选择功能 (1-3, 默认为1): ").strip()
        
        if choice == "2":
            # 批量扫描目录
            directory = input("请输入包含二维码图片的目录路径: ").strip()
            if not os.path.isdir(directory):
                logging.error("无效的目录路径")
                return
            
            image_files = scan_directory(directory)
            if not image_files:
                logging.info("目录中未找到图片文件")
                return
            
            results = []
            for image_path in image_files:
                result = decode_qrcode(image_path)
                print_result_summary(result)
                results.append(result)
            
            # 询问是否导出结果
            export = input("是否导出扫描结果? (y/N): ").strip().lower()
            if export == 'y':
                format_choice = input("选择导出格式 (json/csv, 默认json): ").strip().lower()
                export_format = format_choice if format_choice in ['json', 'csv'] else 'json'
                export_results(results, export_format)
        
        elif choice == "3":
            # 扫描并导出结果
            image_paths_input = input("请输入二维码图片的路径(多个路径用逗号分隔): ")
            image_paths = [path.strip() for path in image_paths_input.split(',') if path.strip()]
            
            if not image_paths:
                logging.error("未提供有效的图片路径")
                return
            
            results = []
            for i, image_path in enumerate(image_paths):
                if len(image_paths) > 1:
                    logging.info(f"正在处理第 {i+1} 个二维码图片: {image_path}")
                result = decode_qrcode(image_path)
                print_result_summary(result)
                results.append(result)
            
            export_format = input("选择导出格式 (json/csv, 默认json): ").strip().lower()
            export_format = export_format if export_format in ['json', 'csv'] else 'json'
            export_results(results, export_format)
        
        else:
            # 默认扫描功能
            image_paths_input = input("请输入二维码图片的路径(多个路径用逗号分隔): ")
            image_paths = [path.strip() for path in image_paths_input.split(',') if path.strip()]
            
            if not image_paths:
                logging.error("未提供有效的图片路径")
                return
            
            for i, image_path in enumerate(image_paths):
                if len(image_paths) > 1:
                    logging.info(f"正在处理第 {i+1} 个二维码图片: {image_path}")
                result = decode_qrcode(image_path)
                print_result_summary(result)

    except KeyboardInterrupt:
        logging.error("程序被中断")
        sys.exit(1)
    except Exception as e:
        logging.error(f"程序运行出错: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()