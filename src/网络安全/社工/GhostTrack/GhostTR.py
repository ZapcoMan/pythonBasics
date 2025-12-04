#!/usr/bin/python
# << HUNX04编写的代码
# << 想要重新编码？？？请先获得许可，至少要在指向此账户的GitHub账户上添加标签，
# << 更简单的方法是使用 Fork。如果不遵守以上要求，将会得到罪过，因为管理员不会同意。

# “Wahai orang-orang yang beriman! Janganlah kamu saling memakan harta sesamamu dengan jalan yang batil,” 
# (QS. An Nisaa': 29). Rasulullah SAW also melarang umatnya untuk mengambil hak orang lain tanpa izin.

# 导入模块

import json
import requests
import time
import os
import phonenumbers
from phonenumbers import carrier, geocoder, timezone
from sys import stderr

Bl = '\033[30m'  # 黑色变量
Re = '\033[1;31m'
Gr = '\033[1;32m'
Ye = '\033[1;33m'
Blu = '\033[1;34m'
Mage = '\033[1;35m'
Cy = '\033[1;36m'
Wh = '\033[1;37m'


# 实用工具

# 装饰器，用于给函数附加运行横幅
def is_option(func):
    def wrapper(*args, **kwargs):
        run_banner()
        func(*args, **kwargs)


    return wrapper


# 菜单功能
@is_option
def IP_Track():
    ip = input(f"{Wh}\n 输入目标IP : {Gr}")  # 输入IP地址
    print()
    print(f' {Wh}============= {Gr}显示IP地址信息 {Wh}=============')
    req_api = requests.get(f"http://ipwho.is/{ip}")  # API IPWHOIS.IS
    ip_data = json.loads(req_api.text)
    time.sleep(2)
    print(f"{Wh}\n 目标IP       :{Gr}", ip)
    print(f"{Wh} IP类型         :{Gr}", ip_data["type"])
    print(f"{Wh} 国家         :{Gr}", ip_data["country"])
    print(f"{Wh} 国家代码    :{Gr}", ip_data["country_code"])
    print(f"{Wh} 城市            :{Gr}", ip_data["city"])
    print(f"{Wh} 大陆       :{Gr}", ip_data["continent"])
    print(f"{Wh} 大陆代码  :{Gr}", ip_data["continent_code"])
    print(f"{Wh} 地区          :{Gr}", ip_data["region"])
    print(f"{Wh} 地区代码     :{Gr}", ip_data["region_code"])
    print(f"{Wh} 纬度        :{Gr}", ip_data["latitude"])
    print(f"{Wh} 经度       :{Gr}", ip_data["longitude"])
    lat = int(ip_data['latitude'])
    lon = int(ip_data['longitude'])
    print(f"{Wh} 地图链接            :{Gr}", f"https://www.google.com/maps/@{lat},{lon},8z")
    print(f"{Wh} 是否为欧盟国家              :{Gr}", ip_data["is_eu"])
    print(f"{Wh} 邮政编码          :{Gr}", ip_data["postal"])
    print(f"{Wh} 国际区号    :{Gr}", ip_data["calling_code"])
    print(f"{Wh} 首都         :{Gr}", ip_data["capital"])
    print(f"{Wh} 边界国家         :{Gr}", ip_data["borders"])
    print(f"{Wh} 国旗图标    :{Gr}", ip_data["flag"]["emoji"])
    print(f"{Wh} ASN             :{Gr}", ip_data["connection"]["asn"])
    print(f"{Wh} 组织机构             :{Gr}", ip_data["connection"]["org"])
    print(f"{Wh} ISP服务商             :{Gr}", ip_data["connection"]["isp"])
    print(f"{Wh} 域名          :{Gr}", ip_data["connection"]["domain"])
    print(f"{Wh} 时区ID              :{Gr}", ip_data["timezone"]["id"])
    print(f"{Wh} 缩写            :{Gr}", ip_data["timezone"]["abbr"])
    print(f"{Wh} 是否夏令时             :{Gr}", ip_data["timezone"]["is_dst"])
    print(f"{Wh} 时差偏移量          :{Gr}", ip_data["timezone"]["offset"])
    print(f"{Wh} UTC时间             :{Gr}", ip_data["timezone"]["utc"])
    print(f"{Wh} 当前时间    :{Gr}", ip_data["timezone"]["current_time"])


@is_option
def phoneGW():
    User_phone = input(
        f"\n {Wh}输入目标电话号码 {Gr}例如 [+6281xxxxxxxxx] {Wh}: {Gr}")  # 输入电话号码
    default_region = "ID"  # 默认国家 印度尼西亚

    parsed_number = phonenumbers.parse(User_phone, default_region)  # 电话号码变量
    region_code = phonenumbers.region_code_for_number(parsed_number)
    jenis_provider = carrier.name_for_number(parsed_number, "en")
    location = geocoder.description_for_number(parsed_number, "id")
    is_valid_number = phonenumbers.is_valid_number(parsed_number)
    is_possible_number = phonenumbers.is_possible_number(parsed_number)
    formatted_number = phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
    formatted_number_for_mobile = phonenumbers.format_number_for_mobile_dialing(parsed_number, default_region,
                                                                                with_formatting=True)
    number_type = phonenumbers.number_type(parsed_number)
    timezone1 = timezone.time_zones_for_number(parsed_number)
    timezoneF = ', '.join(timezone1)

    print(f"\n {Wh}========== {Gr}显示电话号码信息 {Wh}==========")
    print(f"\n {Wh}归属地             :{Gr} {location}")
    print(f" {Wh}地区代码          :{Gr} {region_code}")
    print(f" {Wh}时区             :{Gr} {timezoneF}")
    print(f" {Wh}运营商             :{Gr} {jenis_provider}")
    print(f" {Wh}是否有效号码         :{Gr} {is_valid_number}")
    print(f" {Wh}是否可能的号码      :{Gr} {is_possible_number}")
    print(f" {Wh}国际格式 :{Gr} {formatted_number}")
    print(f" {Wh}移动设备拨号格式        :{Gr} {formatted_number_for_mobile}")
    print(f" {Wh}原始号码      :{Gr} {parsed_number.national_number}")
    print(
        f" {Wh}E.164格式         :{Gr} {phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.E164)}")
    print(f" {Wh}国家代码         :{Gr} {parsed_number.country_code}")
    print(f" {Wh}本地号码         :{Gr} {parsed_number.national_number}")
    if number_type == phonenumbers.PhoneNumberType.MOBILE:
        print(f" {Wh}类型                 :{Gr} 这是一个手机号码")
    elif number_type == phonenumbers.PhoneNumberType.FIXED_LINE:
        print(f" {Wh}类型                 :{Gr} 这是一个固定电话号码")
    else:
        print(f" {Wh}类型                 :{Gr} 这是其他类型的号码")


@is_option
def TrackLu():
    try:
        username = input(f"\n {Wh}输入用户名 : {Gr}")
        results = {}
        social_media = [
            {"url": "https://www.facebook.com/{}", "name": "Facebook"},
            {"url": "https://www.twitter.com/{}", "name": "Twitter"},
            {"url": "https://www.instagram.com/{}", "name": "Instagram"},
            {"url": "https://www.linkedin.com/in/{}", "name": "LinkedIn"},
            {"url": "https://www.github.com/{}", "name": "GitHub"},
            {"url": "https://www.pinterest.com/{}", "name": "Pinterest"},
            {"url": "https://www.tumblr.com/{}", "name": "Tumblr"},
            {"url": "https://www.youtube.com/{}", "name": "Youtube"},
            {"url": "https://soundcloud.com/{}", "name": "SoundCloud"},
            {"url": "https://www.snapchat.com/add/{}", "name": "Snapchat"},
            {"url": "https://www.tiktok.com/@{}", "name": "TikTok"},
            {"url": "https://www.behance.net/{}", "name": "Behance"},
            {"url": "https://www.medium.com/@{}", "name": "Medium"},
            {"url": "https://www.quora.com/profile/{}", "name": "Quora"},
            {"url": "https://www.flickr.com/people/{}", "name": "Flickr"},
            {"url": "https://www.periscope.tv/{}", "name": "Periscope"},
            {"url": "https://www.twitch.tv/{}", "name": "Twitch"},
            {"url": "https://www.dribbble.com/{}", "name": "Dribbble"},
            {"url": "https://www.stumbleupon.com/stumbler/{}", "name": "StumbleUpon"},
            {"url": "https://www.ello.co/{}", "name": "Ello"},
            {"url": "https://www.producthunt.com/@{}", "name": "Product Hunt"},
            {"url": "https://www.snapchat.com/add/{}", "name": "Snapchat"},
            {"url": "https://www.telegram.me/{}", "name": "Telegram"},
            {"url": "https://www.weheartit.com/{}", "name": "We Heart It"}
        ]
        for site in social_media:
            url = site['url'].format(username)
            response = requests.get(url)
            if response.status_code == 200:
                results[site['name']] = url
            else:
                results[site['name']] = (f"{Ye}未找到用户名 {Ye}!")
    except Exception as e:
        print(f"{Re}错误 : {e}")
        return

    print(f"\n {Wh}========== {Gr}显示用户名信息 {Wh}==========")
    print()
    for site, url in results.items():
        print(f" {Wh}[ {Gr}+ {Wh}] {site} : {Gr}{url}")


@is_option
def showIP():
    respone = requests.get('https://api.ipify.org/')
    Show_IP = respone.text

    print(f"\n {Wh}========== {Gr}显示您的IP信息 {Wh}==========")
    print(f"\n {Wh}[{Gr} + {Wh}] 您的IP地址 : {Gr}{Show_IP}")
    print(f"\n {Wh}==============================================")


# 选项
options = [
    {
        'num': 1,
        'text': 'IP追踪',
        'func': IP_Track
    },
    {
        'num': 2,
        'text': '显示您的IP',
        'func': showIP

    },
    {
        'num': 3,
        'text': '电话号码追踪',
        'func': phoneGW
    },
    {
        'num': 4,
        'text': '用户名追踪',
        'func': TrackLu
    },
    {
        'num': 0,
        'text': '退出',
        'func': exit
    }
]


def clear():
    # windows系统
    if os.name == 'nt':
        _ = os.system('cls')
    # mac和linux系统
    else:
        _ = os.system('clear')


def call_option(opt):
    if not is_in_options(opt):
        raise ValueError('未找到选项')
    for option in options:
        if option['num'] == opt:
            if 'func' in option:
                option['func']()
            else:
                print('未检测到函数')


def execute_option(opt):
    try:
        call_option(opt)
        input(f'\n{Wh}[ {Gr}+ {Wh}] {Gr}按回车键继续')
        main()
    except ValueError as e:
        print(e)
        time.sleep(2)
        execute_option(opt)
    except KeyboardInterrupt:
        print(f'\n{Wh}[ {Re}! {Wh}] {Re}退出')
        time.sleep(2)
        exit()


def option_text():
    text = ''
    for opt in options:
        text += f'{Wh}[ {opt["num"]} ] {Gr}{opt["text"]}\n'
    return text


def is_in_options(num):
    for opt in options:
        if opt['num'] == num:
            return True
    return False


def option():
    # 工具横幅
    clear()
    stderr.writelines(f"""
       ________               __      ______                __  
      / ____/ /_  ____  _____/ /_    /_  __/________ ______/ /__
     / / __/ __ \/ __ \/ ___/ __/_____/ / / ___/ __ `/ ___/ //_/
    / /_/ / / / / /_/ (__  ) /_/_____/ / / /  / /_/ / /__/ ,<   
    \____/_/ /_/\____/____/\__/     /_/ /_/   \__,_/\___/_/|_| 

              {Wh}[ + ]  代 码 作 者  H U N X  [ + ]
    """)

    stderr.writelines(f"\n\n\n{option_text()}")


def run_banner():
    clear()
    time.sleep(1)
    stderr.writelines(f"""{Wh}
         .-.
       .'   `.          {Wh}--------------------------------
       :g g   :         {Wh}| {Gr}幽灵追踪器 - IP地址追踪 {Wh}|
       : o    `.        {Wh}|       {Gr}@代码作者 HUNXBYTS      {Wh}|
      :         ``.     {Wh}--------------------------------
     :             `.
    :  :         .   `.
    :   :          ` . `.
     `.. :            `. ``;
        `:;             `:'
           :              `.
            `.              `.     .
              `'`'`'`---..,___`;.-'
        """)
    time.sleep(0.5)


def main():
    clear()
    option()
    time.sleep(1)
    try:
        opt = int(input(f"{Wh}\n [ + ] {Gr}选择选项 : {Wh}"))
        execute_option(opt)
    except ValueError:
        print(f'\n{Wh}[ {Re}! {Wh}] {Re}请输入数字')
        time.sleep(2)
        main()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print(f'\n{Wh}[ {Re}! {Wh}] {Re}退出')
        time.sleep(2)
        exit()