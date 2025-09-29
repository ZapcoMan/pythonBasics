import random
import uuid
from datetime import datetime, timedelta

# 常见姓氏
common_surnames = [
    "王", "李", "张", "刘", "陈", "杨", "赵", "黄", "周", "吴",
    "徐", "孙", "胡", "朱", "高", "林", "何", "郭", "马", "罗",
    "梁", "宋", "郑", "谢", "韩", "唐", "冯", "于", "董", "萧",
    "程", "曹", "袁", "邓", "许", "傅", "沈", "曾", "彭", "吕",
    "苏", "卢", "蒋", "蔡", "贾", "丁", "魏", "薛", "叶", "阎"
]

# 常见男性名字
male_names = [
    "伟", "芳", "娜", "敏", "静", "丽", "强", "磊", "军", "洋",
    "勇", "艳", "杰", "娟", "涛", "明", "超", "秀英", "霞", "平",
    "刚", "桂英", "鹏", "红", "华", "亮", "敏", "宁", "婷", "波",
    "丹", "建华", "静", "洁", "晶", "凯", "丽娟", "玲", "龙", "梅",
    "楠", "倩", "琴", "荣", "涛", "霞", "晓", "燕", "颖", "志强"
]

# 常见女性名字
female_names = [
    "伟", "芳", "娜", "敏", "静", "丽", "秀英", "霞", "桂英", "艳",
    "娟", "红", "丽娟", "玲", "丹", "秀兰", "秀珍", "秀芳", "婷", "玉兰",
    "梅", "洁", "晶", "丽丽", "霞", "秀云", "秀梅", "丽华", "琴", "丽萍",
    "秀英", "丽娜", "丽娟", "秀霞", "丽琴", "秀兰", "丽红", "丽梅", "丽芳", "秀珍"
]

# 家庭关系
family_relations = {
    "爸爸": {"gender": "male", "min_age": 30, "max_age": 70},
    "妈妈": {"gender": "female", "min_age": 30, "max_age": 70},
    "爷爷": {"gender": "male", "min_age": 60, "max_age": 90},
    "奶奶": {"gender": "female", "min_age": 60, "max_age": 90},
    "外公": {"gender": "male", "min_age": 60, "max_age": 90},
    "外婆": {"gender": "female", "min_age": 60, "max_age": 90},
    "大伯": {"gender": "male", "min_age": 30, "max_age": 70},
    "二伯": {"gender": "male", "min_age": 30, "max_age": 70},
    "叔叔": {"gender": "male", "min_age": 25, "max_age": 65},
    "舅舅": {"gender": "male", "min_age": 25, "max_age": 65},
    "姑姑": {"gender": "female", "min_age": 25, "max_age": 65},
    "姨": {"gender": "female", "min_age": 25, "max_age": 65},
    "表哥": {"gender": "male", "min_age": 18, "max_age": 40},
    "表弟": {"gender": "male", "min_age": 5, "max_age": 30},
    "表妹": {"gender": "female", "min_age": 5, "max_age": 30},
    "堂哥": {"gender": "male", "min_age": 18, "max_age": 40},
    "堂姐": {"gender": "female", "min_age": 18, "max_age": 40}
}

# 职业和部门
positions = ["主任", "局长", "科长", "总监", "老板", "董事长", "经理", "主管", "工程师", "会计", "出纳", "文员"]
departments = ["财务部", "人事部", "办公室", "政工处", "宣传部", "后勤科", "市政", "工商局", "教育局", "开发组",
               "技术部", "销售部", "市场部"]

# 同事关系
colleague_relations = ["同事", "合作伙伴", "客户", "供应商"]

# 朋友关系
friend_relations = ["朋友", "同学", "战友", "邻居"]

# 真实的手机号段分布
phone_prefixes = [
    # 移动
    "134", "135", "136", "137", "138", "139", "147", "150", "151", "152",
    "157", "158", "159", "178", "182", "183", "184", "187", "188", "198",
    # 联通
    "130", "131", "132", "145", "155", "156", "166", "175", "176", "185",
    "186", "196",
    # 电信
    "133", "149", "153", "173", "177", "180", "181", "189", "191", "199"
]


# 生成随机中文姓名
def generate_name(gender=None):
    """
    生成随机中文姓名

    Args:
        gender (str): 性别，'male' 或 'female'，如果为 None 则随机

    Returns:
        tuple: (姓名, 性别)
    """
    surname = random.choice(common_surnames)

    if gender is None:
        gender = random.choice(['male', 'female'])

    if gender == 'male':
        name_part = random.choice(male_names)
    else:
        name_part = random.choice(female_names)

    # 有一定概率生成双字名
    if random.random() < 0.3:
        name_part += random.choice(["华", "明", "强", "军", "丽", "娟", "伟", "芳", "娜", "敏"])

    return surname + name_part, gender


# 生成真实感更强的手机号码
def generate_phone():
    """
    生成更真实的中国大陆手机号码

    Returns:
        str: 11位手机号码
    """
    prefix = random.choice(phone_prefixes)
    return prefix + "".join(random.choices("0123456789", k=8))


# 生成生日（根据年龄）
def generate_birthday(age):
    """
    根据年龄生成生日

    Args:
        age (int): 年龄

    Returns:
        str: 生日，格式为 YYYY-MM-DD
    """
    current_year = datetime.now().year
    birth_year = current_year - age
    # 随机生成月份和日期
    birth_month = random.randint(1, 12)
    # 简化处理每月天数
    birth_day = random.randint(1, 28)
    return f"{birth_year}-{birth_month:02d}-{birth_day:02d}"


# 生成家庭联系人
def generate_family_contacts(count):
    """
    生成家庭联系人列表

    Args:
        count (int): 需要生成的家庭联系人数量

    Returns:
        list: 包含家庭联系人信息的列表
    """
    family_list = []
    relations = list(family_relations.keys())

    # 确保包含基本的直系亲属
    basic_relations = ["爸爸", "妈妈", "爷爷", "奶奶", "外公", "外婆"]
    for relation in basic_relations:
        if len(family_list) < count:
            family_list.append(relation)

    # 补充其他亲属
    while len(family_list) < count:
        family_list.append(random.choice(relations))

    return family_list[:count]


# 生成领导联系人
def generate_leader_contacts(count):
    """
    生成领导联系人列表

    Args:
        count (int): 需要生成的领导联系人数量

    Returns:
        list: 包含领导联系人信息的列表
    """
    leaders = []
    for _ in range(count):
        position = random.choice(positions)

        # 70% 概率加姓
        if random.random() < 0.7:
            surname = random.choice(common_surnames)
            leader_name = surname + position
        else:
            leader_name = position

        # 60% 概率加部门后缀
        if random.random() < 0.6:
            leader_name = leader_name + "-" + random.choice(departments)

        leaders.append(leader_name)
    return leaders


# 生成同事联系人
def generate_colleague_contacts(count):
    """
    生成同事联系人列表

    Args:
        count (int): 需要生成的同事联系人数量

    Returns:
        list: 包含同事联系人信息的列表
    """
    colleagues = []
    for _ in range(count):
        relation = random.choice(colleague_relations)
        surname = random.choice(common_surnames)

        # 80% 概率加职位或部门信息
        if random.random() < 0.8:
            if random.random() < 0.5:
                # 添加职位
                position = random.choice(positions)
                colleague_name = surname + relation + "(" + position + ")"
            else:
                # 添加部门
                department = random.choice(departments)
                colleague_name = surname + relation + "(" + department + ")"
        else:
            colleague_name = surname + relation

        colleagues.append(colleague_name)
    return colleagues


# 生成朋友联系人
def generate_friend_contacts(count):
    """
    生成朋友联系人列表

    Args:
        count (int): 需要生成的朋友联系人数量

    Returns:
        list: 包含朋友联系人信息的列表
    """
    friends = []
    for _ in range(count):
        relation = random.choice(friend_relations)
        surname = random.choice(common_surnames)
        friend_name = surname + relation
        friends.append(friend_name)
    return friends


# 生成 vCard
vcf_entries = []
total_contacts = 1540
family_count = 345  # 家庭联系人数量
leader_count = 200  # 领导数量
colleague_count = 300  # 同事数量
friend_count = 200  # 朋友数量
random_count = total_contacts - family_count - leader_count - colleague_count - friend_count  # 随机联系人

# 生成家庭联系人vCard条目
family_relations_list = generate_family_contacts(family_count)
for relation in family_relations_list:
    name, gender = generate_name(family_relations[relation]["gender"])
    phone = generate_phone()
    age = random.randint(family_relations[relation]["min_age"], family_relations[relation]["max_age"])
    birthday = generate_birthday(age)
    uid = str(uuid.uuid4())
    entry = f"""BEGIN:VCARD
VERSION:3.0
N:{name};;;{
    relation};
FN:{name}({relation})
TEL;TYPE=CELL:{phone}
BDAY:{birthday}
UID:{uid}
END:VCARD"""
    vcf_entries.append(entry)

# 生成领导联系人vCard条目
for leader in generate_leader_contacts(leader_count):
    name, gender = generate_name()
    phone = generate_phone()
    age = random.randint(25, 65)
    birthday = generate_birthday(age)
    uid = str(uuid.uuid4())
    entry = f"""BEGIN:VCARD
VERSION:3.0
N:{name};;;{
    leader};
FN:{name}({leader})
TEL;TYPE=CELL:{phone}
BDAY:{birthday}
UID:{uid}
END:VCARD"""
    vcf_entries.append(entry)

# 生成同事联系人vCard条目
for colleague in generate_colleague_contacts(colleague_count):
    name, gender = generate_name()
    phone = generate_phone()
    age = random.randint(22, 60)
    birthday = generate_birthday(age)
    uid = str(uuid.uuid4())
    entry = f"""BEGIN:VCARD
VERSION:3.0
N:{name};;;{
    colleague};
FN:{name}({colleague})
TEL;TYPE=CELL:{phone}
BDAY:{birthday}
UID:{uid}
END:VCARD"""
    vcf_entries.append(entry)

# 生成朋友联系人vCard条目
for friend in generate_friend_contacts(friend_count):
    name, gender = generate_name()
    phone = generate_phone()
    age = random.randint(18, 55)
    birthday = generate_birthday(age)
    uid = str(uuid.uuid4())
    entry = f"""BEGIN:VCARD
VERSION:3.0
N:{name};;;{
    friend};
FN:{name}({friend})
TEL;TYPE=CELL:{phone}
BDAY:{birthday}
UID:{uid}
END:VCARD"""
    vcf_entries.append(entry)

# 生成随机姓名联系人vCard条目
for _ in range(random_count):
    name, gender = generate_name()
    phone = generate_phone()
    age = random.randint(18, 70)
    birthday = generate_birthday(age)
    uid = str(uuid.uuid4())
    entry = f"""BEGIN:VCARD
VERSION:3.0
N:{name};;;; 
FN:{name}
TEL;TYPE=CELL:{phone}
BDAY:{birthday}
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
