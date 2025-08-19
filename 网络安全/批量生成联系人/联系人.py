import random
import uuid

# 随机中文姓名生成
def generate_name():
    """
    生成随机中文姓名

    Returns:
        str: 随机生成的中文姓名，由姓氏和1-2个字的名字组成
    """
    first_names = "赵钱孙李周吴郑王冯陈褚卫蒋沈韩杨朱秦尤许何吕施张孔曹严华金魏陶姜戚谢邹喻柏水窦章云苏潘葛奚范彭郎鲁韦昌马苗凤花方俞任袁柳酆鲍史唐费廉岑薛雷贺倪汤滕殷罗毕郝邬安常乐于时傅皮卞齐康伍余元卜顾孟平黄和穆萧尹姚邵湛汪祁毛禹狄米贝明臧计伏成戴谈宋茅庞熊纪舒屈项祝董梁杜阮蓝闵席季麻强贾路娄危江童颜郭梅盛林刁钟徐邱骆高夏蔡田樊胡凌霍虞万支柯咎管卢莫经房裘缪干解应宗宣丁贲邓郁单杭洪包诸左石崔吉钮龚程嵇邢滑裴陆荣翁荀羊於惠甄曲家封芮羿储靳汲邴糜松井段富巫乌焦巴弓牧隗山谷车侯宓蓬全郗班仰秋仲伊宫宁仇栾暴甘钭厉戎祖武符刘景詹束龙叶幸司韶郜黎蓟薄印宿白怀蒲邰从鄂索咸籍赖卓蔺屠蒙池乔阴郁胥能苍双闻莘党翟谭贡劳逄姬申扶堵冉宰郦雍郤璩桑桂濮牛寿通边扈燕冀郏浦尚农温别庄晏柴瞿阎充慕连茹习宦艾鱼容向古易慎戈廖庾终暨居衡步都耿满弘匡国文寇广禄阙东欧殳沃利蔚越夔隆师巩厍聂晁勾敖融冷訾辛阚那简饶空曾毋沙乜养鞠须丰巢关蒯相查后荆红游竺权逯盖益桓公万俟司马上官欧阳夏侯诸葛闻人东方赫连皇甫尉迟公羊澹台公冶宗政濮阳淳于单于太叔申屠公孙仲孙轩辕令狐钟离宇文长孙慕容鲜于闾丘司徒司空亓官司寇仉督子车颛孙端木巫马公西漆雕乐正壤驷公良拓跋夹谷宰父谷梁晋楚闫法汝鄢涂钦段干百里东郭南门呼延归海羊舌微生岳帅缑亢况郈有琴梁丘左丘东门西门商牟佘佴伯赏南宫墨哈谯笪年爱阳佟第五言福百家姓"
    last_names = "子文杰明芳娜玲强军国华丽"
    name = random.choice(first_names) + "".join(random.sample(last_names, k=random.choice([1, 2])))
    return name

# 随机手机号生成（中国大陆格式 1开头11位）
def generate_phone():
    """
    生成随机中国大陆手机号码

    Returns:
        str: 11位随机手机号码，符合中国大陆手机号格式
    """
    prefix = random.choice([
        "130","131","132","133","134","135","136","137","138","139",
        "150","151","152","153","155","156","157","158","159",
        "180","181","182","183","185","186","187","188","189"
    ])
    return prefix + "".join(random.choices("0123456789", k=8))

# 直系亲戚
direct_relatives = ["爸爸", "妈妈", "爷爷", "奶奶", "外公", "外婆"]
# 可以带排行的亲戚
ranked_relatives = ["叔叔", "舅舅", "姑姑", "姨"]
rank_prefixes = ["大", "二", "三", "四", "五"]

# 生成亲戚联系人
def generate_relative_contacts(count):
    """
    生成亲戚联系人列表

    Args:
        count (int): 需要生成的亲戚联系人数量

    Returns:
        list: 包含亲戚称谓的列表
    """
    relatives_list = []
    relatives_list.extend(direct_relatives)  # 必定存在

    # 舅舅/叔叔/姑姑/姨 → 随机加排行
    for rel in ranked_relatives:
        for prefix in random.sample(rank_prefixes, k=random.randint(1, 3)):
            relatives_list.append(prefix + rel)

    # 如果数量不足，补表兄弟姐妹
    need_more = count - len(relatives_list)
    if need_more > 0:
        others = ["表哥", "表弟", "表妹", "堂哥", "堂姐"]
        relatives_list.extend(random.sample(others, k=min(len(others), need_more)))

    return relatives_list[:count]

# 领导职称
leader_titles = ["主任", "局长", "科长", "总监", "老板", "董事长"]
# 常见部门/地区
departments = ["财务部", "人事部", "办公室", "政工处", "宣传部", "后勤科",
               "市政","工商局","教育局","开发组"]

# 生成领导联系人
def generate_leader_contacts(count):
    """
    生成领导联系人列表

    Args:
        count (int): 需要生成的领导联系人数量

    Returns:
        list: 包含领导称谓的列表
    """
    leaders = []
    surnames = "赵钱孙李周吴郑王冯陈蒋沈韩杨朱秦尤许何吕张"
    for _ in range(count):
        title = random.choice(leader_titles)

        # 50% 概率加姓
        if random.random() < 0.5:
            leader_name = random.choice(surnames) + title
        else:
            leader_name = title

        # 50% 概率加部门/地区后缀
        if random.random() < 0.5:
            leader_name = leader_name + "-" + random.choice(departments)

        leaders.append(leader_name)
    return leaders

# 生成 vCard
vcf_entries = []
total_contacts = 55
relative_count = 25   # 亲戚数量
leader_count = 21      # 领导数量
random_count = total_contacts - relative_count - leader_count

# 生成亲戚联系人vCard条目
for rel in generate_relative_contacts(relative_count):
    phone = generate_phone()
    uid = str(uuid.uuid4())
    entry = f"""BEGIN:VCARD
VERSION:3.0
N:{rel};;;;
FN:{rel}
TEL;TYPE=CELL:{phone}
UID:{uid}
END:VCARD"""
    vcf_entries.append(entry)

# 生成领导联系人vCard条目
for leader in generate_leader_contacts(leader_count):
    phone = generate_phone()
    uid = str(uuid.uuid4())
    entry = f"""BEGIN:VCARD
VERSION:3.0
N:{leader};;;;
FN:{leader}
TEL;TYPE=CELL:{phone}
UID:{uid}
END:VCARD"""
    vcf_entries.append(entry)

# 生成随机姓名联系人vCard条目
for _ in range(random_count):
    name = generate_name()
    phone = generate_phone()
    uid = str(uuid.uuid4())
    entry = f"""BEGIN:VCARD
VERSION:3.0
N:{name};;;;
FN:{name}
TEL;TYPE=CELL:{phone}
UID:{uid}
END:VCARD"""
    vcf_entries.append(entry)

# 打乱联系人顺序
random.shuffle(vcf_entries)

# 拼接 vcf 内容
vcf_content = "\r\n".join(vcf_entries)

# 保存到文件
file_path = "C:/Users/Administrator/Desktop/Decontacts.vcf"
with open(file_path, "w", encoding="utf-8-sig") as f:
    f.write(vcf_content)

print("已生成:", file_path)
